from src.database import db


class RecipesHaveFoodTypes(db.Model):
    __tablename__ = "recipes_have_food_types"

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True, nullable=False)
    food_type_id = db.Column(db.Integer, db.ForeignKey("food_type.food_type_id"), primary_key=True)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.food_type_id = ingredient_id

    def __repr__(self):
        return f"<RecipesHaveFoodTypes {self.recipe_id}, {self.food_type_id}>"
