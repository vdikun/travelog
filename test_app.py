import os
#from app import make_app
from app import app
from db import init_db
from flask.ext.testing import TestCase
import tempfile
from flask import request, url_for
import unittest

class TravelogTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        init_db('./test_schema.sql')
        return app

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.app.config['DATABASE'])
        
    def test_nothing(self):
        with self.app.test_request_context():
            #print request.host
            print url_for("static", filename='img/0.jpg')
        pass

if __name__ == '__main__':
    unittest.main()
