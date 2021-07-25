"""
    This module contains user related utilities
"""

import datetime
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from celery_app import celeryapp
from database import session
from fastapi import HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm.session import Session

from models import UserModel
from users.models import UserRegisterModel
from users.schemas import RegisterForm, UserRole

PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
SERVER = 'il2.persiantools.net'

context = ssl.create_default_context()
file_loader = FileSystemLoader('static')
env = Environment(loader=file_loader)


class UserRepository:
    """
        This class implements user related queries
    """
    @staticmethod
    def add_user_register(username: str, password: str, email: str, db: Session) -> None:

        record = UserRegisterModel(username=username,
                                   password=password,
                                   email=email)

        db.add(record)
        db.commit()

    @staticmethod
    def add_user(username: str, password: str, email: str, db: Session,
                 old_record: Optional[UserRegisterModel], role: UserRole = UserRole.DESIGNER) -> None:

        if old_record is not None:
            db.delete(old_record)

        user = UserModel(username=username,
                         password=password,
                         email=email,
                         role=role.value)
        db.add(user)
        db.commit()

    @staticmethod
    def get_user_register(username: str, db: Session) -> UserRegisterModel:

        if (record := db.query(UserRegisterModel).filter_by(username=username)
                .one_or_none()) is None:
            raise HTTPException(404, detail="record not found")
        return record

    @staticmethod
    def search_for_user_by_username(substring: str, db: Session, is_deleted: bool = False) \
            -> List[UserModel]:

        results = db.query(UserModel)\
            .filter(UserModel.username.contains(substring))\
            .filter_by(is_deleted=is_deleted).all()

        return results

    @staticmethod
    def get_user_by_id(id: str, db: Session, is_deleted: bool = False) -> UserModel:

        if (user := db.query(UserModel).filter_by(id=id, is_deleted=is_deleted)
                .one_or_none()) is None:

            raise HTTPException(
                status_code=404,
                detail=f"user with id={id} not found from id_list"
            )
        
        return user


def send_mail(token: str, rcv_mail: str, request: Request) -> None:
    """
        This functions sends email to user, it usage is for confirmation and registration

        :param token: token that gets included in confirmation link
        :param rcv_mail: recipient email
        :param request: request object used by templating engine for creating HTML

        .. note:: This function might raise `HTTPException` with code 500
    """
    try:
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls(context=context)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        html = create_message(token, request)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email Confirmation"
        message["From"] = MAIL_USERNAME
        message["To"] = rcv_mail
        part1 = MIMEText(html, "html")
        message.attach(part1)
        server.sendmail(MAIL_USERNAME, rcv_mail, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())
    finally:
        server.quit()


def create_message(token: str, request: Request) -> bytes:
    """
        This function generates email including HTML

        :param token: token that gets included in confirmation link
        :param request: request object used by templating engine for creating HTML
    """
    url = request.url_for('validate_email', **{"token": token})
    template = env.get_template("confirm_email.html")
    message = template.render(url=url)
    return message


def clear_old_registers(mins: int = 1) -> None:
    """
        This task deletes unused UserRegister Models from database

        :param minutes: records older than this amount of time will be deleted
    """

    db = session()
    registers = db.query(UserRegisterModel).all()
    for record in registers:
        if record.create_date < datetime.datetime.utcnow() \
                - datetime.timedelta(seconds=mins*60):
            db.delete(record)
    db.commit()


def validate_user_register_form(form: RegisterForm) -> None:
    """
        This util validates user register forms
    """

    db = session()
    if db.query(UserRegisterModel).filter_by(username=form.username).one_or_none() is not None:
        raise HTTPException(409, detail="this username has been taken")

    if form.password != form.confirm_password:
        raise HTTPException(
            401, detail="confirm password does not match password")

    if db.query(UserRegisterModel).filter_by(email=form.email).one_or_none() is not None:
        raise HTTPException(409, detail="this email has been taken")
    db.close()
