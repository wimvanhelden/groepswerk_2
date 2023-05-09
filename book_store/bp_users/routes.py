from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from .. import bcrypt, db
from .models import User, purchases, wishlist
from .user_controller import send_reset_email, verify_reset_token, admin_required
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
    #create new form object:
    form = RegistrationForm()

    # try... except... to handle any database / connection issues
    try:
        #on submit: check if data is OK and try to write to database
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
    except: 
        flash('operation failed, check your connection', 'danger') 
        return redirect(url_for('bp_main.home'))
        
    return render_template("register.html", title="Registration", form=form)


#route for login
@bp_users.route("/login", methods = ["GET", "POST"])
def login():
    #if user is already logged in: redirect to home-page
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.home'))
    #create new form object:
    form = LoginForm()
    # try... except... to handle any database / connection issues
    try:
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
    except: 
        flash('operation failed, check your connection', 'danger') 

    return render_template("login.html", title="Login", form=form)


#route for logout
@login_required
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
        #user = User.query.filter_by(email=form.email.data).first()
        #send_reset_email(user)
        send_reset_email(form.email.data)
        flash('a link for password reset can be found in your cmd prompt screen (if that email adress is linked to an account)', 'info')
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
@bp_users.route("/add_wishlist/<book_id>")
def add_wishlist(book_id):
    try: 
        if current_user.is_authenticated: # change this later, try/except
            # add a check that book is not already in wishlist
            check_book = db.session.query(wishlist).filter_by(userId = current_user.id, bookId = book_id).first()
            print(check_book)  #DEBUG DELETE LATER
            if check_book is None:
                book_to_add = Book.query.get_or_404(book_id)
                current_user.wishlist.append(book_to_add)
                db.session.commit()
                flash(f'book is added to wishlist', 'success')
                return redirect(request.referrer)                
            else: 
                flash(f'book is already in wishlist!', 'danger')
                return redirect(url_for('bp_main.home'))
            
        #if user is not authenticatd:
        else: 
            flash(f'you need to be logged in to add a book to your wishlist', 'danger')
            return redirect(url_for('bp_users.login'))
    except: 
            flash(f'something went wrong... check your connection', 'danger')
            return redirect(url_for('bp_main.home'))


#route for deleting a book from WISHLIST
@login_required
@bp_users.route("/delete_wishlist/<book_id>")
def delete_wishlist(book_id):
    # try to find the id of the wishlist record by filtering on bookID and userID and delete it.... 
    try:
        db.session.query(wishlist).filter_by(userId = current_user.id, bookId = book_id).delete()
        db.session.commit()
        flash(f'book is deleted from wishlist', 'success')
        return redirect(request.referrer)                 
    except: 
        flash(f'book has not been deleted from wishlist', 'danger')
        return redirect(url_for('bp_main.home'))
              
 
#route for PURCHASING a book
@bp_users.route("/purchase/<book_id>", methods=['GET', 'POST'])
def purchase(book_id):
    try: 
        if current_user.is_authenticated:
                book_to_add = Book.query.get_or_404(book_id)
                current_user.purchases.append(book_to_add,)
                db.session.commit()
                flash(f'thank you for your purchase!', 'success')
                return redirect(url_for('bp_main.home'))
        else: 
            flash(f'you need to be logged in to purchase a book', 'danger')
            return redirect(url_for('bp_users.login'))
    except: 
        flash(f'something went wrong... check your connection', 'danger')
        return redirect(url_for('bp_main.home'))

   

#route for "WISHLIST": page with overview of all the books in the user wishlist
@login_required
@bp_users.route("/wishlist/<user_id>")
def show_wishlist(user_id):
    #check to make sure that user wants to see his own wishlist, or is admin
    if current_user.id == int(user_id) or current_user.type == 2:
        print(current_user.id)
        print("yes")
        user_wishlist = User.query.get_or_404(user_id)
        books_dict = user_wishlist.wishlist
        return render_template("wishlist.html", title="wishlist",  books=books_dict, user = user_wishlist)  #wishlist.html handles books_dict == None or books_dict empty
    else: 
        flash(f'you do not have permission to see this wishlist', 'danger')
        return redirect(url_for('bp_main.home'))



#route foor "ACCOUNT": page with overview of all the books in the user purchased in the past
@login_required
@bp_users.route("/account/<user_id>")
def show_account(user_id):
    if current_user.id == int(user_id) or current_user.type == 2:
        user_account = User.query.get_or_404(user_id)
        books_dict = user_account.purchases
        return render_template("account.html", title="account",  books=books_dict, user = user_account)  #account.html handles books_dict == None or books_dict empty
    else: 
        flash(f'you do not have permission to acces this account page', 'danger')
        return redirect(url_for('bp_main.home'))

    

#route for admin account to see al customers
@admin_required
@bp_users.route("/all_accounts")
def show_all_accounts():
    try: 
        all_users = User.query.all()
        return render_template("all_accounts.html", title="all accounts",  all_users = all_users)  #all_accounts.html handles books_dict == None or books_dict empty
    except: 
        flash(f'something went wrong... check your connection', 'danger')
        return redirect(url_for('bp_main.home'))
