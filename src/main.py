from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from model import Token, User
from util import (
    get_current_active_user,
    generate_new_access_token,
    TOKEN_URL
)

app = FastAPI()


@app.post(f"/{TOKEN_URL}", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):

    access_token = generate_new_access_token(form_data.username,
                                             form_data.password)

    return {"access_token": access_token,
            "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get own user account info with token.
    """
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
        current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
