""" takes care of photo stuff on the server """

from db import Photo, Tag, PhotoTag, session
from datetime import datetime
import config
import os
from sqlalchemy.exc import IntegrityError

from utils import *

from tasks import update_image


""" functions that operate on photo objects """

""" utils """

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

def safe(val):
    if type(val) == datetime:
        return str(val)
    return val

# serializes Photo object to JSON    
def to_json(photo):
    photo_dict = dict()
    for k,v in photo.__dict__.iteritems():
        if not k.startswith('_'): # ignore private attributes
            photo_dict[k] = safe(v)
    return photo_dict

# returns JSON-serialized Photo object from id    
def load_photo_json(id):
    photo = load_photo(id)
    if not photo:
        return None
    return to_json(photo)
    
""" upload functions """

# makes placeholder Photo object, stores to db, returns Photo
def new_photo_placeholder():
    photo = Photo()
    session.add(photo)
    session.commit()
    return photo
    
# called by API Photo POST request, returns new Photo's filename
def process_new_photo(ext, tags):
    photo_id = new_photo_placeholder().id
    date_uploaded = datetime.now()
    update_image.delay(photo_id, tags, ext, date_uploaded)
    return str(photo_id) + "." + ext
    
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
    
def get_photos(tags, start, end, lat, lon, rad):
    photos = load_all_photos()
    # filter for matching tags: AND
    if tags:
        tags = [tag.strip() for tag in tags.split(',')]
        print "tags: ", tags
        for tag in tags:
            photos = filter(lambda x: tag in x.tags, photos)
    # filter by start date
    if start:
        print "start: ", start
        photos = filter(lambda x: x.date_created >= start, photos)
    # filter by end date
    if end:
        print "end: ", end
        photos = filter(lambda x: x.date_created <= end, photos)
    # filter by geolocation
    if lat and lon and rad:
        photos = filter(lambda x: in_radius(x, lat, lon, rad), photos)
    return photos
