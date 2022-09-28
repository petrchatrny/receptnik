import hashlib

from src.database import db
from datetime import datetime

from src.models.User import User


class ApiKey(db.Model):
    __tablename__ = "api_key"

    api_key_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    hash = db.Column(db.String(250), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)

    def __init__(self, name, user_id, is_active=False):
        self.name = name
        self.is_active = is_active
        self.user_id = user_id
        self.hash = str(hashlib.sha512(str(user_id).encode("utf-8") + str(datetime.now()).encode("utf-8")).hexdigest())

    def __repr__(self):
        return f"<ApiKey {self.name}>"
