
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired,Email
from werkzeug.utils import secure_filename


class Register(FlaskForm):
    username = StringField('Username',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired())
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo('password',message='Passwords donr match')])
    firstname = StringField('Firstname',validators=[InputRequired())
    lastname = StringField('Lastname',validators=[InputRequired()])
    email = StringField('Email',validators=[InputRequired())
    location = StringField('Location',validators=[InputRequired())
    biography = TextAreaField('Biography')
    photo= FileField("photo",validators=[FileRequired,FileAllowed(['jpg','png','jpeg','Images only!'])])    
    submit = SubmitField("Register")

class LoginIn(FlaskForm):
    username = StringField('Username',validators=[InputRequired())
    password = PasswordField('Password',validators=[InputRequired())
    
class Post(FlaskForm):
    photo = FileField("Photo",validators = [FileRequired(),FileAllowed(['jpg','png','jpeg'])])
    caption = TextAreaField('Caption')

