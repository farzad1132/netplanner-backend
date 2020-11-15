from flask import abort, request
from models import UserModel
import json
from config import db, bcrypt, app
import time
import six
from werkzeug.exceptions import Unauthorized
from jose import JWTError, jwt

JWT_SECRET = app.config.get("SECRET_KEY")
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'
JWT_ISSUER = 'sina.netplanner.flask'

def login(username, password):
    User = UserModel.query.filter_by(username= username).one_or_none()
    if User is None:
        return 404
    elif not bcrypt.check_password_hash(User.password, password):
        return 401
    else:
        return {"user_id": User.id, "token": generate_token(User.id)}, 200

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm= JWT_ALGORITHM)


def _current_timestamp() -> int:
    return int(time.time())