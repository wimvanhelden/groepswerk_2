from .. import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  #type is hardcover, ebook of audiobook
    price = db.Column(db.Float)
    title = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(30), nullable=False)  #dit kan ook met linktabel.. of eenvoudiger.. 
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  #add default later, will be hashed
    category = db.Column(db.String(20))  #categorie example horror, drama...
    db.UniqueConstraint('title', 'author', name='uix_title_author')