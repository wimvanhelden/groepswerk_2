from .. import db, login_manager
from flask_login import UserMixin
from datetime import datetime



#function for reloading the user stored in user session, need this for the app to work, because the function has to know how to find a user by id
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))  
    except Exception as e:
        print(e)
        return None


wishlist = db.Table('wishlist', 
                    db.Column("userId", db.Integer, db.ForeignKey('user.id')),
                    db.Column("bookId", db.Integer, db.ForeignKey('book.id')),
                    db.Column("date_created", db.DateTime, nullable=False, default=datetime.utcnow))

purchases = db.Table('purchases', 
                     db.Column("userId", db.Integer, db.ForeignKey('user.id')),
                    db.Column("bookId", db.Integer, db.ForeignKey('book.id')),
                    db.Column("date_created", db.DateTime, nullable=False, default=datetime.utcnow))


class User(db.Model, UserMixin): #flask expects certain attributes and methods in our model (4): is_authenticated , is_active, is_anonymous, get_id. we could add them ourselves, but easier is inheriting from flask_login class UserMixin
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    
    password = db.Column(db.String(60), nullable=False) 
    date_created =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #not datetime.utcnow()! always use UTC time when saving times in database
    purchases = db.relationship("Book", secondary= purchases, back_populates = "purchases")
    wishlist = db.relationship("Book", secondary= wishlist, back_populates = "wishlist")
    type = db.Column(db.Integer, default = 1)  # normal user: type=1, admin user: type = 2

    # possible add_on: last_login_timestamp.. 
    def __repr__(self): #similar to __str__, for development purposes
        return f"User('{self.username}', '{self.email}', '{self.type}')"

    
