"""
    This module contains endpoint dependencies
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import session
from models import UserModel
from users.schemas import TokenData

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
PREFIX = "/api"

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=PREFIX + "/v2.0.0" + '/users/login')

def get_db() -> Session:
    """
        This is database dependency handler
    """

    db = session()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        This function checks whether a given password matches given hash or not
    """

    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
        This function generates hash for passwords
    """

    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
        This function creates access token

        .. important:: access tokens expire after 30 minutes
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
        This function generates refresh token

        .. important:: refresh tokens expire after 120 minutes
    """

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES*4)
    to_encode.update({  "exp": expire,
                        "refresh": True})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
    """
        This function checks authorization and if user has right to access returns its object

        .. note:: this function might raise `HTTPException` with code `401`
    """

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
    """
        This function decodes a given access token and retturns including username

        .. note:: this function might raise `HTTPException` with code `401`
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (username:=payload.get('username')) is None:
            return None
        return username
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

def decode_refresh_token(token: str, db: Session) -> str:
    """
        This function decodes a given refresh token and retturns including username

        .. note:: this function might raise `HTTPException` with code `401`
    """

    validation_exception = HTTPException(status_code=401,
                                detail='could not validate refresh token',
                                headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('refresh') is not True:
            raise validation_exception
        if (username:= payload.get('sub')) is None:
            raise validation_exception
        if db.query(UserModel).filter_by(username=username, is_deleted=False)\
            .one_or_none() is None:
            raise validation_exception
        return username
    except:
        raise validation_exception

def get_user(username: str, db: Session) -> UserModel:
    """
        This function finds a user object in database with given username
    """

    if (user:=db.query(UserModel).filter_by(username=username, is_deleted=False).one_or_none()):
        return user

def auth_user(username: str, password: str, db: Session) -> UserModel:
    """
        This function checks users login information

        .. note:: this function might raise `HTTPException` with code `401` or `404`
    """

    if (user:=get_user(username, db)) is None:
        raise HTTPException(status_code=404, detail='user not found')
    if not verify_password( plain_password=password,
                            hashed_password=user.password):
        raise HTTPException(status_code=401, detail='wrong username or password')
    return user
