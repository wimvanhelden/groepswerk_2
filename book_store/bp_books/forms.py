from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed  #ths is used for the book picture



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


class UpdateBookForm(FlaskForm):
        
    title = StringField('Title', validators = [DataRequired()])
    author = StringField('Author', validators = [DataRequired()])
    #type = StringField('Type', validators = [DataRequired()])
    type = SelectField("Type", choices=['', 'hardcover', 'ebook', 'audiobook'] )
    category = SelectField("Category", choices=['', 'adventure', 'romance', 'horror', 'science fiction','nonfiction'] )
    price = FloatField('Price', validators=[NumberRange(min=0, message='Price has to be positive')])
    description = TextAreaField('Description')
    picture = FileField('Update book picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Book')