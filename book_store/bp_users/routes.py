from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm
from .. import bcrypt, db
from .models import User



bp_users = Blueprint('bp_users', __name__)



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


@bp_users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('bp_main.home'))