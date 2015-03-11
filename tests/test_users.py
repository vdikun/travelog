""" tests for user.py """

# testing stuff
from nose import with_setup
from nose.tools import nottest
from mock import Mock, patch

# domain stuff
from models import user
from app import make_app
import db
import shutil, os
import config

u_name = "testname"
u_pwd = "testpassword"
u_email = "useremail@something.com"
email = "test@em.com"
v_pwd = "viewerpassword"

emails = ["a@e.m", "b@c.g", "r@p.d"]

class TestUserFunctions:

    @classmethod
    def setup_class(self):
        # set up test db
        app = make_app()
        assert(app)
        db.init_test_db(app)
        
    @classmethod
    def teardown_class(self):
        pass
    
    def test_stuff(self):
        u = user.register_user(u_name, u_pwd, u_email)
        assert (u is not None)
        assert (u == user.find_user(u_name, u_pwd))
        
        viewers = user.find_viewers(u)
        assert len(viewers) == 0
        
        user.make_viewers(u, [email], v_pwd)
        viewers = user.find_viewers(u)
        assert len(viewers) == 1
        
        user.make_viewers(u, emails, v_pwd)
        viewers = user.find_viewers(u)
        assert len(viewers) == 1 + len(emails)
        
         
