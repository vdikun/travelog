# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, session, request, flash, url_for
from flask.ext.login import login_required, login_user, current_user, logout_user

# domain specific
from forms import UploadPhotoForm, LoginForm, SearchForm, MakeViewersForm
from models.photo import load_photo, load_all_photos, get_photos
from models.user import authenticate_user, make_viewers, find_viewers
from api import PhotoList
from serveremail import email_new_viewers

import config

default = Blueprint('default', __name__, url_prefix='')

""" util functions """

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print "Error"
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

""" home page """
""" GET: see all photos 
    if logged in, see log out link & upload form.
    else, see log in form.
"""
@default.route('/')
def index():
    upload_form = UploadPhotoForm()
    login_form = LoginForm()
    search_form = SearchForm(request.form)
    """
    print "hello from search"
    if request.method == 'POST' and form.validate():
        print "start search!"
        photos = get_photos(form.tags.data, form.startdate.data, form.enddate.data)
    return render_template('search.html', form=form, photos=photos)
    """
    return render_template('index.html', upload_form=upload_form, login_form=login_form, search_form=search_form)

""" photo """
""" GET: see photo w/ tags, metadata 
"""
@default.route('/photo/<photo_id>')
def show_photo(photo_id):
    photo = load_photo(photo_id)
    return render_template('show_photo.html', photo=photo)
    
""" login """
""" POST: if successful, user is now logged in 
    redirect to home page
"""
@default.route('/login/', methods=['POST'])
def login():
    form = LoginForm(request.form)
    user = authenticate_user(form.name.data, form.password.data)
    if user is not None:
        login_user(user)
    else:
        flash("login error")
    return redirect(url_for('default.index'))

""" logout """
""" POST: if successful, user is now logged out
    redirect to home page
"""
@default.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('default.index'))

""" search """
""" POST: gets filtered photos from db
"""    
@default.route('/search/', methods=['GET', 'POST'])
def search():
    photos = []
    form = SearchForm(request.form)
    print "hello from search"
    if request.method == 'POST' and form.validate():
        print "start search!"
        photos = get_photos(form.tags.data, form.startdate.data, form.enddate.data)
    return render_template('search.html', form=form, photos=photos)

""" makeviewers """
""" POST: makes viewers in db
"""    
@default.route('/viewers/', methods=['GET', 'POST'])
def makeviewers():
    form = MakeViewersForm(request.form)
    if request.method == 'POST' and form.validate():
        make_viewers(current_user, form.emails.data, form.password.data)
        email_new_viewers(current_user, form.emails.data, form.password.data)
        form = MakeViewersForm()
    viewers = find_viewers(current_user)
    return render_template('viewers.html', form=form, viewers=viewers)

""" upload """
""" uses internal API """
""" TODO """
@default.route('/upload/', methods=['POST'])
@login_required
def upload():
    return None
