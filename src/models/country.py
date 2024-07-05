"""
Country related functionality
"""

from src.models.base import Base
from src.extensions import db


class Country(Base):
    __tablename__ = 'countries'
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(2), nullable=False)

    def __init__(self, name: str, code: str, **kw):
        """Initialize a new country"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """String representation of the country"""
        return f"<Country {self.id} ({self.name},{self.code})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the country"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(country_data: dict) -> "Country":
        """Create a new country"""
        from src.persistence import repo

        new_country = Country(**country_data)
        repo.save(new_country)
        return new_country

    @staticmethod
    def update(country_id: str, sate: dict) -> "Country | None":
        """Update an existing country"""
        from src.persistence import repo
        country: Country | None = Country.query.get(country_id)

        if not country:
            return None

        if "name" in data:
            country.name = data["name"]
        if "code" in data:
            country.code = data["code"]

        repo.save(country)
        return country
