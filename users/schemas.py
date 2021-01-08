from pydantic import BaseModel, validator
from typing import Optional, List
from models import UserModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RegisterForm(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str

    @validator('username')
    def validate_username(cls, v):
        if UserModel.query.filter_by(username=v).one_or_none() is not None:
            raise ValueError('another user exist with this username')
        return v

    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if v != values['password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if UserModel.query.filter_by(email=v).one_or_none() is not None:
            raise ValueError('another user exist with this email address')
        if  not '@' in v:
            raise ValueError('wrong email format')
        # TODO: uncomment block below
        """ account_domain = v.split('@')
        if account_domain[1] != 'sinacomsys.com':
            raise ValueError('wrong email domain') """
        return v

class User(BaseModel):
    username: str
    id: str
    role: str

    class Config:
        orm_mode = True