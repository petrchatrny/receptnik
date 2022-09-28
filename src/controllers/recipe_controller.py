import cloudinary.uploader
from sqlalchemy import desc

from src.database import db
from src.models.PreparationStep import PreparationStep
from src.models.Rating import Rating
from src.models.Recipe import Recipe
from src.models.RecipesHaveFoodTypes import RecipesHaveFoodTypes
from src.models.RecipesHaveIngredients import RecipesHaveIngredients


def delete_recipe_without_commit(recipe):
    # delete ratings
    for rating in Rating.query.filter_by(recipe_id=recipe.recipe_id).all():
        db.session.delete(rating)

    # delete steps
    for step in PreparationStep.query.filter_by(recipe_id=recipe.recipe_id).all():
        db.session.delete(step)

    # delete assigned ingredients
    for ingredient in RecipesHaveIngredients.query.filter_by(recipe_id=recipe.recipe_id).all():
        db.session.delete(ingredient)

    # delete assigned food types
    for food_type in RecipesHaveFoodTypes.query.filter_by(recipe_id=recipe.recipe_id).all():
        db.session.delete(food_type)

    # delete image in cloud
    if recipe.image is not None:
        # public id without format (.png)
        last_slash_index = recipe.image.rfind("/")
        pub_id = recipe.image[last_slash_index + 1:-4]
        cloudinary.uploader.destroy(pub_id)

    # delete recipe
    db.session.delete(recipe)


def get_oldest_recipe_creation_date():
    recipes = Recipe.query.order_by(Recipe.creation_date).all()
    if len(recipes) > 1:
        return recipes[0].creation_date
    return 0


def get_max_preparation_time():
    recipes = Recipe.query.order_by(desc(Recipe.preparation_in_minutes)).all()
    if len(recipes) > 1:
        return recipes[0].preparation_in_minutes
    return 0
