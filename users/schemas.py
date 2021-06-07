"""
    This module contains user related schemas
"""

from pydantic import BaseModel, validator
from typing import Optional, List
from models import UserModel
from database import session

class Token(BaseModel):
    """
        Token schema (used at login)
    """
    access_token: str
    refresh_token: str
    expire: int
    token_type: str

class RefreshToken(BaseModel):
    """
        Refresh Token schema
    """

    refresh_token: str

class TokenData(BaseModel):
    """
        This schema represents data included in token
    """

    username: Optional[str] = None

class RegisterForm(BaseModel):
    """
        User Registration Form schema
        contains three validations:
        
         * username must be unique
         * confirm_password must be equal to password
         * email must be correct
    """

    username: str
    password: str
    confirm_password: str
    email: str

    @validator('username')
    def validate_username(cls, v):
        db = session()
        if db.query(UserModel).filter_by(username=v).one_or_none() is not None:
            db.close()
            raise ValueError('another user exist with this username')
        db.close()
        return v

    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if v != values['password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        db = session()
        if db.query(UserModel).filter_by(email=v).one_or_none() is not None:
            db.close()
            raise ValueError('another user exist with this email address')
        db.close()
        if  not '@' in v:
            raise ValueError('wrong email format')
        # TODO: uncomment block below
        """ account_domain = v.split('@')
        if account_domain[1] != 'sinacomsys.com':
            raise ValueError('wrong email domain') """
        return v

class User(BaseModel):
    """
        User Object schema
    """

    username: str
    id: str
    role: str

    class Config:
        orm_mode = True

class UserSearch(BaseModel):
    """
        User Search query schema
    """
    username: str
    id: str

    class Config:
        orm_mode = True