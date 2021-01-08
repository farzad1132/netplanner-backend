from fastapi import APIRouter, Depends, HTTPException, Request
from users.schemas import RegisterForm
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, auth_user, get_password_hash, get_db, decode_token
from users.schemas import Token
from datetime import timedelta
from starlette.responses import RedirectResponse
from users.utils import send_mail
from users.models import UserRegisterModel
from sqlalchemy.orm import Session
from models import UserModel

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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get('/validate_email/{token}', status_code=200)
def validate_email(token: str, db: Session = Depends(get_db)):
    if (username:=decode_token(token)) is not None:
        if (record:=db.query(UserRegisterModel).filter_by(username=username)\
            .one_or_none()) is not None:
            user = UserModel(   username=username,
                                password=record.password,
                                email=record.email,
                                role='designer')
            db.add(user)
            db.commit()
            return RedirectResponse(url='http://192.168.7.22')