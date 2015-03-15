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

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "travelog.sg@gmail.com"
MAIL_PASSWORD = "travelbox"