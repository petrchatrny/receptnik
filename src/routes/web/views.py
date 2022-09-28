import datetime

from flask import Blueprint, render_template, session, redirect, url_for, abort, current_app
from itsdangerous import SignatureExpired
from sqlalchemy import desc
from sqlalchemy import func as db_func

from src.controllers.auth_controller import login_required
from src.controllers.recipe_controller import get_max_preparation_time, get_oldest_recipe_creation_date
from src.models.User import User
from src.models.Difficulty import Difficulty
from src.models.Recipe import Recipe
from src.models.Rating import Rating

web = Blueprint("web", __name__)


@web.get("/")
def index():
    recipes = Recipe.query.join(Rating).add_columns(
        db_func.avg(Rating.value).label("rating_avg")).group_by(
        Recipe.recipe_id).order_by(
        desc("rating_avg")).limit(3).all()
    recipes = list(map(lambda t: t[0], recipes))
    return render_template("pages/index.html", favourite_recipes=recipes)


@web.get("/recepty")
@login_required
def recepty():
    diffs = Difficulty.query.all()
    return render_template("pages/recipe_list.html", difficulties=diffs,
                           max_preparation_time=get_max_preparation_time(),
                           min_creation_date=get_oldest_recipe_creation_date().strftime("%Y-%m-%d"),
                           today=datetime.datetime.now().strftime("%Y-%m-%d"))


@web.get("/recepty/<recept_id>")
@login_required
def recept(recept_id):
    recipe = Recipe.query.filter_by(recipe_id=int(recept_id)).first()
    if recipe is None:
        return abort(404)
    rating = Rating.query.filter_by(recipe_id=int(recept_id), user_id=session["user"]["user_id"]).first()
    return render_template("pages/recipe.html", recipe=recipe, rating=rating)


@web.get("/dokumentace")
def dokumentace():
    return render_template("pages/documentation.html")


@web.get("/uzivatel")
@login_required
def uzivatel():
    user = User.query.filter_by(user_id=session["user"]["user_id"]).first()
    if user is None:
        session.clear()
        return redirect(url_for("web.prihlaseni"))
    return render_template("pages/user.html", user=user)


@web.get("/prihlaseni")
def prihlaseni():
    return render_template("pages/login.html")


@web.get("/registrace")
def registrace():
    return render_template("pages/register.html")


@web.get("/obnova-hesla")
def obnova_hesla():
    return render_template("pages/reset_password.html")


@web.get("/nove-heslo/<token>")
def nove_heslo(token):
    if token is None:
        return render_template("pages/message.html", title="Nastala chyba",
                               text="Odkaz je neplatný. Zažádejte o změnu hesla prosím znovu.")
    try:
        current_app.config["token_maker"].loads(token, salt=current_app.config["SECRET_KEY"], max_age=300)
        return render_template("pages/new_password.html", code=token)
    except SignatureExpired:
        return render_template("pages/message.html", title="Platnost odkazu vypršela",
                               text="Platnost vytvořeného odkazu je 1 hodina. Tato platnost již vypršela, zažádejte o "
                                    "změnu hesla prosím znovu.")


@web.get("/vytvoreni-receptu")
@login_required
def vytvoreni_receptu():
    difficulties = Difficulty.query.all()
    return render_template("pages/create_recipe_form.html", difficulties=difficulties)


@web.get("/uprava-receptu/<recipe_id>")
@login_required
def uprava_receptu(recipe_id):
    rep = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if rep is None:
        abort(404)
    if rep.user_id != session["user"]["user_id"]:
        abort(403)
    return render_template("pages/edit_recipe_form.html", recipe=rep)


@web.get("/vytvorit-klic")
@login_required
def vytvoreni_klice():
    return render_template("pages/key_form.html")


@web.get("/odhlaseno")
def odhlaseno():
    return render_template("pages/message.html", title="Odhlášeno",
                           text="Byli jste úspěšně odhlášeni. Děkujeme za návštěvu.")


@web.get("/rozlouceni")
def rozlouceni():
    return render_template("pages/message.html", title="Účet smazán",
                           text="Děkujeme za používání naší aplikace.")
