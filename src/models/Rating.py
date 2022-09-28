from src.database import db


class Rating(db.Model):
    __tablename__ = "rating"

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, recipe_id, value):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.value = value

    def __repr__(self):
        return f"<Rating {self.user_id}, {self.recipe_id} - {self.value}>"
