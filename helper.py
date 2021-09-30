from secret import MAIL_USERNAME
from flask_mail import Mail, Message
from models import db
import secrets


mail = Mail()

def connect_mail(app):
    mail.init_app(app)

def send_reset_email_to(user):
    msg = Message("Email Reset",
                    sender= MAIL_USERNAME,
                    recipients=[f"{user.email}"])
    url = 'http://localhost:5000/reset/' + create_save_token(user)
    msg.html = f"<p> To get a new password for your account, just click the button below.</p> <a href='{url}'> Reset Password</a>"
    mail.send(msg)

def create_save_token(user):
    token = user.username + secrets.token_urlsafe()
    user.token = token
    db.session.commit()

    return token
    

