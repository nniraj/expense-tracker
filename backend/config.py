import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Vedant%40065@localhost/expense_tracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-min-32-chars-long")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token valid for 24 hours