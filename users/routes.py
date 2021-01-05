from fastapi import APIRouter, Depends, HTTPException
from users.schemas import RegisterForm
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, auth_user
from users.schemas import Token
from datetime import timedelta

user_router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@user_router.post('/register', status_code=200)
def register_user(register_form: RegisterForm):
    #form = register_form.dict()
    return None

@user_router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}