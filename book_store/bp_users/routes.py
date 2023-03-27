from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .. import bcrypt, db
from .models import User
from .user_controller import send_reset_email



bp_users = Blueprint('bp_users', __name__)

"""
#function for sending reset emails:
def send_reset_email(user):

    import smtplib as smtp
    import time
    from ..config import Config
    import jwt

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

    message = f"to reset password go to the following link {token} {url_for('bp_users.reset_token', token=token,_external=True)}"
    message = f"to reset password go to the following link {url_for('bp_users.register')}"
 
    connection.login(email_addr, email_passwd)
    connection.sendmail(from_addr=email_addr, to_addrs=user.email, msg=message)
    connection.close()

"""

#route for register:
@bp_users.route("/register", methods=["GET", "POST"])
def register():
    #if user is already logged in: redirect to home-page
    if current_user.is_authenticated:
        flash('you can not create a new account when you are already logged in', 'danger')
        return redirect(url_for('bp_main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #validating if a username and password are new (unique) happens in "models"
        #first hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #now create the user instance
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('bp_users.login'))
    return render_template("register.html", title="Registration", form=form)


#route for login
@bp_users.route("/login", methods = ["GET", "POST"])
def login():
    #if user is already logged in: redirect to home-page
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #query the database to see if user exists: 
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #check that user exists, and that password is valid
            #login user, with "remember me" function if checked
            login_user(user, remember=form.remember.data)
            #check if user tried to acces a page that required login (like account page) 
            #if so: direct him there after login in (instead of the home page
            next_page = request.args.get('next') #returns none is page doest exist
            #redirect to next page, or homepage
            return redirect(next_page) if next_page else redirect(url_for('bp_main.home'))
        else: 
            flash('login unsuccesfull! please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)


#route for logout
@bp_users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('bp_main.home'))




#route for request reset passwourd
@bp_users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #if user is already logged in: redirect to home-page
    if current_user.is_authenticated:
        flash('You can not ask for password reset when already logged in', 'danger')
        return redirect(url_for('bp_main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        send_reset_email(user)
        flash('An email has been sent to you with instructions to reset your password', 'info')
        return redirect(url_for("bp_users.login"))
        
    return render_template("reset_request.html", title="Reset Password", form=form)


#route for password reset: enter new password
@bp_users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #if user is already logged in: redirect to home-page
    if current_user.is_authenticated:
        flash('You can not ask for password reset when already logged in', 'danger')
        return redirect(url_for('bp_main.home'))
    #try to verify (find) user by token:
    user = User.verify_reset_token(token)
    #if user is none: message token is invalid and redirect to "reset_request" page
    if user is None: 
        flash('Token is invalid or expired...', 'warning')
        return redirect(url_for('bp_users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = form.password.data
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('bp_users.login'))
    return render_template("reset_token.html", title="Reset Password", form=form)