import hashlib
import glob
import random

from src.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    nickname = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    icon = db.Column(db.String(80), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    password_reset = db.Column(db.String(250), nullable=True)

    # relations
    recipes = db.relationship("Recipe", viewonly=True)
    api_keys = db.relationship("ApiKey", backref="user")

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email
        self.password = self.hash_password(password, email)
        self.icon = self.get_random_user_icon()

    def __repr__(self):
        return f"<User {self.nickname}>"

    @staticmethod
    def hash_password(password, email):
        # using user's email as a salt
        return str(hashlib.sha512(password.encode("utf-8") + email.encode("utf-8")).hexdigest())

    def get_registration_date_in_czech_format(self):
        return datetime.strftime(self.registration_date, "%d.%m.%Y")

    def get_recipes_avg_rating(self):
        if len(self.recipes) == 0:
            return 0
        return sum(r.get_rating() for r in self.recipes) / len(self.recipes)

    def to_session_json(self):
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "email": self.email,
            "icon": self.icon,
            "registration_date": self.get_registration_date_in_czech_format()
        }

    @staticmethod
    def get_random_user_icon():
        icon_files = glob.glob("src/static/img/user_icons/*")
        rng = random.randint(0, len(icon_files) - 1)
        return icon_files[rng].replace("src/static", "")
