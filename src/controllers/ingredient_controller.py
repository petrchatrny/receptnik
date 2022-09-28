from src.database import db
from src.models.Ingredient import Ingredient


def create_ingredient_if_not_exits(text):
    ingredient = Ingredient.query.filter_by(name=text).first()
    if ingredient is not None:
        return ingredient.ingredient_id
    ingredient = Ingredient(name=text)
    db.session.add(ingredient)
    db.session.commit()
    return ingredient.ingredient_id
