from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired,Email
from werkzeug.utils import secure_filename

class UploadForm(FlaskForm):
    Description = TextAreaField("Description", validators=[DataRequired()]),
    photo= FileField("photo",validators=[FileRequired,FileAllowed(['jpg','png','jpeg','Images only!'])])
