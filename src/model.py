from typing import Union

from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    username: str


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class UserInRequest(User):
    password: str
