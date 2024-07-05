"""
City related functionality
"""

from src.models.base import Base
from src.extensions import db


class City(Base):
    """City Class"""
    __tablename__ = 'cities'
    name = db.Column(
        db.String(120),
        nullable=False
        )
    country_id = db.Column(
        db.String(36),
        db.ForeignKey('countries.id'),
        nullable=False
        )

    def __init__(self, name: str, country_id: str, **kw) -> None:
        """Initialize a new city"""
        super().__init__(**kw)
        self.name = name
        self.country_id = country_id

    def __repr__(self) -> str:
        """String representation of the city"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the city"""
        return {
            "id": self.id,
            "name": self.name,
            "country_id": self.country_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(city_data: dict) -> "City":
        """Create a new city"""
        from src.persistence import repo

        new_city = City(**city_data)
        repo.save(new_city)
        return new_city

    @staticmethod
    def update(city_id: str, data: dict) -> "City | None":
        """Update an existing city"""
        from src.persistence import repo

        city: City | None = City.query.get(city_id)

        if not city:
            return None

        if "name" in data:
            city.name = data["name"]
        if "country_id" in data:
            city.country_id = data["country_id"]

        repo.update(city)
        return city
