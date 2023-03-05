from typing import Union

from model import UserInDB

FAKE_USERS_DB = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "$2b$12$XQj9GdQCWnByERsz0N0EpulcUK6Wx13iKyN9P6l6g9cF9Kf9.50qa",  # noqa: E501
        "disabled": False,
    }
}


def get_user_from_db(username: str) -> Union[UserInDB, None]:
    user_in_db = None

    if username in FAKE_USERS_DB:
        user_dict = FAKE_USERS_DB[username]
        user_in_db = UserInDB(**user_dict)

    return user_in_db
