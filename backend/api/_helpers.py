import random
import string

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ._db import addToRooms, addToUsers, fetchByEmail, getFromUsers, updateUser
from ._spotify import getUserMeta


def randomString(size=22, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def jsonEncode(content, statuscode):
    obj = jsonable_encoder(content)
    res = JSONResponse(content=obj, status_code=statuscode)
    return res


def newUser(access, refresh):
    meta = getUserMeta(access)
    name = meta["display_name"]
    email = meta["email"]
    country = meta["country"]

    existing_user = fetchByEmail(email, name)
    if not existing_user:
        user = addToUsers(name, email, country, access, refresh, [])
        return user["key"]
    else:
        update = {
            "access_token": access,
            "refresh_token": refresh,
        }
        user = updateUser(update, existing_user["key"])
        return user["key"]


def newUserAlt(access, refresh):
    meta = getUserMeta(access)
    name = meta["display_name"]
    email = meta["email"]
    country = meta["country"]

    existing_user = fetchByEmail(email, name)

    if not existing_user:
        user = addToUsers(name, email, country, access, refresh, [])
        return user
    else:
        update = {
            "access_token": access,
            "refresh_token": refresh,
        }
        user = updateUser(update, existing_user["key"])
        return user


def newRoom(owner):
    user = getFromUsers(owner)
    if user == None:
        raise Exception("Sorry, no user found")
    add_room = addToRooms(
        name=user["name"] + "'s Room",
        owner=owner,
        join_code=str(randomString(size=6)),
        people=[],
        active=True,
    )
    return add_room["key"]


# ListOfString -> ListOfDict
def fetchAndModify(lou):
    """
    fetches every users name form the list of keys and returns a dict with name and identifier
    """
    loud = []
    for u in lou:
        user = getFromUsers(u)
        loud.append({"name": user["name"], "identifier": u})
    return loud
