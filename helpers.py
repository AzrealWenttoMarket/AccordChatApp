from functools import wraps
from flask import session, request, redirect, url_for
# restrict a page to a logged-in user only e.g
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function