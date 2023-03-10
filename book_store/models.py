from . import db, app
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin): #flask expects certain attributes and methods in our model (4): is_authenticated , is_active, is_anonymous, get_id. we could add them ourselves, but easier is inheriting from flask_login class UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  #add default later, will be hashed
    password = db.Column(db.String(60), nullable=False) #will be hashed
    #user created on.... 
    #purchase = db.relationship('Post', backref='author', lazy=True)  #note: this is a relationship, not a column! uppercase Post because we are referencing the class!
    #wishlist = ... 

    def __repr__(self): #similar to __str__, for development purposes
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    


#class book

#class sales (userid, bookid, date)

#class wishlist (userid, bookid)

    
with app.app_context():  #found in comment section of corey shafer part 6
    db.create_all()