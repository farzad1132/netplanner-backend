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

from models import UserModel
from users.models import UserRegisterModel
from users.schemas import RefreshToken, RegisterForm, Token, User, UserSearch
from users.utils import (clear_old_registers, send_mail,
                         validate_user_register_form)

user_router = APIRouter(
    tags=['Users']
)


@user_router.post('/v2.0.0/users/register', status_code=200)
def register_user(register_form: RegisterForm, request: Request, db: Session = Depends(get_db)):
    validate_user_register_form(register_form)

    record = UserRegisterModel(username=register_form.username,
                               password=get_password_hash(
                                   register_form.password),
                               email=register_form.email)

    db.add(record)
    db.commit()
    token = create_access_token(data={'username': register_form.username})
    clear_old_registers()
    send_mail(token, register_form.email, request)
    return None


@user_router.post("/v2.0.0/users/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = auth_user(form_data.username, form_data.password, db=db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES*4)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expire
    )
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "expire": ACCESS_TOKEN_EXPIRE_MINUTES*60,
            "token_type": "bearer"}


@user_router.post("/v2.0.0/users/refresh_token", response_model=Token)
def refresh_token(refresh_token: RefreshToken,
                  db: Session = Depends(get_db)):
    username = decode_refresh_token(refresh_token.refresh_token, db=db)
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "expire": ACCESS_TOKEN_EXPIRE_MINUTES*60,
            "token_type": "bearer"}


@user_router.get('/v2.0.0/users/validate_email/{token}', status_code=200)
def validate_email(token: str, db: Session = Depends(get_db)):
    if (username := decode_token(token)) is not None:
        if (record := db.query(UserRegisterModel).filter_by(username=username)
                .one_or_none()) is not None:
            user = UserModel(username=username,
                             password=record.password,
                             email=record.email,
                             role='designer')
            db.delete(record)
            db.add(user)
            db.commit()
            return RedirectResponse(url='http://192.168.7.22')


@user_router.get('/v2.0.0/users/search_for_users', status_code=200, response_model=List[UserSearch])
def search_user(search_string: str = Query(..., min_length=3),
                db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    results = db.query(UserModel)\
        .filter(UserModel.username.contains(search_string))\
        .filter_by(is_deleted=False).all()
    return results
