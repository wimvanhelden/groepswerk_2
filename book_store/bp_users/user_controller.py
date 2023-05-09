from functools import wraps
from flask import abort, url_for, Blueprint, current_app, flash, redirect
from flask_login import current_user
from .models import User
import jwt
from time import time

from config_data import password_token


#custom wrapper @admin_required
def admin_required(f):
    @wraps(f)
    def wrapper_admin(*args, **kwargs):
        cu = current_user
        if cu is not None and cu.type == 2:
            return f(*args, **kwargs)
        else:
            flash(f'page is only accessbile for admins!', 'danger')
            return redirect(url_for('bp_main.home'))
    return wrapper_admin



#function for sending reset emails:
def send_reset_email(email_adress):
    try:
        #try to find a user with the email adress from the form input: 
        user_check = User.query.filter_by(email = email_adress).first()
        # if user exists: output reset link to cmd screen
        # (possible addition: email )
        if user_check is not None: 
            #generate token: 
            expiration_time = 900  #900 seconds is 15 minutes
            #get the app config key to encode the jwt: 
            key = password_token
            #set(encode) token:
            token = jwt.encode({'user_email':email_adress, 'user_id':user_check.id, 'exp':time()+expiration_time}, key, algorithm ="HS256"  )
            print({url_for('bp_users.reset_token', token=token, _external=True)})
    except Exception as e:
        print(e)



def verify_reset_token(token):
    try:
        key = password_token
        decoded_jwt = jwt.decode(token, key, algorithms=['HS256'])  
        print(decoded_jwt['user_id'])
        user_id = decoded_jwt['user_id']
        user = User.query.get(user_id)
        if user is not None: 
            return User.query.get(user_id)
    except:
        return None
    return User.query.get(user_id)