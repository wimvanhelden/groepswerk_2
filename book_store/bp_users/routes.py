from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .. import bcrypt, db
from .models import User, purchases
from .user_controller import send_reset_email, verify_reset_token
from ..bp_books.models import Book



# initiate Blueprint
bp_users = Blueprint('bp_users', __name__)


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
    user = verify_reset_token(token)
    #if user is none: message token is invalid and redirect to "reset_request" page
    if user is None: 
        flash('Token is invalid or expired...', 'warning')
        return redirect(url_for('bp_users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # put this in password "setter" later
        
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('bp_users.login'))
    return render_template("reset_token.html", title="Reset Password", form=form)



#route for adding a book to WISHLIST
@bp_users.route("/add_wishlist/<book_id>", methods=['GET', 'POST'])
def add_wishlist(book_id):
    if current_user.is_authenticated: # change this later
        book_to_add = Book.query.get_or_404(book_id)
        current_user.wishlist.append(book_to_add)
        db.session.commit()
        flash(f'book is added to wishlist', 'success')
        return redirect(url_for('bp_main.home'))
    

#route for PURCHASING a book
@bp_users.route("/purchase/<book_id>", methods=['GET', 'POST'])
def purchase(book_id):
   if current_user.is_authenticated:# change this later
        book_to_add = Book.query.get_or_404(book_id)
        current_user.purchases.append(book_to_add,)
        db.session.commit()
        flash(f'thank you for your purchase!', 'success')
        return redirect(url_for('bp_main.home'))
   

#route foor "WISHLIST": page with overview of all the books in the user wishlist
# add: user has to be logged in
@bp_users.route("/wishlist/<user_id>")
def show_wishlist(user_id):
    user_wishlist = User.query.get_or_404(user_id)
    books_dict = user_wishlist.wishlist
    return render_template("wishlist.html", title="wishlist",  books=books_dict, user = user_wishlist)  #wishlist.html handles books_dict == None or books_dict empty


    

