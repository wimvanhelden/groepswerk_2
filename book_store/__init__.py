from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '22a742a01ab7bab950c22668922661b5'  #maybe we should put this in a config file? 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.app_context().push()  #deze lijn staat niet op youtube tutorial... was bij mij nodig om de database te kunnen aanmaken vanuit cmd screen(minuut 18:30 video 4)
#de database word aangemaakt in een folder "instance", ik ga die handmatig verzetten naar main directory




from . import routes, models