from datetime import datetime

import cloudinary.uploader
from sqlalchemy import collate

from src.controllers.auth_controller import easy_authentication_required, hard_authentication_required
from src.controllers.format_controller import FormatController, parse_bool
from src.controllers.ingredient_controller import create_ingredient_if_not_exits
from flask import Blueprint, request, session, render_template, Response, current_app

from src.controllers.logging_controller import database_error
from src.controllers.recipe_controller import delete_recipe_without_commit, get_max_preparation_time, \
    get_oldest_recipe_creation_date
from src.database import db
from src.models.PreparationStep import PreparationStep
from src.models.Rating import Rating
from src.models.Recipe import Recipe
from src.models.RecipesHaveIngredients import RecipesHaveIngredients

blueprint = Blueprint("recipes", __name__, url_prefix="/recipes")
PAGE_LENGTH = 6
INGREDIENTS_LIMIT = 20
STEPS_LIMIT = 15


@blueprint.get("/")
@easy_authentication_required
def get_recipes():
    # get values
    filters = []
    data = dict(request.args)
    page = int(data.get("page", 1))
    m_format = str(data.get("format", "json"))
    order_by = str(data.get("order_by", "name"))

    # setup filters
    filters.append(Recipe.name.ilike(f"%{data.get('name', '')}%"))
    filters.append(Recipe.preparation_in_minutes <= int(data.get("max_preparation_time", get_max_preparation_time())))
    if "newer_than" in data:
        newer_than = datetime.strptime(data["newer_than"], "%Y-%m-%d")
    else:
        newer_than = get_oldest_recipe_creation_date()
    filters.append(Recipe.creation_date >= newer_than)
    try:
        if "difficulty" in data and int(data["difficulty"]) != -1:
            filters.append(Recipe.difficulty_id == int(data["difficulty"]))
        if "is_vegetarian" in data:
            filters.append(Recipe.is_vegetarian == parse_bool(data["is_vegetarian"]))
        if "is_vegan" in data:
            filters.append(Recipe.is_vegan == parse_bool(data["is_vegan"]))
        if "is_gluten_free" in data:
            filters.append(Recipe.is_gluten_free == parse_bool(data["is_gluten_free"]))
        if "is_lactose_free" in data:
            filters.append(Recipe.is_lactose_free == parse_bool(data["is_lactose_free"]))
    except ValueError:
        return {"message": "wrong_data_format"}, 406

    # get list of recipes by filters
    if order_by == "rating":
        recipes = Recipe.query.filter(*filters).all()
        recipes.sort(key=lambda r: r.get_rating(), reverse=True)
    else:
        if current_app.config["ENV"] == "production":
            recipes = Recipe.query.filter(*filters).order_by(collate(Recipe.name, 'czech')).all()
        else:
            recipes = Recipe.query.filter(*filters).order_by(Recipe.name).all()

    # slice list to pages
    recipes = [recipes[i:i + PAGE_LENGTH] for i in range(0, len(recipes), PAGE_LENGTH)]
    max_page = len(recipes)

    # select page
    if page - 1 < len(recipes) and page >= 1:
        recipes = recipes[page - 1]
    else:
        recipes = []

    # convert page to selected format
    if m_format == "html":
        return {"page": page,
                "max_page": max_page,
                "data": render_template("data_templates/recipe_list.html", recipes=recipes)}, 200
    else:
        try:
            formatter = FormatController(m_format)
            return Response(formatter.converter.convert_recipe_list(recipes), mimetype=f"application/{m_format}")
        except ValueError:
            return {"message": "wrong_format_type"}, 400


@blueprint.get("/<recipe_id>")
@easy_authentication_required
def get_recipe(recipe_id):
    # receive data
    data = dict(request.args)
    m_format = str(data.get("format", "json"))

    # get recipe
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if recipe is None:
        return {"message": "no_such_recipe"}, 400

    # convert to format
    try:
        formatter = FormatController(m_format)
        return Response(formatter.converter.convert_full_recipe(recipe), mimetype=f"application/{m_format}")
    except ValueError:
        return {"message": "wrong_format_type"}, 400


