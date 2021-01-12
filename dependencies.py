from database import session
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import UserModel
from typing import Optional
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from users.schemas import TokenData

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if (user:=get_user(username=token_data.username, db=db)) is None:
        raise credentials_exception
    return user

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (username:=payload.get('username')) is None:
            return None
        return username
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_user(username: str, db: Session):
    #db = next(get_db())
    if (user:=db.query(UserModel).filter_by(username=username, is_deleted=False).one_or_none()):
        return user

def auth_user(username: str, password: str):
    if (user:=get_user(username, next(get_db()))) is None:
        raise HTTPException(status_code=404, detail='user not found')
    if not verify_password( plain_password=password,
                            hashed_password=user.password):
        raise HTTPException(status_code=401, detail='wrong username or password')
    return user