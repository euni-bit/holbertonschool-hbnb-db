"""
Review related functionality
"""

from src.models.base import Base
from src import db

class Review(Base):
    __tablename__ = 'reviews'
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __init__(self, text: str, user_id: str, place_id: str, **kw):
        """Initialize a new review"""
        super().__init__(**kw)
        self.text = text
        self.user_id = user_id
        self.place_id = place_id

    def __repr__(self) -> str:
        """String representation of the review"""
        return f"<Review {self.id} (User: {self.user_id}, Place: {self.place_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the review"""
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(review_data: dict) -> "Review":
        """Create a new review"""
        from src.persistence import repo

        new_review = Review(**review_data)
        repo.save(new_review)
        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        from src.persistence import repo

        review: Review | None = Review.query.get(review_id)

        if not review:
            return None

        if "text" in data:
            review.text = data["text"]
        if "user_id" in data:
            review.user_id = data["user_id"]
        if "place_id" in data:
            review.place_id = data["place_id"]

        repo.update(review)
        return review
