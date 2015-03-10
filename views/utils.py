""" util functions for views """

from flask import flash

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print "Error"
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

class AuthenticationError(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv