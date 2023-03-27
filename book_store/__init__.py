from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



db = SQLAlchemy()
bcrypt = Bcrypt()  #this handles encrypting passwords
login_manager = LoginManager()  #this handles sessions
login_manager.login_view = 'bp_users.login'  #this line is for letting "login_required" know where the login is
login_manager.login_message_category = 'info'  #a nicer flash message for login
#app.app_context().push()  #deze lijn staat niet op youtube tutorial... was bij mij nodig om de database te kunnen aanmaken vanuit cmd screen(minuut 18:30 video 4)
#de database word aangemaakt in een folder "instance", ik ga die handmatig verzetten naar main directory

#move to factory later... 




def create_app(config_class=Config):
    app = Flask(__name__)
    #import configuration from config.py
    app.config.from_object(Config)
    #connect our initiations to the app: 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    #mail.init_app(app)
    #import and register blueprints
    from .bp_users.routes import bp_users
    app.register_blueprint(bp_users)
    from .bp_books.routes import bp_books
    app.register_blueprint(bp_books)
    from .bp_main.routes import bp_main
    app.register_blueprint(bp_main)
    return app