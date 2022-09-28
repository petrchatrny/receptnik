from src.database import db


class PreparationStep(db.Model):
    __tablename__ = "preparation_step"

    preparation_step_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(250), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)

    def __init__(self, number, text, recipe_id):
        self.number = number
        self.text = text
        self.recipe_id = recipe_id

    def __repr__(self):
        return f"<PreparationStep {self.text}>"
