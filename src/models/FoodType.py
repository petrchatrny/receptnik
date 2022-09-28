from src.database import db


class FoodType(db.Model):
    __tablename__ = "food_type"

    food_type_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<FoodType {self.name}>"
