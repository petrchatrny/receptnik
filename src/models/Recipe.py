from src.database import db
from datetime import datetime
from src.models.Rating import Rating
from sqlalchemy.sql import func


class Recipe(db.Model):
    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(150), nullable=True)
    preparation_in_minutes = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    is_vegetarian = db.Column(db.Boolean, nullable=False)
    is_vegan = db.Column(db.Boolean, nullable=False)
    is_gluten_free = db.Column(db.Boolean, nullable=False)
    is_lactose_free = db.Column(db.Boolean, nullable=False)
    is_author_anonymous = db.Column(db.Boolean, nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey("difficulty.difficulty_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    # relationships
    steps = db.relationship("PreparationStep", backref="recipe")
    food_types = db.relationship("FoodType", secondary="recipes_have_food_types", backref="recipe")
    difficulty = db.relationship("Difficulty", backref="recipe")
    ingredients = db.relationship("RecipesHaveIngredients", backref="recipe")
    author = db.relationship("User")
    rating = None

    def __init__(self, name, servings, difficulty_id, user_id,
                 is_vegetarian=False, is_vegan=False, is_lactose_free=False, is_gluten_free=False,
                 is_author_anonymous=False,
                 image="", preparation_in_minutes=0):
        self.name = name
        self.image = image
        self.preparation_in_minutes = preparation_in_minutes
        self.servings = servings
        self.is_vegetarian = is_vegetarian
        self.is_vegan = is_vegan
        self.is_lactose_free = is_lactose_free
        self.is_gluten_free = is_gluten_free
        self.is_author_anonymous = is_author_anonymous
        self.difficulty_id = difficulty_id
        self.user_id = user_id
        self.rating = None

    def __repr__(self):
        return f"<Recipe {self.name}>"

    def get_rating(self):
        if self.rating is None:
            rating = db.session.query(func.avg(Rating.value).label("average")).filter_by(
                recipe_id=self.recipe_id).first()
            if rating is not None and len(rating) > 0 and rating[0] is not None:
                self.rating = rating[0]
            else:
                self.rating = 0
        return self.rating
