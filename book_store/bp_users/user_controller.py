from functools import wraps
from flask import abort, url_for, Blueprint
from flask_login import current_user
from .models import User
import jwt
from time import time
from ..config import Config


def only_admins(func):
    @wraps(func)
    def is_allowed(*args, **kwargs):
        cu = current_user
        if cu is not None and cu.profile_type == 0:
            return func(*args, **kwargs)
        else:
            abort(403)
    return is_allowed



#function for sending reset emails:
def send_reset_email(user):

    import smtplib as smtp

    connection = smtp.SMTP_SSL('smtp.gmail.com', 465)
    
    email_addr = 'groepswerktwee@gmail.com'  #put this in seperate file later
    email_passwd = 'nzqxhmwdalwivadz'  #put this in seperate file later
    user_adress = user.email
    #generate token: 
    expiration_time = 900  #900 seconds is 15 minutes
    #get the app config key to encode the jwt: 
    key = Config.SECRET_KEY
    #set(encode) token:
    token = jwt.encode({'user_email':user_adress, 'exp':time()+expiration_time}, key, algorithm ="HS256"  )

    message = f"to reset password go to the following link {url_for('bp_users.reset_token', token=token, _external=True)}"
    print(message)
    message2 = "testing testing"
 
    connection.login(email_addr, email_passwd)
    connection.sendmail(from_addr=email_addr, to_addrs=user.email, msg=message)
    connection.close()


