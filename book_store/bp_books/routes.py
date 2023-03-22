from flask import render_template, redirect, url_for, flash, Blueprint
from .util import save_picture
from .. import db
from .models import Book
from .forms import AddBookForm
#add: import form 
#add: import models


bp_books = Blueprint('bp_books', __name__)


@bp_books.route("/books")
def books():
    books_dict = Book.query.all()
    return render_template("books.html", title="books",  books=books_dict)  #books.html handles books_dict == None or books_dict empty




@bp_books.route("/add_book", methods=['POST', 'GET'])
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
            return redirect(url_for('bp_main.home'))
        except:
            flash(f'This book could not be added.. maybe it is already in database?', 'danger')
    return render_template("add_book.html", title="Add Book", form=form)
