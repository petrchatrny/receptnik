import logging

from flask import Blueprint, request, session, current_app

from src.controllers.auth_controller import hard_authentication_required
from src.controllers.logging_controller import database_error
from src.models.ApiKey import db, ApiKey

blueprint = Blueprint("api_keys", __name__, url_prefix="/api-keys")


@blueprint.post("/")
@hard_authentication_required
def create_api_key():
    # get values
    user_id = int(session["user"]["user_id"])
    if "name" not in request.form:
        return {"message": "missing_data"}, 400
    name = request.form["name"]

    # check key limit
    keys = ApiKey.query.filter_by(user_id=user_id).all()
    if len(keys) >= current_app.config["API_KEY_LIMIT"]:
        return {"message": "too_many_keys"}, 406

    # create key
    key = ApiKey(name, session["user"]["user_id"])

    db.session.add(key)

    try:
        db.session.commit()
        return {"message": "success"}, 200
    except Exception as e:
        logging.log(logging.ERROR, f"DB ERROR: {e}")
        return {"message": "db_failure", "error": str(e)}, 400


@blueprint.post("/<api_key_id>/activation")
@hard_authentication_required
def change_api_key_activation(api_key_id):
    user_id = session["user"]["user_id"]
    key = ApiKey.query.filter_by(api_key_id=api_key_id, user_id=user_id).first()

    if key is None:
        return {"message": "unauthorized_access"}, 403

    key.is_active = not key.is_active
    is_key_active = key.is_active

    try:
        db.session.commit()
        return {"message": "success", "is_key_active": is_key_active}, 200
    except Exception as e:
        return database_error(e)


@blueprint.delete("/<api_key_id>")
def delete_api_key(api_key_id):
    user_id = session["user"]["user_id"]
    key = ApiKey.query.filter_by(api_key_id=api_key_id, user_id=user_id).first()
    if key is None:
        return {"message": "unauthorized_access"}, 403

    db.session.delete(key)

    try:
        db.session.commit()
        return {"message": "success"}, 200
    except Exception as e:
        return database_error(e)
