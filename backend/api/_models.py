from pydantic import BaseModel


class Login(BaseModel):
    code: str
    state: str


class Confirm(BaseModel):
    join_code: str


class Join(BaseModel):
    code: str
    room_id: str


class Connect(BaseModel):
    room_key: str


class Auth(BaseModel):
    user_id: str


class Room(BaseModel):
    user_id: str
    room_id: str
