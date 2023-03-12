from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileField, FileAllowed  #ths is used for the book picture


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    

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
    #type = StringField('Type', validators = [DataRequired()])
    type = SelectField("Type", choices=['', 'hardcover', 'ebook', 'audiobook'] )
    category = SelectField("Category", choices=['', 'adventure', 'romance', 'horror', 'science fiction','nonfiction'] )
    price = FloatField('Price', validators=[NumberRange(min=0, message='Price has to be positive')])
    description = TextAreaField('Description')
    picture = FileField('Add book picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Book')

    


