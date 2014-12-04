from flask_wtf.file import FileField
from wtforms import Form, StringField, PasswordField

class UploadPhotoForm(Form):
    photo = FileField('Your photo')
    tags = StringField('tags')
    
class LoginForm(Form):
    name = StringField('username')
    password = PasswordField('password')
