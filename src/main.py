from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from model import AuthResponse, User, UserInRequest
from auth_logic import (
    get_current_active_user,
    generate_new_access_token,
    register_new_user,
    disable_token,
    TOKEN_URL
)

app = FastAPI()
origins = [
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(f"/{TOKEN_URL}", response_model=AuthResponse)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):

    (access_token, user) = generate_new_access_token(form_data.username,
                                                     form_data.password)

    return {"access_token": access_token,
            "token_type": "bearer",
            "username": user}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get own user account info with token.
    """
    return current_user


@app.post("/users", response_model=User)
async def register_access(user_request: UserInRequest):
    print(user_request)
    return register_new_user(user_request)


@app.delete(f"/{TOKEN_URL}")
async def disable_access_token(result: bool = Depends(disable_token)):
    return {"message": "Token disabled"}
