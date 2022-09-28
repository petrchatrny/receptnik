from src.database import db


class Difficulty(db.Model):
    __tablename__ = "difficulty"

    difficulty_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Difficulty {self.title}>"
