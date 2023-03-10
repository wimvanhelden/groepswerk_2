from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed  #ths is used for the book picture

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    #login happens with email, not username
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddBookForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    author = StringField('Author', validators = [DataRequired()])
    description = TextAreaField('Description')
    picture = FileField('Add book picture', validators=[FileAllowed(['jpg', 'png'])])
    #picture = FileField('Add book picture', validators=[FileAllowed(['jpg', 'png'])])
    #add something later for the categorie
    submit = SubmitField('Add Book')


