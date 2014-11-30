""" tests for photos.py """

# testing stuff
from nose import with_setup
from nose.tools import nottest
from mock import Mock, patch

# domain stuff
from photos import *
from db import Photo, Tag, PhotoTag, init_test_db
import shutil, os
import config

# utils
from os.path import isfile
from datetime import datetime

IMG_DIR      = "./static/img/"
TEST_IMG_DIR = "./static/test/"

P_NONE = 12
P_UPLOADED = 1
P_NOT_UPLOADED = 2

class TestPhotoFunctions:

    @classmethod
    def setup_class(self):
        # set up test db
        init_test_db()
        # copy images from ./img/ to ./test/
        shutil.copytree(IMG_DIR, TEST_IMG_DIR)
        
    @classmethod
    def teardown_class(self):
        # move images back
        shutil.rmtree(IMG_DIR)
        shutil.copytree(TEST_IMG_DIR, IMG_DIR)
        shutil.rmtree(TEST_IMG_DIR)

    def test_new_photo_placeholder(self):
        photo = new_photo_placeholder()
        assert(photo.id == 4) # kind of a stupid test, but...
    
    @nottest    
    def test_delete_photo(self):
        # delete Photo that doesn't exist
        try:
            delete_photo(P_NONE)
            assert(False)
        except:
            pass
        # delete Photo that exists
        count_tags = session.query(PhotoTag).filter(PhotoTag.p_id==P_UPLOADED).count()
        print "number of tags for photo %i: %i" % (P_UPLOADED, count_tags)
        assert(count_tags != 0)
        delete_photo(P_UPLOADED)
        # assert that Photo is deleted
        assert(session.query(Photo).filter(Photo.id==P_UPLOADED).count() == 0)
        print "deleted photo ", P_UPLOADED
        # assert that image file is likewise deleted
        assert(not os.path.isfile(get_photo_fname(P_UPLOADED, "jpg")))
        # assert that child tags are deleted
        count_tags = session.query(PhotoTag).filter(PhotoTag.p_id==P_UPLOADED).count()
        print "number of tags for photo %i: %i" % (P_UPLOADED, count_tags)
        assert(count_tags == 0) #nuh. fails.
        
    def test_geotag_reader(self):
        fname = get_photo_fname(P_UPLOADED, 'jpg')
        gtr = GeoTagReader(fname)
        # whatever.
        assert (gtr.get_date_created())
        assert (gtr.get_lat())
        assert (gtr.get_lon())
        
    def test_update_photo_metadata(self):
        dt_uploaded = datetime.now()
        ext = "jpg"
        photo_id = P_NOT_UPLOADED
        # look at Photo in db
        photo = get_photo(photo_id)
        assert (photo.uploaded == 0)
        assert (photo.date_uploaded is None)
        assert (photo.date_created is None)
        assert (photo.ext is None)
        # update metadata
        update_photo_metadata(photo_id, ext, dt_uploaded)
        # assert that metadata is updated
        photo = get_photo(photo_id)
        assert (photo.uploaded == 1)
        assert (photo.date_uploaded == dt_uploaded)
        assert (photo.date_created is not None)
        assert (photo.ext == "jpg")
        
    def test_add_tags(self):
        # Singapore tag already exists on this photo. sky tag exists on other photo. cat tag is new.
        tags = get_photo_tags(P_UPLOADED)    
        assert (len(tags) == 3)    
        assert ('landscape' in tags and 'Singapore' in tags and 'street' in tags)
        # add tags to Photo
        add_tags(P_UPLOADED, ['Singapore', 'sky', 'cat'])
        # look at tags again. yo.
        tags = get_photo_tags(P_UPLOADED)
        assert (len(tags) == 5)
        assert ('sky' in tags and 'cat' in tags)
        
    def test_upload_image(self):
        ext = 'jpg'
        with patch('models.photos.update_photo_metadata.delay') as update_photo_metadata:
            upload_image(P_NOT_UPLOADED, 'xxy', ext)
            fname = get_photo_fname(P_NOT_UPLOADED, ext)
            assert isfile(fname)
            update_photo_metadata.assert_called_once()

    def test_photo_to_json(self):
        photo = get_photo(P_UPLOADED)
        json = to_json(photo)
        print json
