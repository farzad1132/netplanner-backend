from flask import abort, request
from models import UserModel, ProjectModel
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

def register_designer():

def search_user():

def add_designer_to_project(body, user_id):
    if (user:=UserModel.query.filter_by(user_id= user_id).one_or_none()) is None:
        return {"error_msg": "user not found"}, 404
    elif user.role != "manager":
        return {"error_msg": "user not authorized"}, 401

    if (project_id:=body["project"]) is None:
        return {"error_msg": "project_id can not be None"}, 400
    
    if (id_list:=body["id_list"]) is None:
        return {"error_msg": "id_list can not be None"}, 400
    
    if (project:=db.session.query(ProjectModel).filter_by(user_id=user_id, id=project_id).one_or_none()) is None:
        return {"error_msg": "project not found"}, 404
    
    for id in id_list:
        if db.session.query(UserModel).filter_by(id=id).one_or_none() is None:
            return {"error_msg": f"user with id={id} not found from id_list"}, 404
        # complete here

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