""" views which are accessible only to viewers """

from flask import Blueprint, render_template, redirect, session, request, url_for
from flask.ext.login import login_required, login_user, current_user, logout_user

viewer = Blueprint('viewer', __name__, url_prefix='/viewer')

from forms import SearchForm

""" home page for viewers
	displays: log out link, upload form, search form
"""
@viewer.route('/')
def index():
    search_form = SearchForm(request.form)
    return render_template('index.html', search_form=search_form)