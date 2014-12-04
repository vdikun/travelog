""" takes care of photo stuff on the server """

from flask import url_for
from db import Photo, Tag, PhotoTag, session
from datetime import datetime
import config
import os
from sqlalchemy.exc import IntegrityError

from utils import *

from tasks import add_tags, upload_image


""" functions that operate on photo objects """

# adds img_data, tags to Photo object
def marshal(photo):
    photo.img_uri = url_for('static', filename=static_photo_fname(photo.id, photo.ext))
    tags = get_photo_tags(photo.id)
    photo.tags = tags
    return photo

# returns Photo object with added attributes: img_data, tags    
def load_photo(id):
    if not photo_exists(id): 
        return None
    photo = get_photo(id)
    return marshal(photo)

# serializes Photo object to JSON    
def to_json(photo):
    photo_dict = dict()
    for k,v in photo.__dict__.iteritems():
        if not k.startswith('_'): # ignore private attributes
            photo_dict[k] = v
    return photo_dict

# returns JSON-serialized Photo object from id    
def load_photo_json(id):
    photo = load_photo(id)
    if not photo:
        return None
    return to_json(photo)

# makes placeholder Photo object, stores to db, returns Photo
def new_photo_placeholder():
    photo = Photo()
    session.add(photo)
    session.commit()
    return photo

# removes Photo from db and Photo image from file system    
def delete_photo(id):
    assert_photo_exists(id)
    photo = get_photo(id)
    ext = photo.ext
    # remove from db
    # phototags should get dropped automatically
    session.delete(photo) 
    session.commit()
    # remove from file system
    os.remove(get_photo_fname(id, ext))

# called by API Photo POST request, returns new Photo's id
def process_new_photo(image_data, ext, tags):
    photo_id = new_photo_placeholder().id
    upload_image.delay(photo_id, image_data, ext)
    add_tags.delay(photo_id, tags)
    return photo_id

# returns list of marshalled Photo objects
def load_all_photos():
    photos = session.query(Photo).filter(Photo.date_uploaded != None).all()
    photos.sort(key=lambda x: x.date_uploaded)
    return [marshal(photo) for photo in photos]
