from flask import render_template, redirect, url_for, flash, Blueprint
from .forms import RegistrationForm, LoginForm
#add: import model user


bp_users = Blueprint('bp_users', __name__)

@bp_users.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created! You are now able to log in!', 'success')
        return redirect(url_for('bp_users.login'))   #we can change this: automaticaly login and redirect to home? 
    return render_template("register.html", title="Register", form=form)


@bp_users.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # finish later... 
        flash('Login Succesfull!')
        pass
    else:
        flash('Login unsuccesful... Please check login/password!')
    return render_template("login.html", title = "Login", form=form)
