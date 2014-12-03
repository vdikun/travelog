from flask_wtf.file import FileField
from wtforms import Form, StringField

class UploadPhotoForm(Form):
    photo = FileField('Your photo')
    tags = StringField('tags')
