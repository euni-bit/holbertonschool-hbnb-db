"""
Place related functionality
"""

from src.models.base import Base
from src import db

class Place(Base):
    __tablename__ = 'places'
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name: str, city_id: str, user_id: str, description: str = "", **kw):
        """Initialize a new place"""
        super().__init__(**kw)
        self.name = name
        self.city_id = city_id
        self.user_id = user_id
        self.description = description

    def __repr__(self) -> str:
        """String representation of the place"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the place"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city_id": self.city_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(place_data: dict) -> "Place":
        """Create a new place"""
        from src.persistence import repo

        new_place = Place(**place_data)
        repo.save(new_place)
        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        from src.persistence import repo

        place: Place | None = Place.query.get(place_id)

        if not place:
            return None

        if "name" in data:
            place.name = data["name"]
        if "description" in data:
            place.description = data["description"]
        if "city_id" in data:
            place.city_id = data["city_id"]
        if "user_id" in data:
            place.user_id = data["user_id"]

        repo.update(place)
        return place
