from passlib.context import CryptContext
from typing import Union

from model import User, UserInDB, UserInRequest

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "$2b$12$XQj9GdQCWnByERsz0N0EpulcUK6Wx13iKyN9P6l6g9cF9Kf9.50qa",  # noqa: E501
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")


def _get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_user_from_db(username: str) -> Union[UserInDB, None]:
    user_in_db = None

    if username in fake_users_db:
        user_dict = fake_users_db[username]
        user_in_db = UserInDB(**user_dict)

    return user_in_db


def add_user_to_db(user_request: UserInRequest) -> Union[User, None]:
    if user_request.username in fake_users_db:
        return None

    hashed_password = _get_password_hash(user_request.password)
    fake_users_db[user_request.username] = {
        "username": user_request.username,
        "full_name": user_request.full_name,
        "email": user_request.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }

    return User(username=user_request.username,
                email=user_request.email,
                full_name=user_request.full_name,
                disabled=user_request.disabled)
