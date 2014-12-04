from db import session, User
from sqlalchemy import and_, or_

def authenticate_user(name, password):
    user = session.query(User).filter(and_(User.name==name, User.password==password)).first()
    return user
    
def get_user(uid):
    user = session.query(User).filter(User.id==uid).first()
    return user
