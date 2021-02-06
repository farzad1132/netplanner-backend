from fastapi import APIRouter, Depends, HTTPException, Request, Query, Body
from users.schemas import RegisterForm, Token, UserSearch, User, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, auth_user,
 get_password_hash, get_db, decode_token, get_current_user, create_refresh_token, decode_refresh_token)
from datetime import timedelta
from starlette.responses import RedirectResponse
from users.utils import send_mail
from users.models import UserRegisterModel
from sqlalchemy.orm import Session
from models import UserModel
from typing import List

user_router = APIRouter(
    tags=['Users']
)

@user_router.post('/v2.0.0/users/register', status_code=200)
def register_user(register_form: RegisterForm, request: Request, db: Session = Depends(get_db)):
    record = UserRegisterModel( username=register_form.username,
                                password=get_password_hash(register_form.password),
                                email=register_form.email)
    db.add(record)
    db.commit()
    token = create_access_token(data={'username':register_form.username})
    # TODO: delete old records in async mode
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
def refresh_token(  refresh_token: RefreshToken,
                    db: Session = Depends(get_db)):
    username = decode_refresh_token(refresh_token, db=db)
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "expire": ACCESS_TOKEN_EXPIRE_MINUTES*60,
            "token_type": "bearer"}

@user_router.get('/v2.0.0/users/validate_email/{token}', status_code=200)
def validate_email(token: str, db: Session = Depends(get_db)):
    if (username:=decode_token(token)) is not None:
        if (record:=db.query(UserRegisterModel).filter_by(username=username, is_deleted=False)\
            .one_or_none()) is not None:
            user = UserModel(   username=username,
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