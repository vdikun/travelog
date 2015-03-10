""" runs the app. """

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
 
from flask.ext.login import LoginManager
     
from views import default, owner, viewer

from models.user import get_user

from api import init_api

from db import connect_db

from serveremail import mail

DEFAULT_BLUEPRINTS = (
    default,
    owner,
    viewer
)

def configure_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(userid):
        return get_user(userid)

def add_site_map(app):
    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            if "GET" in rule.methods:
                url = url_for(rule.endpoint)
                links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples
        return link

def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
def configure_error_handlers(app):
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('error/401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('error/500.html'), 500

def make_db_connections(app):

    @app.before_request
    def before_request():
        g.db = connect_db(app)

    @app.teardown_request
    def teardown_request(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

def init_mail(app):
    mail.init_app(app)

def make_app():
    app = Flask(__name__)
    app.config.from_object('travelog.config')
    configure_blueprints(app, DEFAULT_BLUEPRINTS)
    configure_error_handlers(app)
    configure_login(app)
    add_site_map(app)
    init_api(app)
    init_mail(app)
    make_db_connections(app)
    return app


    
app = make_app()

if __name__ == '__main__':
    app.run()
