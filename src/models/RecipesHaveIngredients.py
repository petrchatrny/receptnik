from src.database import db


class RecipesHaveIngredients(db.Model):
    __tablename__ = "recipes_have_ingredients"

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True, nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(10), nullable=False)

    # relations
    ingredient = db.relationship("Ingredient", backref="recipe")

    def __init__(self, recipe_id, ingredient_id, value, unit):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"<RecipesHaveIngredients {self.value}, {self.unit}>"
