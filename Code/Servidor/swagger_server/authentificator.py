from flask import session


def sign_in(userid):
    session['userid'] = userid


def sign_admin():
    session['admin'] = True


def sign_out():
    session.pop('userid', None)
    if 'admin' in session:
        session.pop('admin', None)


def get_userid():
    if 'userid' in session:
        return session['userid']
    else:
        return None
    
def is_admin():
    if 'admin' in session:
        return session['admin']
    else:
        return False


def enforce_auth(func):
    def inner(*args, **kwargs):
        if 'userid' not in session:
            return 'Need authentification', 401
        return func(*args, **kwargs)
    return inner


def enforce_user(userid):
    def wraper(func):
        def inner(*args, **kwargs):
            if 'userid' not in session or session['userid'] != userid:
                return 'Forbidden for this user', 403
            return func(*args, **kwargs)
        return inner
    return wraper


def enforce_admin(func):
    def inner(*args, **kwargs):
        if 'admin' not in session:
            return 'Forbidden for non-admins', 403
        return func(*args, **kwargs)
    return inner
