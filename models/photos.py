""" takes care of photo stuff on the server """
""" some tasks handled asynchronously by celery """

from flask import url_for
from db import Photo, Tag, PhotoTag, session
from datetime import datetime
import config
import os
from geotagreader import GeoTagReader
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError

from celery import Celery
celeryapp = Celery('photos', broker='amqp://guest@localhost//')

""" utility functions """

class NoSuchObjectException(Exception):
    pass
    
def get_photo_fname(photo_id, photo_ext):
    return config.IMG_DIR + str(photo_id) + "." + photo_ext
    
def get_photo(photo_id):
    assert_photo_exists(photo_id)
    return session.query(Photo).filter(Photo.id==photo_id).first()
    
def get_photo_tags(photo_id):
    query = session.query(Tag).filter(and_(PhotoTag.p_id==photo_id, PhotoTag.t_id==Tag.id))
    tags = [tag.text for tag in query]
    return tags
    
# asserts that the photo exists
def assert_photo_exists(id):
    if not photo_exists(id):
        raise NoSuchObjectException()

# returns true if id matches Photo object in database
def photo_exists(id):
    if session.query(Photo).filter(Photo.id==id).count() == 0:
        return False
    return True


""" functions that operate on photo objects """

# returns Photo object with added attributes: img_data, tags    
def load_photo(id):
    if not photo_exists(id): 
        return None
    photo = session.query(Photo).filter(Photo.id==id).first()
    photo_fname = get_photo_fname(id, photo.ext)
    photo.img_uri = url_for('static/img', filename="something.jpg")
    taglist = session.query(Tags).filter(PhotoTag.p_id==id)
    tags = []
    for tag in taglist:
        tags.append(tag.text)
    photo.tags = tags
    return photo

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

# called by API Photo POST request    
def process_new_photo(image_data, ext, tags):
    photo_id = new_photo_placeholder().id
    upload_image.delay(photo_id, image_data, ext)
    add_tags.delay(photo_id, tags)
    return photo_id

# uploads Photo image to file system
@celeryapp.task
def upload_image(photo_id, img_data, photo_ext):
    photo_fname = get_photo_fname(photo_id, photo_ext)
    f = open(photo_fname, "w")
    f.write(img_data)
    f.close()
    date_uploaded = datetime.now()
    update_photo_metadata.delay(photo_id, photo_ext, date_uploaded)
    
# updates metadata of Photo object in db
@celeryapp.task
def update_photo_metadata(photo_id, photo_ext, date_uploaded):
    photo_fname = get_photo_fname(photo_id, photo_ext)
    # read metadata: geolocation, date created
    gtr = GeoTagReader(photo_fname)
    lat = gtr.get_lat()                   # float
    lon = gtr.get_lon()                   # float
    date_created = gtr.get_date_created() # datetime object
    # set values on Photo object
    photo = get_photo(photo_id)
    photo.ext = photo_ext
    photo.lat = lat
    photo.lon = lon
    photo.date_created = date_created
    photo.date_uploaded = date_uploaded
    photo.uploaded = 1
    assert photo in session
    session.commit()

# adds tags to Photo object in db
@celeryapp.task
def add_tags(photo_id, tags):
    assert_photo_exists(photo_id)
    for tag in tags:
        # make a new Tag object and store it
        tagObject = Tag(text=tag)
        try:
            session.add(tagObject)
            session.commit()
        except IntegrityError:
            # this Tag object probably exists already
            print "could not add tag with text '%s'" % tag
            session.rollback()
        # then make a PhotoTag object and store it
        tagObject = session.query(Tag).filter(Tag.text==tag).first()
        photoTag = PhotoTag(p_id = photo_id, t_id = tagObject.id)
        try:
            session.add(photoTag)
            session.commit()
        except IntegrityError:
            # duplicate PhotoTag, probably
            print "could not tag photo %i with '%s'" % (photo_id, tag)
            session.rollback()
