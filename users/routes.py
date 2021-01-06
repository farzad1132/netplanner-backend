from fastapi import APIRouter, Depends, HTTPException, Request
from users.schemas import RegisterForm
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, auth_user
from users.schemas import Token
from datetime import timedelta
from starlette.responses import RedirectResponse
from users.utils import send_mail

user_router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@user_router.post('/register', status_code=200)
def register_user(register_form: RegisterForm, request: Request):
    #form = register_form.dict()
    # TODO: use real token
    send_mail("1234", register_form.email, request)
    
    return None

@user_router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get('/validate_email/{token}', status_code=200)
def validate_email(token: str):
    # TODO: decode real token
    if token == "1234":
        return RedirectResponse(url='https://google.com')
    return None