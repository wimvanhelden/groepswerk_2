from functools import wraps
from flask import abort, url_for, Blueprint, current_app
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
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    email_addr = 'groepswerktwee@gmail.com'  #put this in seperate file later
    email_passwd = 'nzqxhmwdalwivadz'  #put this in seperate file later
    user_adress = user.email
    #generate token: 
    expiration_time = 900  #900 seconds is 15 minutes
    #get the app config key to encode the jwt: 
    key = Config.SECRET_KEY
    #set(encode) token:
    token = jwt.encode({'user_email':user_adress, 'user_id':user.id, 'exp':time()+expiration_time}, key, algorithm ="HS256"  )
    message = MIMEMultipart("alternative")
    message["Subject"] = "bookstore password reset"
    message["From"] = email_addr
    message["To"] = user_adress
    text = """\
    Bookstore password reset"""
    html = f"""\
    <html>
      <body>
        <p>Hi,<br>
           Please use this link to reset your password:<br>
           <a href={url_for('bp_users.reset_token', token=token, _external=True)}>reset password</a> <br>

           If you did not request a password reset, you can ignore this email. <br>
           Have a nice day! <br>
        </p>
      </body>
    </html>
    """    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtp.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_addr, email_passwd)
        server.sendmail(
            email_addr, user_adress, message.as_string()
        )







def verify_reset_token(token):

    try:
        key = Config.SECRET_KEY
        decoded_jwt = jwt.decode(token, key, algorithms=['HS256'])  
        print(decoded_jwt['user_id'])
        user_id = decoded_jwt['user_id']
        user = User.query.get(user_id)
        print(user.username)

    except:
        return None
    return User.query.get(user_id)