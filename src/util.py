from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from model import TokenData, User, UserInDB


# to get a string like this run:
# openssl genrsa 2048
SECRET_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEArNDp6K0k6ezytKF1KkLLizWD+25PaMoGsV7d2MBko8bBng/A
dpy8Yx10mfQSSH9Euhrt+9IDhye4vpzkDm5YVYq/E+T65FQ62keWDTKP54AjjANJ
rKDsIPx/cObOxz+Wj/5GzCeriJz6ic2AsbV7o5YUre9VOHr06jWpe4w02ey714Os
Qv0bisUk7qycTrNgGg9kAbxXR4tzFMJ5M7/jyjiOMSQVpJ0zWmqE1p4m2sCnx61X
J7hBMX5YAit2ut7HQO0acuyvKCuGPTCsBhp/5ZHOv5v/vj11PhceqPFVcDCzjdbC
3UlIDVHnhfNEJkG4M6gRi0NaI7ZNb2kqax+F8wIDAQABAoIBAQCF1ZzwpvaJewlT
Ph8AxY3gl2dJFtrEqoCYaIGiVQ0bkNdtU4GX2jZDBBLDD7QBFR7iiex4MuKsjuSS
KeqsCmS6iqMEAzcSEPErDnl0aw3rGN9ulTU/TbjQqvr/MqA8ylAN37xwauB7Aic9
BTt/ZK8Ftzr4oPr8rKxznW9N0P01Lszy4xGhNcd0UH61rXkQf5FsR6Wklj/zOPyu
YNWDubt2DjEQ3AhEGHsOsyDFuTzfA2rAJLNo/vqQPpRxcXEwYAgJfcVk2p0pMiQZ
aYtTuDzZTVMhvJwU8DhewKLjTrzc4pm6NBuhBDOA++wQzG6P8zi+hlJxXMWiLde2
l6cM2CkRAoGBAN0CiDpe0SveC25re//cKHGhBODbWNPkJjqOUjJQAYYQkyf1JCLu
4dazRRuR4ibZRZPhIJNLdK1YqcWy0v6B6bTqkViKRFyRifRVAhVTCSEL/mZ2wH4n
C9N5+SI7RDa4BUGfDXG3QCOv09KLte4xrAcWBY7i4JSqNTri0P5QDxGdAoGBAMgt
GYY6H5CtPXxVtnvLCloUuMpzKwdMyzhEHP3w/ifluMXC4RVmxTOuGxgOitGR7Xcg
jD4lq+YBrjQwoOrkbMMeokwo9SRGo0dCSeck11JvHhp2HOq6jOPq3qLRb+fp9MFu
ZhqEXkf1lx1ghzPQ7Nj7/IJv+nfDT0oSFykGwujPAoGBAIfV/pShoj4sAyqitVvU
nKb6KF1rc3UITNbAkpSJx+X2Wfu9F7DA0d174YXIbA8kizcQr0zYm6XPUMlJ15TF
lDa11Q9uLAYZDYk2lkk09+9vx7SCWF0w8nvQA+eeNZbME675avHxh2JntvE5HWCA
9xKD3narywyUcJL4xSsJWbmhAoGAIjJyNdggJFs0MdWCw0tAjXsUxqE+LJUV8prQ
SSGuiapZEo/kW/+emOGZh1aUqJDBfKR20PcmkriexhO4qeg0HHFTUKd+mZ/nrPjK
H07P6ilJf0PGVONhxl4Ngss8zuXNBm6Ryt3qLWjrU/11m4iJrdf+n1n59BPNq93D
TyL0kUkCgYALI/03LxFopzBTk99bxDGCcv4d+KBvw9Jw9T3/j1PVBkvNwQyfM07n
n6eVCynvfHUVIZENi2fFpjg6yndSsWBvRV2fcIhA/WGbEzOOJye6QDeTqgfFy2cw
1ulWwS5XBx0fZ4D2fn5O/ImR22ce5e+z8e9eJzcSiHVA0MUFMxDceg==
-----END RSA PRIVATE KEY-----
"""
ALGORITHM = "RS512"
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
        # Check token validity.
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
