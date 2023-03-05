from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from model import TokenData, User, UserInDB


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "f35580a85721bfd1944377ed69a2084bea8f4b68be586cd74730495e248990e6"
ALGORITHM = "HS256"
# ALGORITHM = "RS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TIME_DELTA_MINUTES = 15

TOKEN_URL = "token"

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def _verify_password(plain_password,
                     hashed_password) -> bool:
    return pwd_context.verify(plain_password,
                              hashed_password)


def _get_user(db, username: str) -> Optional[UserInDB]:
    user_in_db = None

    if username in db:
        user_dict = db[username]
        user_in_db = UserInDB(**user_dict)

    return user_in_db


def _authenticate_user(username: str,
                       password: str) -> Optional[UserInDB]:
    user = _get_user(fake_users_db,
                     username)

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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

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
    return access_token


async def _get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Check target token's validity.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = _get_user(fake_users_db,
                     username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: User = Depends(_get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
