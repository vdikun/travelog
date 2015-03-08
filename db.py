""" db stuff """

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import closing
import sqlite3
from travelog import config

from flask.ext.login import UserMixin

Base = declarative_base()
engine = create_engine(config.DATABASEURI)
metadata = MetaData(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

class Photo(Base):
    __table__ = Table('photos', metadata, autoload=True)

class Tag(Base):
    __table__ = Table('tags', metadata, autoload=True)
    
class PhotoTag(Base):
    __table__ = Table('phototag', metadata, autoload=True)
    
class User(Base, UserMixin):
    __table__ = Table('users', metadata, autoload=True)
    
class Viewer(Base):
    __table__ = Table('viewers', metadata, autoload=True)
    
def connect_db(app):
    print "connect_db: %s" % app.config['DATABASE']
    db = sqlite3.connect(app.config['DATABASE'])
    db.cursor().executescript("PRAGMA foreign_keys = ON;") # should implement delete-cascade but doesn't
    return db
    
def init_db(app, schema_file='./schema.sql'):
    with closing(connect_db(app)) as db:
        with open(schema_file, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
def init_test_db(app):
    init_db(app, schema_file='./test_schema.sql')
