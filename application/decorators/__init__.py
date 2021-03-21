from functools import wraps 
from  flask import redirect, url_for, session, flash

def enforce_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('email') is None:
            flash('please log in first!')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper #return inner function


def prevent_login_signup(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('email'):
            flash("your are currently logged in")
            return redirect(url_for('profile'))
        return fn(*args, **kwargs)
    return wrapper


def enforce_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_email = kwargs.get('email')
        if correct_email != session.get('email'):
            flash('Not Authenticated')
            return redirect(url_for('profile'))
        return fn(*args, **kwargs)
    return wrapper


    
def is_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        correct_access = 300
        if correct_access != session.get('access'):
            flash("you are not authorized")
            return redirect(url_for('profile'))
        return fn(*args, **kwargs)
    return wrapper
