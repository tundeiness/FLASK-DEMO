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