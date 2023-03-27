from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .models import User


    

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):  #validate_fieldname is soort magic function in wtforms, word automatisch aangeroepen
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError("username already exists, please pick a different one")
        
    def validate_email(self, email):   #validate_fieldname is soort magic function in wtforms, word automatisch aangeroepen
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError("email already exists, please pick a different one")

class LoginForm(FlaskForm):
    #login happens with email, not username
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class RequestResetForm(FlaskForm):
        email = StringField('Email', 
                        validators=[DataRequired(), Email()])
        submit = SubmitField('Request Password Reset')
        #we run a check if the email exists: 
        def validate_email(self, email):   
            user = User.query.filter_by(email=email.data).first()
            if user is None: 
                raise ValidationError("There is no account with that email. Please register first.")
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
