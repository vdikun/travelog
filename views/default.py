# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, session, request, url_for
from flask.ext.login import login_required, login_user, current_user, logout_user

# domain specific
from forms import LoginForm, SearchForm
from models.photo import load_all_photos, get_photos
from models.user import authenticate_user
import config

default = Blueprint('default', __name__, url_prefix='')

    
""" login """
""" POST: if successful, user is now logged in 
    redirect to home page
"""
@default.route('/login/', methods=['POST'])
def login():
    form = LoginForm(request.form)
    print "username: {0} && password: {1}".format(form.name.data, form.password.data)
    user = authenticate_user(form.name.data, form.password.data)
    if user is not None:
        print "logging in user"
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


""" home page
    different for different kinds of users
"""
@default.route('/')
def index():
    if not current_user.is_authenticated():
        # TODO display new account form
        form = LoginForm()
        return render_template('login.html', login_form=form)
    elif current_user.is_owner():
        return redirect(url_for('owner.index'))
    else:
        return redirect(url_for('viewer.index'))


""" search """
""" POST: gets filtered photos from db
"""    
@default.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    photos = []
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        photos = get_photos(current_user, form.tags.data, form.startdate.data, form.enddate.data)
    return render_template('search.html', form=form, photos=photos)


""" photo
    GET: see photo w/ tags, metadata
"""
@default.route('/photo/<photo_id>')
@login_required
def show_photo(photo_id):
    if not can_view_photo(current_user):
        raise AuthenticationError("You are not authorized to view this photo")
    photo = load_photo(photo_id)
    return render_template('show_photo.html', photo=photo)