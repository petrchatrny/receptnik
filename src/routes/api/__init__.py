from flask import Blueprint
import src.routes.api.ingredients as ingredients
import src.routes.api.recipes as recipes
import src.routes.api.users as users
import src.routes.api.api_keys as api_keys
import src.routes.api.food_types as food_types

api_blueprint = Blueprint("api", __name__,  url_prefix="/api")
api_blueprint.register_blueprint(ingredients.blueprint)
api_blueprint.register_blueprint(recipes.blueprint)
api_blueprint.register_blueprint(users.blueprint)
api_blueprint.register_blueprint(api_keys.blueprint)
api_blueprint.register_blueprint(food_types.blueprint)
