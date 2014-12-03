""" runs the app. """

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

#from api import init_api

def make_app():
    app = Flask(__name__)
    app.config.from_object('config')
    #init_api(app)  
            
    return app
    
app = make_app()

if __name__ == '__main__':
    app.run()
