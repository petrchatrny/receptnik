import functools

from flask import request, session, redirect, url_for

from src.models.User import User
from src.models.ApiKey import ApiKey


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("web.prihlaseni"))
        return func(*args, **kwargs)

    return secure_function


def easy_authentication_required(func):
    @functools.wraps(func)
    def easy_authentication(*args, **kwargs):
        if "api_key" in request.args:
            key = str(request.args["api_key"])
            found_key = ApiKey.query.filter_by(hash=key).first()
            if found_key is None:
                return {"message": "unauthenticated_access"}, 401
            if not found_key.is_active:
                return {"message": "inactive_api_key"}, 406
            return func(*args, **kwargs)
        elif "user" in session:
            user = check_user_in_session()
            if user is None:
                return {"message": "unauthenticated_access"}, 401
            return func(*args, **kwargs)
        else:
            return {"message": "unauthenticated_access"}, 401

    return easy_authentication


def hard_authentication_required(func):
    @functools.wraps(func)
    def hard_authentication(*args, **kwargs):
        if "user" in session:
            user = check_user_in_session()
            if user is None:
                return {"message": "unauthenticated_access"}, 401
            return func(*args, **kwargs)
        else:
            return {"message": "unauthenticated_access"}, 401

    return hard_authentication


def check_user_in_session():
    return User.query.filter_by(user_id=session["user"]["user_id"], nickname=session["user"]["nickname"],
                                email=session["user"]["email"], icon=session["user"]["icon"]).first()
