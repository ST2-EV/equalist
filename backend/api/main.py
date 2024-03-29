from datetime import date
from typing import Optional
from urllib.parse import urlencode

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

from ._create_playlist import make
from ._db import (
    checkUserExists,
    getFromRooms,
    getFromRoomsByJoinCode,
    getFromUsers,
    updateRoom,
    updateRoomId,
)
from ._helpers import fetchAndModify, jsonEncode, newRoom, newUser, newUserAlt
from ._models import Auth, Confirm, Join, Login, Room
from ._spotify import AUTH_URL, CLIENT_ID, REDIRECT_URI, get_access_and_refresh_token

app = FastAPI()


origins = ["http://localhost", "http://localhost:8080", "https://equalist.xyz/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(code: Optional[str] = None, state: Optional[str] = None):

    if code:
        html_content = (
            """
                        <html>
                            <head>
                                <title>Redirect from spotify</title>
                            </head>
                            <body>
                                <h1>Redirect from spotify to equalist</h1>
                                <h3>code: </h3>
                                <p>"""
            + code
            + """</p>
                                <h3>state: </h3>
                                <p>"""
            + state
            + """</p>
                            </body>
                        </html>
                        """
        )
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return {"message": "Hello World"}


@app.get("/oauth/{type}")
def oauth(type):
    """
    OAUTH REDIRECT
    """
    if type == "none":
        state = "none"
    else:
        state = type

    scope = "user-read-private user-read-email user-top-read playlist-modify-public playlist-modify-private ugc-image-upload"

    payload = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "state": state,
    }

    res = RedirectResponse(f"{AUTH_URL}/?{urlencode(payload)}")

    return res


@app.post("/login-debug")
def login(item: Login):
    """
    login with oauth token
    """
    try:
        code = item.code
        aAndR = get_access_and_refresh_token(code)
        user = newUser(aAndR["access_token"], aAndR["refresh_token"])
        room = newRoom(user)
        return jsonEncode(getFromUsers(user), 201)
    except:
        return jsonEncode({"message": "Login failed, Please try again later"}, 500)


@app.post("/login")
def login(item: Login):
    """
    login with oauth token
    """
    code = item.code
    try:
        aAndR = get_access_and_refresh_token(code)
        user_id = newUser(aAndR["access_token"], aAndR["refresh_token"])
        room_id = newRoom(user_id)
        loginobj = {"user_id": user_id, "room_id": room_id}
        return jsonEncode(loginobj, 201)
    except Exception as e:
        print(e)
        # stack trace
        raise e
        return jsonEncode({"message": "Login failed, Please try again later"}, 500)


@app.post("/create-room")
def create_room(item: Auth):
    """
    to create room for the user with the user_id
    """
    try:
        if checkUserExists(item.user_id):
            room_id = newRoom(item.user_id)
            loginobj = {"user_id": item.user_id, "room_id": room_id}
            return jsonEncode(loginobj, 201)
        else:
            return jsonEncode({"message": "User does not exist"}, 400)
    except Exception as e:
        print(e)
        return jsonEncode({"message": "Oops! room could not be created."}, 500)


@app.post("/room-info")
def room_info(item: Room):
    """
    get information of the room
    """
    try:
        room = getFromRooms(item.room_id)
        if len(room["people"]) != 0:
            room["people"] = fetchAndModify(room["people"])
        if item.user_id == room["owner"] or item.user_id in room["people"]:
            return jsonEncode(room, 201)
        else:
            jsonEncode({"message": "Sorry, you dont have access to this room!"}, 500)
    except Exception as e:
        print(e)
        return jsonEncode(
            {
                "message": "Oops! couldn't get the room's information! (It's our fault, come back later)"
            },
            500,
        )


@app.post("/create-playlist")
def create_playlist(item: Room):
    """
    creates the playlist based all the people in the room so far
    """
    try:
        room = getFromRooms(item.room_id)
        lou = []
        print(room)
        if item.user_id == room["owner"] or item.user_id in room["people"]:
            owner = getFromUsers(item.user_id)
            owner_obj = {
                "access_token": owner["access_token"],
                "refresh_token": owner["refresh_token"],
            }
            lou.append(owner_obj)
            for u in room["people"]:
                friend = getFromUsers(u)
                friend_obj = {
                    "access_token": friend["access_token"],
                    "refresh_token": friend["refresh_token"],
                }
                lou.append(friend_obj)
            today = date.today()
            d = today.strftime("%B %d")
            playlist = make(lou, owner["name"] + "'s playlist - " + d)
            playlist["playlist_name"] = owner["name"] + "'s playlist"
            playlist["date"] = d
            updateRoomId(playlist, item.room_id)
            return jsonEncode(playlist, 201)
        else:
            jsonEncode({"message": "Sorry, you can't create this playlist!"}, 500)
    except Exception as e:
        print(e)
        return jsonEncode(
            {
                "message": "Oops! couldn't create the playlist (It's our fault, come back later)"
            },
            500,
        )


@app.post("/confirm")
def confirm(item: Confirm):
    """
    confirmation before joining room
    """
    try:
        room = getFromRoomsByJoinCode(item.join_code)
        if room["active"]:
            robj = {
                "name": room["name"],
                "room_id": room["key"],
                "number_online": len(room["people"]),
            }
            return jsonEncode(robj, 200)
        else:
            return jsonEncode({"message": "Requested room is no longer active"}, 200)
    except Exception as e:
        print(e)
        return jsonEncode({"message": "Room join code invalid"}, 400)


@app.post("/join")
async def join(item: Join):
    """
    join into a room
    """
    try:
        code = item.code
        join_code = item.room_id  # ALERT: emphasis on join_code
        aAndR = get_access_and_refresh_token(code)
        user = newUserAlt(aAndR["access_token"], aAndR["refresh_token"])
        current_room = getFromRoomsByJoinCode(join_code)

        if not user["key"] in current_room["people"]:
            updateRoom(user["key"], current_room["key"])
            return jsonEncode(
                {
                    "message": "joined room",
                    "user_id": user,
                    "room_id": current_room["key"],
                },
                200,
            )
        else:
            return jsonEncode(
                {
                    "message": "joined room",
                    "user_id": user,
                    "room_id": current_room["key"],
                },
                200,
            )
    except Exception as e:
        return jsonEncode({"message": "join failed"}, 400)


@app.get("/friends/{user_id}/{room_id}")
def get_friends(user_id, room_id):
    try:
        room = getFromRooms(room_id)
        if len(room["people"]) != 0:
            room["people"] = fetchAndModify(room["people"])
        if user_id == room["owner"]:
            data = {"friends": room["people"]}
            return jsonEncode(data, 201)
        else:
            jsonEncode({"message": "Sorry, you dont have access to this room!"}, 500)
    except Exception as e:
        print(e)
        return jsonEncode(
            {
                "message": "Oops! couldn't get the room's information! (It's our fault, come back later)"
            },
            500,
        )
