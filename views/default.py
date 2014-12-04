# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, session, request, flash, url_for
from flask.ext.login import login_required, login_user, current_user, logout_user

# domain specific
from forms import UploadPhotoForm, LoginForm
from models.photo import load_photo, load_all_photos
from models.user import authenticate_user
from api import PhotoList

default = Blueprint('default', __name__, url_prefix='')

""" home page """
""" GET: see all photos 
    if logged in, see log out link & upload form.
    else, see log in form.
"""
@default.route('/')
def index():
    photos = load_all_photos()
    upload_form = UploadPhotoForm()
    login_form = LoginForm()
    return render_template('index.html', photos=photos, upload_form=upload_form, login_form=login_form)

""" photo """
""" GET: see photo w/ tags, metadata 
"""
@default.route('/photo/<photo_id>')
def show_photo(photo_id):
    photo = load_photo(photo_id)
    return render_template('show_photo.html', photo=photo)

""" search """
""" GET: see search form
    POST: see search form and search results
"""
@default.route('/search', methods=['GET', 'POST'])
def search_photo():
    return 404

""" login """
""" POST: if successful, user is now logged in 
    redirect to home page
"""
@default.route('/login', methods=['POST'])
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
@default.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('default.index'))
    
""" upload """
""" POST: if successful, new photo is created
    redirect to new photo page
"""
@default.route('/upload', methods=['POST'])
#@login_required
def upload_photo_view():
    form = UploadPhotoForm(request.form)
    if form.validate():
        # call API: POST to PhotoList
        # get photo ID from return
        ret = PhotoList.post()
        flash('uploaded photo.')
        photo = load_photo(ret['photo_id'])
        return url_for('default.show_photo', photo=photo)
    flash('invalid form.')
    return redirect(url_for('default.index'))
