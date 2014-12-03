# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort, render_template, flash
from flask.ext.login import login_required
from sqlalchemy import *

# domain specific
from forms import UploadPhotoForm
from models import load_photo
from api import PhotoList

photo_bp = Blueprint('photo_bp', __name__, url_prefix='/photos')

@photo_bp.route('/<photo_id>', methods=['GET'])
def show_photo(photo_id):
    photo = load_photo(photo_id)
    return render_template('show_photo.html', photo=photo)

@photo_bp.route('/upload', methods=['POST'])
@login_required
def upload_photo_view():
    form = UploadPhotoForm(request.form)
    if form.validate():
        # call API: POST to PhotoList
        # get photo ID from return
        ret = PhotoList.post()
        flash('uploaded photo.')
        photo = load_photo(ret['photo_id'])
        return render_template('show_photo.html', photo=photo)
    flash('invalid form.')
