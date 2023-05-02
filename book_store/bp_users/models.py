from .. import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import jwt



#function for reloading the user stored in user session, need this for the app to work, because the function has to know how to find a user by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  #does this need try except?


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
    password = db.Column(db.String(60), nullable=False) #will be hashed
    date_created =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #not datetime.utcnow()! always use UTC time when saving times in database
    purchases = db.relationship("Book", secondary= purchases, back_populates = "purchases")
    wishlist = db.relationship("Book", secondary= wishlist, back_populates = "wishlist")
    #categorie... 
    def __repr__(self): #similar to __str__, for development purposes
        return f"User('{self.username}', '{self.email}')"
    
    """
    def get_token(self, expiration_time=600): 
        return jwt.encode(‘something’: self.id, ‘exp’: time() + expires_in, secret_key, algorithm=’HS256’)
    """


"""
    def get_reset_token(self, expires_sec=3000):
        #create serializer object:
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        #return a token that is created by the dumps method, based on user_id:
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        #create serializer object:
        s = Serializer(current_app.config['SECRET_KEY'])
        #try getting the user_id from the token. this can fail, so we use try...except...
        try: 
            user_id = s.loads(token)['user_id]']
        except: 
            return None
        #if we find a user_id in token: return the user with that user_id
        return User.query.get(user_id)
"""
    
