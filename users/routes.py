from datetime import timedelta
from typing import List

from dependencies import (ACCESS_TOKEN_EXPIRE_MINUTES, auth_user,
                          create_access_token, create_refresh_token,
                          decode_refresh_token, decode_token, get_current_user,
                          get_db, get_password_hash)
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from users.schemas import RefreshToken, RegisterForm, Token, User, UserSearch
from users.utils import (UserRepository, clear_old_registers, send_mail,
                         validate_user_register_form)

user_router = APIRouter(
    tags=['Users']
)


@user_router.post('/v2.0.0/users/register', status_code=200)
def register_user(register_form: RegisterForm, request: Request,
                  db: Session = Depends(get_db)):

    validate_user_register_form(register_form)

    # adding user register record to database
    UserRepository.add_user_register(username=register_form.username,
                                   password=register_form.password,
                                   email=register_form.email,
                                   db=db)

    # creating access token in order to insert into register email
    token = create_access_token(data={'username': register_form.username})

    # clearing previous register records
    clear_old_registers()

    # sending register email to user
    send_mail(token, register_form.email, request)
    return None


@user_router.post("/v2.0.0/users/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # checking user authentication
    user = auth_user(form_data.username, form_data.password, db=db)

    # creating access and refresh token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES*4)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expire
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expire": ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "token_type": "bearer"
    }


@user_router.post("/v2.0.0/users/refresh_token", response_model=Token)
def refresh_token(refresh_token: RefreshToken,
                  db: Session = Depends(get_db)):

    # checking refresh token validation
    username = decode_refresh_token(refresh_token.refresh_token, db=db)

    # creating new tokens
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expire": ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "token_type": "bearer"
    }


@user_router.get('/v2.0.0/users/validate_email/{token}', status_code=200)
def validate_email(token: str, db: Session = Depends(get_db)):
    from main import FRONTEND_URL
    if (username := decode_token(token)) is not None:

        # getting user registry record
        record = UserRepository.get_user_register(username=username)

        # adding user to system as designer
        UserRepository.add_user(
            username=username,
            password=record.password,
            email=record.email,
            old_record=record
        )

        return RedirectResponse(url=FRONTEND_URL)


@user_router.get('/v2.0.0/users/search_for_users', status_code=200,
                 response_model=List[UserSearch])
def search_user(search_string: str = Query(..., min_length=3),
                db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):

    return UserRepository.search_for_user_by_username(search_string, db)
