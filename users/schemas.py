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