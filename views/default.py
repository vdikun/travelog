# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

default = Blueprint('default', __name__, url_prefix='')

@default.route('/', methods=['GET'])
@default.route('/photos', methods=['GET'])
def show_photos():
    photos = [] # TODO
    return render_template('show_photos.html', photos=photos)
    
@default.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
    
@default.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')
