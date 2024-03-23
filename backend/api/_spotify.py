import base64
import os
from secrets import *

import requests

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
ME_URL = "https://api.spotify.com/v1/me"


def stringToBase64(string):
    messageBytes = string.encode("ascii")
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode("ascii")
    return base64Message


def getUserMeta(access):
    headers = {"Authorization": "Bearer " + str(access)}
    x = requests.get(url=ME_URL, headers=headers)
    print(x.text)
    return x.json()


def get_access_and_refresh_token(code):
    message = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64Message = stringToBase64(message)
    headers = {"Authorization": "Basic " + str(base64Message)}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    aAndR = {}
    x = requests.post(url=TOKEN_URL, data=data, headers=headers)
    print(x.text)
    aAndR = {
        "access_token": x.json()["access_token"],
        "refresh_token": x.json()["refresh_token"],
    }
    return aAndR
