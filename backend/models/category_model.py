from extensions import db

class Category(db.Model):
    """Category model for organizing expenses into different types."""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)