from fastapi import APIRouter, Depends, HTTPException, Request, Query
from users.schemas import RegisterForm, Token, UserSearch, User
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import (ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, auth_user,
 get_password_hash, get_db, decode_token, get_current_user)
from datetime import timedelta
from starlette.responses import RedirectResponse
from users.utils import send_mail
from users.models import UserRegisterModel
from sqlalchemy.orm import Session
from models import UserModel
from typing import List

user_router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@user_router.post('/register', status_code=200)
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

@user_router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                            db: Session = Depends(get_db)):
    user = auth_user(form_data.username, form_data.password, db=db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get('/validate_email/{token}', status_code=200)
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

@user_router.get('/search_for_users', status_code=200, response_model=List[UserSearch])
def search_user(search_string: str = Query(..., min_length=3),
                db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    results = db.query(UserModel)\
        .filter(UserModel.username.contains(search_string))\
        .filter_by(is_deleted=False).all()
    return results