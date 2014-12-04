""" minimal RESTful API for Photos """
""" supports POST /photos, GET /photos/<id>, DELETE /photos/<id> """

from flask import request
from flask.ext import restful

from models.photo import load_photo_json, new_photo_placeholder, upload_image, add_tags, delete_photo

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

    def post(self):
        image_data = request.form['image_data']
        tags = request.form['tags']
        ext = request.form['ext']
        photo_id = process_new_photo(image_data, ext, tags) 
        return {"photo_id": photo_id, "status": "uploading"}

def init_api(app):
    api = restful.Api(app)        
    api.add_resource(PhotoList, '/photos/')
    api.add_resource(Photo, '/photos/<string:photo_id>')
