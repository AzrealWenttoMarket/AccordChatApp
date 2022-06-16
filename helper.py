from functools import wraps
from flask import request, redirect, url_for, session
import random
import string

def login_required(f):
    @wraps(f)
    def decorated_fucntion(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_fucntion

def random_str(digit=7):
    answer = ""
    for i in range(digit):
        answer += random.choice(string.ascii_letters + string.digits)
    return answer