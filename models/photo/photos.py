""" takes care of photo stuff on the server """

from db import Photo, Tag, PhotoTag, session
from datetime import datetime
import config
import os
from sqlalchemy.exc import IntegrityError
from geotagreader import GeoTagReader
from models.permissions import can_view_photo

from utils import *


""" functions that operate on photo objects """

""" assorted functions """

# returns JSON-serialized Photo object from id    
def load_photo_json(id):
    photo = load_photo(id)
    if not photo:
        return None
    return to_json(photo)
    
# asserts that the photo exists
def assert_photo_exists(id):
    if not photo_exists(id):
        raise NoSuchObjectException()

# returns true if id matches Photo object in database
def photo_exists(id):
    if session.query(Photo).filter(Photo.id==id).count() == 0:
        return False
    return True


""" getters """

def get_photo(photo_id):
    assert_photo_exists(photo_id)
    return session.query(Photo).filter(Photo.id==photo_id).first()
    
def get_photo_tags(photo_id):
    query = session.query(Tag).filter(and_(PhotoTag.p_id==photo_id, PhotoTag.t_id==Tag.id))
    tags = [tag.text for tag in query]
    return tags

# adds img_data, tags to Photo object
def marshal(photo):
    photo.img_uri = '/static' + static_photo_fname(photo.id, photo.ext)
    tags = get_photo_tags(photo.id)
    photo.tags = tags
    return photo

# returns Photo object with added attributes: img_data, tags    
def load_photo(id):
    if not photo_exists(id): 
        return None
    photo = get_photo(id)
    return marshal(photo)


""" upload functions """

# called by API Photo POST request, returns new Photo's filename
def process_new_photo(ext, tags, user):
    photo_id = new_photo_placeholder(user).id
    date_uploaded = datetime.now()
    update_image(photo_id, tags, ext, date_uploaded)
    return str(photo_id) + "." + ext

# makes placeholder Photo object, stores to db, returns Photo
def new_photo_placeholder(user):
    photo = Photo(o_id = user.id)
    session.add(photo)
    session.commit()
    return photo

# uploads Photo image to file system
def update_image(photo_id, tags, ext, date_uploaded):
    add_tags(photo_id, tags)
    update_photo_metadata(photo_id, ext, date_uploaded)
    
# updates metadata of Photo object in db
def update_photo_metadata(photo_id, photo_ext, date_uploaded):
    photo_fname = get_photo_fname(photo_id, photo_ext)
    # read metadata: geolocation, date created
    gtr = GeoTagReader(photo_fname)
    try:
        lat = gtr.get_lat()                   # float
        lon = gtr.get_lon()                   # float
        date_created = gtr.get_date_created() # datetime object 
    except KeyError:
        lat = None
        lon = None
        date_created = date_uploaded
    # set values on Photo object
    photo = get_photo(photo_id)
    photo.ext = photo_ext
    photo.lat = lat
    photo.lon = lon
    photo.date_created = date_created
    photo.date_uploaded = date_uploaded
    assert photo in session
    session.commit()

# adds tags to Photo object in db
def add_tags(photo_id, tags):
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


""" delete functions """

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

    
""" search functions """

# returns list of marshalled Photo objects
def load_all_photos():
    photos = session.query(Photo).filter(Photo.date_uploaded != None).all()
    photos.sort(key=lambda x: x.date_uploaded)
    return [marshal(photo) for photo in photos]

# implements filter on photos    
def get_photos(user, tags, start, end, lat, lon, zoom):
    # it's really really dumb to load all photos...but for now it is ok.
    photos = load_all_photos()
    # permissions!
    photos = filter(lambda x: can_view_photo(user, x), photos)
    # filter for matching tags: AND
    if tags:
        tags = [tag.strip() for tag in tags.split(',')]
        print "tags: ", tags
        for tag in tags:
            photos = filter(lambda photo: (lambda photo_tag: tag in photo_tag, photo), photos)
    # filter by start date
    if start:
        print "start: ", start
        photos = filter(lambda x: x.date_created >= start, photos)
    # filter by end date
    if end:
        print "end: ", end
        photos = filter(lambda x: x.date_created <= end, photos)
    # filter by geolocation
    if lat and lon and zoom:
        rad = 6.0/zoom # 6.0 is some arbitrary number, hope it works :B
        photos = filter(lambda x: in_radius(x.lat, x.lon, lat, lon, zoom), photos)
    return photos
