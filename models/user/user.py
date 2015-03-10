from db import session, User
from sqlalchemy import and_, or_, exc

class NewUserError(Exception):
	pass

def authenticate_user(name, password):
    user = session.query(User).filter(and_(User.name==name, User.password==password)).first()
    return user
    
def get_user(uid):
    user = session.query(User).filter(User.id==uid).first()
    return user

def register_user(name, password, email):
	user = User(name=name, password=password, email=email)
	session.add(user)
	try:
		session.commit()
	except exc.IntegrityError, e:
		session.rollback()
		if 'users.email' in e.message:
			raise NewUserError("That email is taken. Please try again")
		elif 'users.name' in e.message:
			raise NewUserError("That username is taken. Please try again")
		else:
			raise NewUserError("Something went wrong. Please try again")
	return user