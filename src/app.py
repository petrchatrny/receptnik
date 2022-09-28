import logging
import os

import cloudinary.uploader
from flask import Flask
from itsdangerous import URLSafeTimedSerializer

from src.config import ProductionConfig, MissingEnvironVariableError
from src.database import db
from src.routes.api import api_blueprint
from src.routes.web import web_blueprint, err_blueprint

# init app
app = Flask(__name__)

# configure app
environ = os.environ.get("FLASK_ENV")
if environ is None or environ == "development":
    app.config.from_object("src.config.DevelopmentConfig")
elif environ == "production":
    if ProductionConfig.SECRET_KEY is None:
        raise MissingEnvironVariableError("SECRET_KEY")
    if ProductionConfig.MAIL_SERVER is None:
        raise MissingEnvironVariableError("MAIL_SERVER")
    if ProductionConfig.MAIL_PORT is None:
        raise MissingEnvironVariableError("MAIL_PORT")
    if ProductionConfig.MAIL_USE_SSL is None:
        raise MissingEnvironVariableError("MAIL_USE_SSL")
    if ProductionConfig.MAIL_USE_TLS is None:
        raise MissingEnvironVariableError("MAIL_USE_TLS")
    if ProductionConfig.MAIL_USERNAME is None:
        raise MissingEnvironVariableError("MAIL_USERNAME")
    if ProductionConfig.MAIL_PASSWORD is None:
        raise MissingEnvironVariableError("MAIL_PASSWORD")
    if ProductionConfig.SQLALCHEMY_DATABASE_URI is None:
        raise MissingEnvironVariableError("SQLALCHEMY_DATABASE_URI")
    app.config.from_object("src.config.ProductionConfig")

# setup token maker
token_maker = URLSafeTimedSerializer(secret_key=app.config["SECRET_KEY"])
app.config["token_maker"] = token_maker

# setup cloudinary
cloudinary.config(
    cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
    api_key=app.config["CLOUDINARY_API_KEY"],
    api_secret=app.config["CLOUDINARY_API_SECRET"]
)

# setup db
db.init_app(app)

# register blueprints
app.register_blueprint(api_blueprint)
app.register_blueprint(web_blueprint)
app.register_blueprint(err_blueprint)

# init db
with app.app_context():
    # import tables to declare them and prevent NoReferencedTableError (non-existing Foreign keys)
    from src.models.Difficulty import Difficulty
    from src.models.FoodType import FoodType
    from src.models.Ingredient import Ingredient
    from src.models.RecipesHaveIngredients import RecipesHaveIngredients
    from src.models.Recipe import Recipe
    from src.models.User import User
    from src.models.Rating import Rating
    from src.models.ApiKey import ApiKey
    from src.models.PreparationStep import PreparationStep

    db.create_all()
    try:
        db.session.commit()
    except Exception as e:
        logging.log(logging.ERROR, f"DB initialization failed: {e}")

if __name__ == "__main__":
    app.run()
