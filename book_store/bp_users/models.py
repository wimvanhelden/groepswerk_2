from .. import db, app
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin): #flask expects certain attributes and methods in our model (4): is_authenticated , is_active, is_anonymous, get_id. we could add them ourselves, but easier is inheriting from flask_login class UserMixin
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(60), nullable=False) #will be hashed
    date_created =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #not datetime.utcnow()! always use UTC time when saving times in databas
    #purchase = db.relationship('Post', backref='author', lazy=True)  #wij hebben n op n relaties, nog bekijken of dat ook gaat werken
    #wishlist = ... 
    #categorie... 
    def __repr__(self): #similar to __str__, for development purposes
        return f"User('{self.username}', '{self.email}')"
    



    
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), unique=True, nullable=False)