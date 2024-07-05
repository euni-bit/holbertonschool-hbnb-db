"""
User model for the application
"""

from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from src.models.base import Base


class User(Base):
    """User class."""

    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email, first_name, last_name, password, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    @staticmethod
    def create(data):
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            raise ValueError("A user with this email already exists.")
        user = User(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=data.get("password")
        )
        user.save()
        return user

    @staticmethod
    def update(entity_id, data):
        user = User.query.get(entity_id)
        if user is None:
            return None
        user.email = data.get("email", user.email)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        if "password" in data:
            user.password_hash = generate_password_hash(data["password"])
        user.save()
        return user
