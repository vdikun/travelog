""" minimal RESTful API for Photos """
""" supports POST /photos, GET /photos/<id>, DELETE /photos/<id> """

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, fields
from werkzeug.utils import secure_filename

from models.photo import load_photo_json, to_json, process_new_photo, delete_photo, get_photos

import os
import config

from datetime import datetime

def fileext(filename):
    return filename.rsplit(".")[-1].upper()
def allowed_file(filename):
    ext = fileext(filename)
    if ext in ["JPG"]:
        return True
    return False
    
def mydate(value):
    if not value:
        return None
    dt = datetime.strptime(value, "%Y-%m-%d") # raises ValueError if fails
    return dt
    
def myfloat(value):
    if not value:
        return value
    return float(value)

class Photo(restful.Resource):
        
    def get(self, photo_id):
        photo_js = load_photo_json(photo_id)
        if photo_js is None:
            return 404
        return photo_js
        
    def delete(self, photo_id):
        try:
            delete_photo(photo_id)
            return 200
        except:
            return 404
            
class PhotoList(restful.Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tags', type=str, help='Photo tags')
        parser.add_argument('startdate', type=mydate, help="Start of date range")
        parser.add_argument('enddate', type=mydate, help="End of date range")
        parser.add_argument('lat', type=myfloat, help="Latitude of center")
        parser.add_argument('lon', type=myfloat, help="Longitude of center")
        parser.add_argument('rad', type=myfloat, help='Radius from center in some arbitrary units', default=5)
        self.get_parser = parser

    def get(self):
        args = self.get_parser.parse_args()
        photos = get_photos(args.tags, args.startdate, args.enddate, args.lat, args.lon, args.rad)
        print "getting %s photos" % len(photos)
        return [to_json(photo) for photo in photos]
    
    def post(self):           
        tags = [tag.strip() for tag in request.form['tags'].split(',')]
        file = request.files['photo']
        redirect = ("redirectme" in request.form)
        
        if not file:
            return 404, "No file"
        if not allowed_file(file.filename):
            return 404, "Bad file extension"
            
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # insert temporary record in database
        new_filename = process_new_photo(fileext(file.filename), tags)
        # Move the file from the temporary folder to the upload folder we setup
        file.save(os.path.join(config.UPLOAD_FOLDER, new_filename))
        return {"success": True, "file": new_filename}

def init_api(app):
    api = restful.Api(app)        
    api.add_resource(PhotoList, '/photos/')
    api.add_resource(Photo, '/photos/<string:photo_id>')