@blueprint.post("/")
@hard_authentication_required
def create_recipe():
    # check received data
    data = dict(request.form)
    parsed_data = {"steps": [], "ingredients": [], "is_author_anonymous": False, "is_vegetarian": False,
                   "is_vegan": False, "is_gluten_free": False, "is_lactose_free": False}

    # parse simple data
    try:
        parsed_data["name"] = str(data["name"])
        parsed_data["servings"] = int(data["servings"])
        parsed_data["preparation_in_minutes"] = int(data["preparation_in_minutes"])
        parsed_data["difficulty"] = int(data["difficulty"])
        parsed_data["user_id"] = int(session["user"]["user_id"])
        if "is_author_anonymous" in data:
            parsed_data["is_author_anonymous"] = parse_bool(data["is_author_anonymous"])
        if "is_vegetarian" in data:
            parsed_data["is_vegetarian"] = parse_bool(data["is_vegetarian"])
        if "is_vegan" in data:
            parsed_data["is_vegan"] = parse_bool(data["is_vegan"])
        if "is_gluten_free" in data:
            parsed_data["is_gluten_free"] = parse_bool(data["is_gluten_free"])
        if "is_lactose_free" in data:
            parsed_data["is_lactose_free"] = parse_bool(data["is_lactose_free"])
    except KeyError:
        return {"message": "missing_data"}, 400
    except ValueError:
        return {"message": "wrong_data_format"}, 406

    # process ingredients and steps
    for key, value in data.items():
        if "step" in key and value != "":
            split = key.split("-")
            parsed_data["steps"].append({"number": int(split[1]), "text": value})
        elif "ingredient_name" in key and value != "":
            split = key.split("-")
            if len(parsed_data["ingredients"]) <= int(split[1]) - 1:
                parsed_data["ingredients"].append({"name": "", "value": 0, "unit": ""})
            parsed_data["ingredients"][int(split[1]) - 1]["name"] = value
        elif "ingredient_value" in key and value != "":
            split = key.split("-")
            parsed_data["ingredients"][int(split[1]) - 1]["value"] = value
        elif "ingredient_unit" in key and value != "":
            split = key.split("-")
            parsed_data["ingredients"][int(split[1]) - 1]["unit"] = value
    if len(parsed_data["ingredients"]) > INGREDIENTS_LIMIT:
        return {"message": "too_many_ingredients"}, 406
    if len(parsed_data["steps"]) > STEPS_LIMIT:
        return {"message": "too_many_steps"}, 406

    # process image file
    filename = None
    if "image" in request.files and request.files["image"].filename != "":
        file = request.files["image"]

        # check mime type
        if file.mimetype not in current_app.config["ALLOWED_MIMETYPES"]:
            return {"message": "wrong_image_format"}, 415

        # save file
        pub_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f-')
        upload_result = cloudinary.uploader.upload(file, public_id=pub_id)
        if upload_result:
            filename = upload_result["secure_url"]
    parsed_data["image"] = filename

    # save recipe to DB
    recipe = Recipe(name=parsed_data["name"], image=parsed_data["image"], servings=parsed_data["servings"],
                    difficulty_id=parsed_data["difficulty"], user_id=parsed_data["user_id"],
                    is_vegetarian=parsed_data["is_vegetarian"], is_vegan=parsed_data["is_vegan"],
                    is_lactose_free=parsed_data["is_lactose_free"], is_gluten_free=parsed_data["is_gluten_free"],
                    is_author_anonymous=parsed_data["is_author_anonymous"],
                    preparation_in_minutes=parsed_data["preparation_in_minutes"])
    db.session.add(recipe)
    try:
        db.session.commit()
    except Exception as e:
        return database_error(e)
    r_id = recipe.recipe_id

    # add/get ingredients to/from db
    used_ingredient_ids = [create_ingredient_if_not_exits(i["name"]) for i in parsed_data["ingredients"]]

    # create Ingredients-Recipe association
    for i in range(len(used_ingredient_ids)):
        db.session.add(RecipesHaveIngredients(ingredient_id=used_ingredient_ids[i],
                                              value=parsed_data["ingredients"][i]["value"],
                                              unit=parsed_data["ingredients"][i]["unit"], recipe_id=r_id))

    # create preparation steps
    for s in parsed_data["steps"]:
        db.session.add(PreparationStep(number=s["number"], text=s["text"], recipe_id=r_id))

    # add everything to db
    try:
        db.session.commit()
        return {"message": "success", "recipe_id": r_id}, 200
    except Exception as e:
        return database_error(e)


@blueprint.put("/<recipe_id>")
@hard_authentication_required
def update_recipe(recipe_id):
    # TODO Implement me
    return "<h1>Work in progress</h1>"


@blueprint.delete("/<recipe_id>")
@hard_authentication_required
def delete_recipe(recipe_id):
    user_id = int(session["user"]["user_id"])
    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
    if recipe is None:
        return {"message": "no_such_recipe"}, 404

    # authorization
    if recipe.user_id != user_id:
        return {"message": "unauthorized_access"}, 403

    delete_recipe_without_commit(recipe)
    try:
        db.session.commit()
        return {"message": "success"}, 200
    except Exception as e:
        return database_error(e)


@blueprint.post("/<recipe_id>/rate")
@hard_authentication_required
def rate_recipe(recipe_id):
    user_id = int(session["user"]["user_id"])
    if "value" not in request.form:
        return {"message": "missing_data"}, 400
    value = request.form["value"]

    rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if rating is not None:
        rating.value = value
    else:
        rating = Rating(user_id, recipe_id, value)

    db.session.add(rating)
    try:
        db.session.commit()
        return {"message": "success"}, 200
    except Exception as e:
        return database_error(e)
