#import urllib.request
from flask import redirect, render_template, request,session, url_for
from functools import wraps

def apology(top="", bottom=""):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html",top=escape(top),bottom=escape(bottom))

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function