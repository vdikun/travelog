import config
from db import session, Photo, Tag, PhotoTag
from sqlalchemy import and_, or_
from flask.ext.restful.fields import DateTime
import math
from datetime import datetime

""" utility functions for photos """

class NoSuchObjectException(Exception):
    pass

def in_radius(p1_lat, p1_lon, p2_lat, p2_lon, rad):
    if (not p1_lat) or (not p1_lon):
        return False
    d_lat = p1_lat - p2_lat
    d_lon = p1_lon - p2_lon
    dist = math.sqrt(pow(d_lat,2) + pow(d_lon,2))
    return dist <= rad

def safe(val):
    if type(val) == datetime:
        return str(val)
    return val

def get_photo_fname(photo_id, photo_ext):
    return config.IMG_DIR + str(photo_id) + "." + photo_ext
    
def static_photo_fname(photo_id, photo_ext):
    return '/img/' + str(photo_id) + "." + photo_ext

# serializes Photo object to JSON    
def to_json(photo):
    photo_dict = dict()
    for k,v in photo.__dict__.iteritems():
        if not k.startswith('_'): # ignore private attributes
            photo_dict[k] = safe(v)
    return photo_dict