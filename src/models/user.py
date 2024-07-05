"""
User model for the application
"""

from typing import Any
from src import db
from src.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email: str, first_name: str, last_name: str, password: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    @staticmethod
    def create(data: dict) -> Any:
        # Check if a user with the same email already exists
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=data.get("password")
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(entity_id: str, data: dict) -> Any:
        user = User.query.get(entity_id)
        if user is None:
            return None
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        if "password" in data:
            user.password_hash = generate_password_hash(data["password"])
        db.session.commit()
        return user
