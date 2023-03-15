from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from model import User, UserInDB, UserInRequest
from db import get_user_from_db, add_user_to_db


# to get a string like this run:
# openssl genrsa 2048 -out sign_key.pem
with open("sign_key.pem", encoding="UTF-8") as s_file:
    SECRET_KEY = s_file.read()

ALGORITHM = "RS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TIME_DELTA_MINUTES = 15

TOKEN_URL = "token"


pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

black_list_token = []

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

DISABLED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Target token was disabled",
    headers={"WWW-Authenticate": "Bearer"},
)


def _verify_password(plain_password,
                     hashed_password) -> bool:
    return pwd_context.verify(plain_password,
                              hashed_password)


def _authenticate_user(username: str,
                       password: str) -> Union[UserInDB, None]:
    user = get_user_from_db(username)

    if not user:
        return None

    if not _verify_password(password,
                            user.hashed_password):
        return None

    return user


def _create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             SECRET_KEY,
                             algorithm=ALGORITHM)

    return encoded_jwt


def generate_new_access_token(username: str,
                              password: str) -> str:

    # Check user name and password validity.
    user = _authenticate_user(username,
                              password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token.
    access_token = _create_access_token(data={"sub": user.username})
    return (access_token, user.username)


def _token_validation(token):
    try:
        # Check token validity.
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
    except JWTError:
        raise CREDENTIALS_EXCEPTION

    if token in black_list_token:
        raise DISABLED_EXCEPTION

    return payload


async def _get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Check target token's validity.
    """
    payload = _token_validation(token)

    username: str = payload.get("sub")
    if username is None:
        raise CREDENTIALS_EXCEPTION

    user = get_user_from_db(username=username)
    if user is None:
        raise CREDENTIALS_EXCEPTION

    return user


async def get_current_active_user(
        current_user: User = Depends(_get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def register_new_user(user_request: UserInRequest) -> bool:
    registered_user = add_user_to_db(user_request)
    if registered_user is None:
        raise HTTPException(status_code=400, detail="User already exists")

    return registered_user


def disable_token(token: str = Depends(oauth2_scheme)) -> bool:
    _ = _token_validation(token)

    black_list_token.append(token)

    return True
