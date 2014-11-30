""" runs the app. """

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from api import init_api

app = Flask(__name__)
app.config.from_object('config')
init_api(app)  
        
@app.before_request
def before_request():
    #g.db = connect_db()
    pass

@app.teardown_request
def teardown_request(exception):
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    """
    pass

if __name__ == '__main__':
    app.run()
