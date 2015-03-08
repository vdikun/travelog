from flask_wtf.file import FileField, FileRequired, FileAllowed
#from wtforms.fields import FileField
from wtforms import Form, StringField, PasswordField, DateField, FloatField
from wtforms.validators import ValidationError
from config import ALLOWED_EXTENSIONS
import os

from customfields import TagListField

class UploadPhotoForm(Form):

    photo = FileField('photo', [FileRequired("Where is the file!!"), FileAllowed(['jpg'], 'JPG images only')])
    tags = StringField('tags')

    def allowed_filename(form, field):
        #"""
	print "field: ", field
	print "form: ", form
	print "field.data: ", field.data
        if field.data:
            filename = field.data.filename
            ext = filename.rsplit(".")[-1]
            if not ext.upper() in ALLOWED_EXTENSIONS:
                raise ValidationError('Has to be an image')
        else:
            raise ValidationError('Please, provide an image')
        #"""
        """
        try:
            filename = field.data.filename
            ext = filename.rsplit(".",1)[1]
            if not ext.upper() in ALLOWED_IMG_EXT:
                raise ValidationError('Has to be an image')
        except:
            raise ValidationError('Please, provide an image')
        """
        """
        if field.file:
            filename=field.file.name.upper()
            if not ('.' in filename and filename.rsplit('.',1)[1] in ALLOWED_IMG_EXT):
                raise ValidationError('Wrong Filetype, you can upload only %s files' % ALLOWED_IMG_EXT)
        else:
            raise ValidationError('field not Present')
        """

class SearchForm(Form):
    tags = StringField('tags')
    startdate = DateField('start')
    enddate = DateField('end')
    lat = FloatField('latitude')
    lon = FloatField('longitude')
    radius = FloatField('radius')
    
class LoginForm(Form):
    name = StringField('username')
    password = PasswordField('password')
    
class MakeViewersForm(Form):
    emails = TagListField('emails')
    password = StringField('password')
