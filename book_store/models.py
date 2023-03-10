from . import db, app
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin): #flask expects certain attributes and methods in our model (4): is_authenticated , is_active, is_anonymous, get_id. we could add them ourselves, but easier is inheriting from flask_login class UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(60), nullable=False) #will be hashed
    date_created =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #not datetime.utcnow()! always use UTC time when saving times in databas
    #purchase = db.relationship('Post', backref='author', lazy=True)  #wij hebben n op n relaties, nog bekijken of dat ook gaat werken
    #wishlist = ... 

    def __repr__(self): #similar to __str__, for development purposes
        return f"User('{self.username}', '{self.email}')"
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(30), nullable=False)  #dit kan ook met linktabel.. of eenvoudiger.. 
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  #add default later, will be hashed
    categorie = db.Column(db.String(20))  #dit kan ook met linktabel.. of eenvoudiger.. 
    db.UniqueConstraint('title', 'author', name='uix_title_author')


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), unique=True, nullable=False)

#class sales (userid, bookid, date)

#class wishlist (userid, bookid)

#class book-language (bookid, languageid)

db.create_all()  #can this line stay in, or will this overwrite data??
print('database created')
"""
with app.app_context():  #found in comment section of corey shafer part 6
    db.create_all()
"""