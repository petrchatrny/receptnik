from flask import Blueprint, render_template

err = Blueprint("error", __name__)


@err.app_errorhandler(403)
def forbidden_access(e):
    return render_template('errors/403.html'), 403


@err.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
