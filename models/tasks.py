""" some photo tasks which are handled asynchronously by celery """

from celery import Celery
celeryapp = Celery('photos', broker='amqp://guest@localhost//')

import os
from datetime import datetime
from utils import get_photo_fname, assert_photo_exists, get_photo
from geotagreader import GeoTagReader
from db import Photo, Tag, PhotoTag, session
from sqlalchemy.exc import IntegrityError

# uploads Photo image to file system
@celeryapp.task
def upload_image(photo_id, img_data, photo_ext):
    photo_fname = get_photo_fname(photo_id, photo_ext)
    f = open(photo_fname, "w")
    f.write(img_data)
    f.close()
    assert os.path.isfile(photo_fname)
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
