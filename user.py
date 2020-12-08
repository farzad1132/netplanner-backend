from flask import abort, request
from models import UserModel, ProjectModel, UserSchema, ProjectUsersModel
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

def login(body):

    if (password:=body["password"]) is None:
        return {"error_msg":"'password' can not be none"}, 400
    
    if (username:=body["username"]) is None:
        return {"error_msg":"'username' can not be none"}, 400

    if (user:=UserModel.query.filter_by(username= username).one_or_none()) is None:
        return {"error_msg": "user not found"}, 404
    
    elif not bcrypt.check_password_hash(user.password, password):
        return {"wrong username or password"}, 404
    else:
        return {"user_id": user.id, "token": generate_token(user.id), 'role': user.role}, 200

#def register_designer():

def search_user(search_string):
# this method will search for users with given sub string (search_string)
    #
    # parameters:
    #   1. sub string for search (search_string)
    #
    # returns:
    #   1. username
    #   2. user id
    #   3. user role

    if (results:=db.session.query(UserModel)\
        .filter(UserModel.username.contains(search_string)).all()) is None:
        return {"error_msg": "no user found"}, 404
    else:
        schema = UserSchema(only=('username', 'id', 'role'), many=True)
        return schema.dump(results), 200


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