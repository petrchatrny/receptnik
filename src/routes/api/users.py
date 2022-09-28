import uuid
from smtplib import SMTPRecipientsRefused

from flask import Blueprint, request, current_app, url_for, render_template, session, redirect
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.exc import IntegrityError

from src.controllers.auth_controller import hard_authentication_required
from src.controllers.logging_controller import database_error
from src.controllers.recipe_controller import delete_recipe_without_commit
from src.models.Rating import Rating
from src.models.User import User, db

blueprint = Blueprint("users", __name__, url_prefix="/users")


@blueprint.post("/login")
def login():
    # check incoming data
    data = request.form
    if "email" not in data or "password" not in data:
        return {"message": "missing_data"}, 400

    email = data["email"]
    password = User.hash_password(data["password"], email)

    # find user in database
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return {"message": "wrong_credentials"}, 401

    # add user to session
    session["user"] = user.to_session_json()
    return {"message": "success"}, 200


@blueprint.post("/logout")
def logout():
    if "user" in session:
        session.pop("user")

    return redirect(url_for("web.odhlaseno"))


@blueprint.post("/register")
def register():
    # check incoming data
    data = request.form
    if "nickname" not in data or "email" not in data or "password" not in data:
        return {"message": "missing_data"}, 400

    # check unique email
    user_with_same_email = User.query.filter_by(email=data["email"]).first()
    if user_with_same_email is not None:
        return {"message": "email_already_taken"}, 400

    # create token and link for email confirmation
    token = current_app.config["token_maker"].dumps(data, salt=current_app.config["SECRET_KEY"])
    link = url_for("api.users.confirm_email", token=token, _external=True)

    # create mail client and message
    mail = Mail(current_app)
    msg = Message("Potvrzení registrace 🍽️", recipients=[data["email"]], sender="me.development@seznam.cz")

    # put data to html body of message
    mail_html = render_template("emails/registration_confirm.html", link=link,
                                logo=url_for("static", filename="/img/logo.jpg", _external=True))
    msg.html = mail_html

    # send mail
    try:
        mail.send(msg)
    except SMTPRecipientsRefused:
        return {"message": "invalid_email"}, 400
    else:
        return {"message": "success"}, 200


@blueprint.get("/confirm-email/<token>")
def confirm_email(token=None):
    if token is None:
        return render_template("pages/message.html", title="Nastala chyba", text="Odkaz je neplatný. Zaregistrujte se "
                                                                                 "prosím znovu.")
    try:
        # load data
        user_data = current_app.config["token_maker"].loads(token, salt=current_app.config["SECRET_KEY"], max_age=300)

        # insert user in the database
        u = User(nickname=user_data["nickname"], email=user_data["email"], password=user_data["password"])
        db.session.add(u)
        db.session.commit()
    except SignatureExpired:
        return render_template("pages/message.html", title="Platnost odkazu vypršela",
                               text="Platnost vytvořeného odkazu je 1 hodina. Tato platnost již vypršela, zaregistrujte"
                                    " se prosím znovu.")
    except BadSignature:
        return render_template("pages/message.html", title="Nastala chyba",
                               text="Odkaz je neplatný. Zaregistrujte se prosím znovu.")
    except IntegrityError:
        return render_template("pages/message.html", title="Odkaz byl již využit",
                               text="Tento odkaz byl již využit a už neplatí.")
    except Exception:
        return render_template("pages/message.html", title="Něco se nepodařilo",
                               text="Došlo k neznámé chybě. Operace nemohla být provedena")
    else:
        return render_template("pages/message.html", title="Zaregistrováno",
                               text="Registrace proběhla úspěšně, můžete se přihlásit.")


@blueprint.post("/forgot-password")
def forgot_password():
    data = request.form
    if "email" not in data:
        return {"message": "missing_data"}, 400

    # create unique code
    code = str(uuid.uuid4())

    # generate token
    token = current_app.config["token_maker"].dumps(code, salt=current_app.config["SECRET_KEY"])
    user = User.query.filter_by(email=data["email"]).first()
    if user is not None:
        # assign code to user
        user.password_reset = token
        try:
            db.session.commit()
        except Exception as e:
            return database_error(e)
    else:
        # fake email send due to security
        return {"message": "success"}, 200

    # send code to user as time-based token via email
    link = url_for("web.nove_heslo", token=token, _external=True)
    mail = Mail(current_app)
    msg = Message("Změna hesla", recipients=[data["email"]], sender="me.development@seznam.cz")
    mail_html = render_template("emails/password_reset.html", link=link,
                                logo=url_for("static", filename="/img/logo.jpg", _external=True))
    msg.html = mail_html
    # send mail
    try:
        mail.send(msg)
    except SMTPRecipientsRefused:
        return {"message": "invalid_email"}, 400
    else:
        return {"message": "success"}, 200


@blueprint.post("/update-password/<token>")
def update_password(token):
    if "password" not in request.form or token is None:
        return {"message": "missing_data"}, 400
    try:
        # check that token is valid
        current_app.config["token_maker"].loads(token, salt=current_app.config["SECRET_KEY"], max_age=300)

        # insert user in the database
        user = User.query.filter_by(password_reset=token).first()
        if user is None:
            return {"message": "invalid_link"}, 400
        user.password = User.hash_password(request.form["password"], user.email)
        db.session.commit()
        return {"message": "success"}, 200
    except SignatureExpired:
        return {"message": "link_expired"}, 400
    except BadSignature:
        return {"message": "invalid_link"}, 400
    except IntegrityError:
        return {"message": "link_already_used"}, 400
    except Exception as e:
        return database_error(e)


@blueprint.put("/<user_id>")
@hard_authentication_required
def update_user(user_id):
    # TODO Implement me
    return "<h1>Work in progress</h1>"


@blueprint.delete("/<user_id>")
@hard_authentication_required
def delete_user(user_id):
    session_user_id = int(session["user"]["user_id"])
    if session_user_id != int(user_id):
        return {"message": "unauthorized_access"}, 403

    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return {"message": "no_such_user"}, 404

    # delete user's recipes
    for recipe in user.recipes:
        delete_recipe_without_commit(recipe)

    # delete user's API keys
    for api_key in user.api_keys:
        db.session.delete(api_key)

    # delete user's rating
    ratings = Rating.query.filter_by(user_id=user_id).all()
    for rating in ratings:
        db.session.delete(rating)

    # delete user
    session.pop("user")
    db.session.delete(user)

    try:
        db.session.commit()
        return {"message": "success"}
    except Exception as e:
        return database_error(e)
