DATABASE = '/var/lib/sqlite3/travelog.db'
DATABASEURI = 'sqlite:///' + DATABASE
DEBUG = True
SECRET_KEY = "ihavethepants"
USERNAME = "admin"
PASSWORD = "default"
PRESERVE_CONTEXT_ON_EXCEPTION = False
UPLOAD_FOLDER = "./static/img/"
IMG_DIR = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ['jpg']

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'travelog.sg@gmail.com'
MAIL_PASSWORD = 'manypants'
