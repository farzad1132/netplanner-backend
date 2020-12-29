from database import session
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import UserModel
from typing import Optional

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def auth_user(user_id: str, db: Session = Depends(get_db)):
    if (user:=UserModel.query.filter_by(id=user_id).one_or_none()) is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user