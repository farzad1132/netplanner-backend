from flask import abort, request
from models import UserModel
import json
from config import db, bcrypt


def login(Username, Password):
    User = UserModel.query.filter_by(username= Username).one_or_none()
    if User is None:
        return 404
    elif not bcrypt.check_password_hash(User.password, Password):
        return 401
    else:
        return {"UserId": User.id}, 200