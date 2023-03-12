from flask import Flask, render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm, AddBookForm
from . import app,db
from .models import Book
import secrets #used for generating a new name for profile pictures
import os #used for checking the file extension (jpg , ...) of new profile pictures
from PIL import Image #PIL is pillow, used for resizing profile pictures (pip install Pillow)

#dummy data for books (development): 
"""
books_dict = [   
    {'author':'Umberto Eco',
     'title': "De naam van de roos",
    'description' : "Brilliante detectivethriller uit de middeleeuwen"},
    {'author': "Gabrial Garcia Marquez",
     "title": "Honderd jaar eenzaamheid",
     'description': "Magisch realisme in een fictief zuid amerikaans land"},
    {'author': 'Hendrik Consience',
     'title':'De leeuw van Vlaanderen',
     'description': 'Klassieker over de guldensporenslag'} 
]
"""

books_dict = Book.query.all()





@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/test")  #development only!!!
@app.route("/")
def test():
    return render_template("test.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/books")
def books():
    return render_template("books.html", title="books",  books=books_dict)  #books.html handles books_dict == None or books_dict empty


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created! You are now able to log in!', 'success')
        return redirect(url_for('login'))   #we can change this: automaticaly login and redirect to home? 
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # finish later... 
        flash('Login Succesfull!')
        pass
    else:
        flash('Login unsuccesful... Please check login/password!')
    return render_template("login.html", title = "Login", form=form)



#handles the logic of saving a picture
def save_picture(form_picture):  #needs more try/except... 
    #first generate a random name, using secrets module
    random_hex = secrets.token_hex(8)
    #make sure we save the file with the same extension as it is uploaded
    #so check which extension it is... 
    _f_name, f_ext = os.path.splitext(form_picture.filename)  #path.splitext return two things, we only use f_ext
    #concat random hex and file extension for new filename
    picture_fn = random_hex + f_ext
    #form path where picture file will be saved
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    #resize the image using PIP (Pillows)
    output_size = (125,125)  #nice thing to put in a config file
    i = Image.open(form_picture)
    i.thumbnail(output_size)  
    #save image: 
    i.save(picture_path)
    #nice possible addition: delete the previous image
    return picture_fn  #return filename to store in db

@app.route("/add_book", methods=['POST', 'GET'])
def add_book():
    form = AddBookForm()   
    if form.validate_on_submit():
        #try and except to handle possible errors (like the unique constraint author+title: crashes the app)
        try: 
            book = Book()
            #handles pictures.. not a required field so we need if-clause
            if form.picture.data:
                picture_file = save_picture(form.picture.data)  #save picture saves the image and returns name
                book.image_file = picture_file                
            book.title = form.title.data
            book.author = form.author.data
            book.description = form.description.data
            db.session.add(book)
            db.session.commit()
            flash(f'This book has been added!', 'success')            
            return redirect(url_for('home'))
        except:
            flash(f'This book could not be added.. maybe it is already in database?', 'danger')
    return render_template("add_book.html", title="Add Book", form=form)
