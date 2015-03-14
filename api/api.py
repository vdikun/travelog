""" minimal RESTful API for Photos """
""" supports POST /photos, GET /photos/<id>, DELETE /photos/<id> """

from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, fields
from werkzeug.utils import secure_filename

from models.photo import load_photo_json, to_json, process_new_photo, delete_photo, get_photos

from flask.ext.login import login_required, current_user

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

    @login_required
    def get(self, photo_id):
        photo_js = load_photo_json(photo_id)
        if photo_js is None:
            return 404
        return photo_js

    @login_required
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

    @login_required
    def get(self):
        args = self.get_parser.parse_args()
        photos = get_photos(current_user, args.tags, args.startdate, args.enddate, args.lat, args.lon, args.rad)
        print "getting %s photos" % len(photos)
        return [to_json(photo) for photo in photos]
    
    @login_required
    def post(self):
        file = request.files.getlist('photo[]')
        tags = [tag.strip() for tag in request.form['tags'].split(',')]

        redirect = ("redirectme" in request.form)
<<<<<<< HEAD
        
        

        for i in file:
            print dir(i)
            if not i:
                return 404, "No file"
            if not allowed_file(i.filename):
                return 404, "Bad file extension"
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(i.filename)

            ### Well if you want to carry on with this you have to make sure
            ### that the file name origionally does not exist in this folder
            ### so additional code should be written to realize that function
            ### I'm not writting today.
            
            # insert temporary record in database
            i.save(os.path.join(config.UPLOAD_FOLDER, filename))
            new_filename = process_new_photo(filename, fileext(i.filename), tags, current_user)
    
            # Move the file from the temporary folder to the upload folder we setup
            os.rename(os.path.join(config.UPLOAD_FOLDER, filename),os.path.join(config.UPLOAD_FOLDER, new_filename))

        ### Also the return value should change according to all these things
=======
        print file
        print "andy\n"
        if not file:
            return 404, "No file"
        if not allowed_file(file.filename):
            return 404, "Bad file extension"

        
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # insert temporary record in database
        print filename
        print "filename is the above one"
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        new_filename = process_new_photo(filename, fileext(file.filename), tags, current_user)
        
        # Move the file from the temporary folder to the upload folder we setup
        os.rename(os.path.join(config.UPLOAD_FOLDER, filename),os.path.join(config.UPLOAD_FOLDER, new_filename))

>>>>>>> 849704e16e9477b9ed37d6ee711009319c1f526f
        return {"success": True, "file": new_filename}

def init_api(app):
    api = restful.Api(app)        
    api.add_resource(PhotoList, '/photos/')
    api.add_resource(Photo, '/photos/<string:photo_id>')




