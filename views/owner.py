""" views which are accessible only to owners """

from flask import Blueprint, render_template, redirect, session, request, url_for, jsonify
from flask.ext.login import login_required, login_user, current_user, logout_user

from forms import UploadPhotoForm, MakeViewersForm, SearchForm
from models.user import make_viewers, find_viewers
from models.photo import load_photo
from models.permissions import can_upload_photo
from serveremail import email_new_viewers
from utils import AuthenticationError

from functools import wraps

owner = Blueprint('owner', __name__, url_prefix='/owner')

def owner_required(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not current_user.is_owner():
            raise AuthenticationError("You must be logged in as an owner to access this view.")
        return f(*args, **kwds)
    return wrapper


""" home page for owners
	displays: log out link, upload form, search form
"""
@owner.route('/')
def index():
    upload_form = UploadPhotoForm()
    search_form = SearchForm(request.form)
    return render_template('index.html', upload_form=upload_form, search_form=search_form)


""" viewers
	GET: shows existing viewers and form
"""    
@owner.route('/viewers/', methods=['GET'])
@owner_required
def viewers():
    form = MakeViewersForm()
    viewers = find_viewers(current_user)
    return render_template('viewers.html', form=form, viewers=viewers)


""" makeviewers
    POST: creates new viewing accounts, redirects to GET
"""    
@owner.route('/viewers/', methods=['POST'])
@owner_required
def makeviewers():
    form = MakeViewersForm(request.form)
    if form.validate():
        make_viewers(current_user, form.emails.data, form.password.data)
        try:
            email_new_viewers(current_user, form.emails.data, form.password.data)
        except:
            flash("something went wrong. are you sure those emails are correct?")
    return viewers()


""" upload """
""" uses internal API """
""" TODO """
@owner.route('/upload/', methods=['POST'])
@owner_required
def upload():
    return None