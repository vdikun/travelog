import os
#from app import make_app
from app import app
from db import init_db
from flask.ext.testing import TestCase
import tempfile
from flask import request, url_for
import unittest

from models.photo import marshal, get_photo

class TravelogTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        init_db(app, './test_schema.sql')
        return app

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config['DATABASE'])
        
    def test_marshal(self):
        with self.app.test_request_context():
            photo = get_photo(1)
            marshal(photo)

if __name__ == '__main__':
    unittest.main()
