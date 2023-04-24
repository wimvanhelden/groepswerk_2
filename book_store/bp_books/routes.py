from flask import render_template, redirect, url_for, flash, Blueprint, request
from .util import save_picture
from .. import db
from .models import Book
from .forms import AddBookForm, UpdateBookForm
#add: import form 
#add: import models


bp_books = Blueprint('bp_books', __name__)

#route foor "books": page with overview of all the books
@bp_books.route("/books")
def books():
    books_dict = Book.query.all()
    return render_template("books.html", title="books",  books=books_dict)  #books.html handles books_dict == None or books_dict empty



#route ADD BOOK 
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
            book.price = form.price.data
            book.type = form.type.data
            book.category = form.category.data
            db.session.add(book)
            db.session.commit()
            flash(f'This book has been added!', 'success')            
            return redirect(url_for('bp_main.home'))
        except:
            flash(f'This book could not be added.. maybe it is already in database?', 'danger')
    return render_template("add_book.html", title="Add Book", form=form)


#route for "book": page for individual books: 
@bp_books.route("/book/<book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)  #we use this method instead of get to handle errors
    return render_template('book.html', title=book.title, book=book)


#route for UPDATE BOOK
@bp_books.route("/update_book/<int:book_id>", methods=['POST', 'GET'])
def update_book(book_id):
    form = UpdateBookForm()
    book = Book.query.get_or_404(book_id)
    if form.validate_on_submit():
        #try and except to handle possible errors (like the unique constraint author+title: crashes the app)
        try: 
            
            #handles pictures.. not a required field so we need if-clause
            if form.picture.data:
                picture_file = save_picture(form.picture.data)  #save picture saves the image and returns name
                book.image_file = picture_file                
            book.title = form.title.data
            book.author = form.author.data
            book.description = form.description.data
            book.price = form.price.data
            book.type = form.type.data
            book.category = form.category.data
            db.session.add(book)
            db.session.commit()
            flash(f'This book has been updated', 'success')            
            return redirect(url_for('bp_main.home'))
        except:
            flash(f'This book could not be updated.. maybe the title+author combination is already in database??', 'danger')
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.type.data = book.type
        form.category.data = book.category
        form.price.data = book.price
        form.description.data = book.description
        if book.image_file:
            form.picture.data = book.image_file

    return render_template("update_book.html", title="Update Book", form=form)

@bp_books.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    #add later: delete the book picture.... 
    flash('The book has been deleted!', 'success')
    return redirect(url_for('bp_main.home'))