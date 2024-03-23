# Use the make function to create the playlist based on the users

# Data Types Refernce:
## User
## examples:
user1 = {
    "access_token": "asdasaghui9orhe9wfhuewq324234",
    "refresh_token": "asdasdasdafasdfafafdsadafsad",
}

## ListOfUser (Input)
## examples:
lou1 = [user1, user1, user1]

## ListOfTrackId
## examples:
loti1 = ["3dQjCswDedsHNxdaOhcfiz", "5Ii1kY2dSOyMZpRGFa6NxO"]

## PlaylistObj (Output)
##examples:
OBJ1 = {
    "playlist_url": "",
    "playlist_id": "",
    "playlist_name": "",
    "playlist_cover": "",
}

# Main code to make the playlist
import functools
import math
import operator
import os
import random

import requests

NUMBER_OF_SONGS_PER_PLAYLIST = 25
TRACK_URL = "https://api.spotify.com/v1/me/top/tracks"
REC_URL = "https://api.spotify.com/v1/recommendations"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# ListOfUser String -> PlaylistObj
def make(lou, playlist_name):
    """
    the main function that creates the playlist and returns a link to it.
    """
    tracks_per_user = math.ceil(NUMBER_OF_SONGS_PER_PLAYLIST / len(lou))
    loti = get_pop_tracks(lou, tracks_per_user)
    loti = functools.reduce(
        operator.iconcat, loti, []
    )  # makes list of lists into a single list
    loti = list(set(loti))  # removes duplicates
    loti = random.sample(loti, len(loti))
    loti = fill_if_empty(loti, lou)
    return create_playlist_api(loti, lou[0], playlist_name)


# ListOfUser, Number -> ListOf[ListOfTrackId]
def get_pop_tracks(lou, tracks_per_user):
    """
    returns a list of lists that contain the top tracks of each user respectively.
    """
    loti = []
    for u in lou:
        loti.append(get_track(u, tracks_per_user))
    return loti


# User Number -> ListOfTrackId
def get_track(u, tracks_per_user):
    """
    returns a list of the top tracks of the given user.
    """
    x = requests.get(
        TRACK_URL,
        headers={
            "Authorization": "Bearer " + protect(u["access_token"], u["refresh_token"])
        },
        params={"limit": tracks_per_user},
    )
    return [n["id"] for n in x.json()["items"]]


# String String -> String
def protect(access_token, refresh_token):
    """
    returns new access token if the given access token timed out or returns the same access token.
    """
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + access_token}
    x = requests.get(url, headers=headers)
    if "error" in x.json().keys():
        acc_token = get_access_token(refresh_token)
        return acc_token["access_token"]
    return access_token


# String -> String
def get_access_token(refresh_token):
    """
    gets a new access token from spotify with the given refresh token.
    """
    url = "https://accounts.spotify.com/api/token"
    myobj = {
        "Content-Type": "application/x-www-form-urlencoded",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    x = requests.post(url, auth=(CLIENT_ID, CLIENT_SECRET), data=myobj)
    return x.json()


# ListOfTrackId ListOfUser-> ListOfTrackId
def fill_if_empty(loti, lou):
    """
    if the given loti has less tracks than required then fills the gaps with recommendations from spotify otherwise
    returns loti itself.
    """
    if len(loti) >= NUMBER_OF_SONGS_PER_PLAYLIST:
        return loti
    else:
        x = requests.get(
            REC_URL,
            headers={
                "Authorization": "Bearer "
                + protect(lou[0]["access_token"], lou[0]["refresh_token"])
            },
            params={
                "limit": abs(NUMBER_OF_SONGS_PER_PLAYLIST - len(loti)),
                "seed_tracks": ",".join(loti[0:5]),
            },
        )
        return loti + [n["id"] for n in x.json()["tracks"]]


# ListOfTrackId User String -> PlaylistObj
def create_playlist_api(final_playlist, user, playlist_name):
    """
    create a playlist on spoitfy with the given list of trackids and playist name
    """
    user_id = get_user_info(user["access_token"], user["refresh_token"])["id"]
    url = "https://api.spotify.com/v1/users/" + user_id + "/playlists"
    headers = {
        "Authorization": "Bearer "
        + protect(user["access_token"], user["refresh_token"])
    }
    x = requests.post(
        url,
        json={
            "name": playlist_name,
            "description": "Made by equalist.xyz",
            "public": True,
        },
        headers=headers,
    )

    playlist_url = x.json()["external_urls"]["spotify"]
    playlist_id = x.json()["id"]
    # adding
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
    headers = {
        "Authorization": "Bearer "
        + protect(user["access_token"], user["refresh_token"])
    }
    uris = ["spotify:track:" + track for track in final_playlist]
    uris = list(set(uris))
    y = requests.post(url, json={"uris": uris}, headers=headers)
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/images"
    img = requests.get(url, headers=headers)
    return {
        "playlist_url": playlist_url,
        "playlist_id": playlist_id,
        "playlist_name": playlist_name,
        "playlist_cover": img.json()[1]["url"],
    }


# String String -> JSON object
def get_user_info(access_token, refresh_token):
    """
    returns meta information about the user(ex: user_id, etc) from spotify.
    """
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + access_token}
    x = requests.get(url, headers=headers)
    if "error" in x.json().keys():
        acc_token = get_access_token(refresh_token)
        url = "https://api.spotify.com/v1/me"
        headers = {"Authorization": "Bearer " + acc_token["access_token"]}
        x = requests.get(url, headers=headers)
    return x.json()
