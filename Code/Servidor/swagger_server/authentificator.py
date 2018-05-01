from Flask import session


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


def enforce_auth(func):
    def inner(*args, **kwargs):
        if 'userid' not in session:
            return 'Need authentification', 401
        return func(*args, **kwargs)
    return inner


def enforce_user(func, userid):
    def inner(*args, **kwargs):
        if 'userid' not in session or session['userid'] == userid:
            return 'Forbidden for this user', 403
        return func(*args, **kwargs)
    return inner


def enforce_admin(func):
    def inner(*args, **kwargs):
        if 'admin' not in session:
            return 'Forbidden for this non-admins', 403
        return func(*args, **kwargs)
    return inner