import json
import os

import requests

REDIS_KV_KEY = os.getenv("REDIS_KV_KEY")
REDIS_URL = os.getenv("REDIS_URL")
HEADERS = {"Authorization": f"Bearer {REDIS_KV_KEY}"}


def _setJson(key, value: dict):
    response = requests.post(f"{REDIS_URL}/set/{key}", headers=HEADERS, json=value)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error {response.status_code}: {response.text}")


def _get(key):
    response = requests.get(f"{REDIS_URL}/get/{key}", headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        return json.loads(data["result"])
    else:
        raise ValueError(f"Failed to fetch data. Status code: {response.status_code}")


def _del(key):
    response = requests.get(f"{REDIS_URL}/del/{key}", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError(f"Failed to fetch data. Status code: {response.status_code}")


def addToRooms(name, owner, join_code, people, active):
    room = {
        "name": name,
        "owner": owner,
        "join_code": join_code,
        "people": people,
        "active": active,
    }
    id = f"room_{join_code}"
    _setJson(id, room)
    return {"key": id}


def addToUsers(name, email, country, access, refresh, playlists):
    user = {
        "name": name,
        "email": email,
        "country": country,
        "access_token": access,
        "refresh_token": refresh,
        "playlists": playlists,
    }
    id = f"user_{name}_{email}"
    _setJson(id, user)
    user["key"] = id
    return user


def getFromRooms(key):
    room = _get(key)
    room["key"] = key
    return room


def getFromRoomsByJoinCode(join_code):
    id = f"room_{join_code}"
    room = _get(id)
    room["key"] = id
    return room


def getFromUsers(key):
    user = _get(key)
    user["key"] = key
    return user


def checkUserExists(user_id):
    user = _get(user_id)
    if user:
        return True
    else:
        return False


def updateRoom(newUser, key):
    room = _get(key)
    room["people"].append(newUser)  # possible race condition
    _setJson(key, room)
    room["key"] = key
    return room


def updateRoomId(data, key):
    room = _get(key)
    room["active"] = False
    room["playlist_url"] = data["playlist_url"]
    room["playlist_cover"] = data["playlist_cover"]
    room["date"] = data["date"]
    _setJson(key, room)
    room["key"] = key
    return room


def updateUser(updates, key):
    user = _get(key)
    user.update(updates)
    _setJson(key, user)
    user["key"] = key
    return user


def fetchByEmail(email, name):
    id = f"user_{name}_{email}"
    user = _get(id)
    if user:
        user["key"] = id
    return user
