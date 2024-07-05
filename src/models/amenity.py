"""
Amenity related functionality
"""

from src.models.base import Base
from src import db


class Amenity(Base):
    __tablename__ = 'amenities'
    name = db.Column(db.String(120), nullable=False)
 
    def __init__(self, name: str, **kw):
        """Initialize a new amenity"""
        super().__init__(**kw)
        self.name = name
 
    def __repr__(self) -> str:
        """String representation of the amenity"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the amenity"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            }

    @staticmethod
    def create(amenity_data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence import repo

        amenity = Amenity(**data)
        repo.save(amenity)
        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        from src.persistence import repo

        amenity: Amenity | None = Amenity.query.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)

        return amenity
