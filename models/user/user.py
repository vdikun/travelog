from db import session, User, ViewerRelation
from sqlalchemy import and_, or_


'''
returns mathing User object
'''    
def find_user(name, password):
    user = session.query(User).filter(and_(User.name==name, User.password==password)).first()
    return user
 

'''
required by Flask-Login
'''
def authenticate_user(name, password):
    return find_user(name, password)


'''
returns User object matching uid
''' 
def get_user(uid):
    user = session.query(User).filter(User.id==uid).first()
    return user


'''
creates new User tuple and inserts into DB
returns None on failure, User object otherwise
'''
def make_user(name, password):
    user = User(name=name, password=password)
    session.add(user)
    try: 
        session.commit()
        return user
    except:
        return None

    
'''
returns list of a user's viewers (User objects)
'''
def find_viewers(owner):
    rows = (session.query(User, ViewerRelation)
            .filter(and_(User.id == ViewerRelation.v_id,
                         ViewerRelation.o_id == owner.id)
                    ).all()
           )
    return [x[0] for x in rows]


'''
returns user's owner
'''
def get_owner(viewer):
    assert viewer.is_viewer()
    owner = (session.query(User, ViewerRelation)
                                    .filter(and_(ViewerRelation.v_id == viewer.id,
                                                 ViewerRelation.o_id == User.id))
                                    .first()
                     )[0]
    return owner


'''
creates new Viewer tuple and inserts into DB
'''        
def make_viewer(owner, email, password):
    viewer = User(name=email, password=password, owner=False)
    session.add(viewer)
    session.commit()
    constraint = ViewerRelation(v_id=viewer.id, o_id=owner.id)
    session.add(constraint)
    session.commit()
    return viewer

'''
creates list of new Viewer tuples and inserts into DB
'''  
def make_viewers(owner, emails, password):
    [make_viewer(owner, email, password) for email in emails]
