"""
    This module contains user related utilities
"""

import smtplib, ssl, os
from fastapi import HTTPException
from fastapi import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
SERVER = 'il2.persiantools.net'

context = ssl.create_default_context()
file_loader = FileSystemLoader('static')
env = Environment(loader=file_loader)

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
    url = request.url_for('validate_email', **{"token":token})
    template = env.get_template("confirm_email.html")
    message = template.render(url=url)
    return message