import smtplib, ssl, os
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 587
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
SERVER = 'il2.persiantools.net'

templates = Jinja2Templates(directory='static')
context = ssl.create_default_context()

def send_mail(token: str, rcv_mail: str, request: Request):
    try:
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls(context=context)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        html = create_message(token, request)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email Confirmation"
        message["From"] = MAIL_USERNAME
        message["To"] = rcv_mail
        part1 = MIMEText(str(html.body), "html")
        #part2 = MIMEText("message", "plain")
        message.attach(part1)
        server.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__repr__())
    finally:
        server.quit()

def create_message(token: str, request: Request):
    url = request.url_for('validate_email', **{"token":token})
    message = templates.TemplateResponse("confirm_email.html", {"url": url, 'request': request})
    return message
    