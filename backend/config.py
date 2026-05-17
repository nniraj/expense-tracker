import os
from datetime import timedelta

class Config:
    """Base configuration - loads from environment variables."""
    # Database URL must be set in .env file or environment
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError(
            "DATABASE_URL environment variable is not set. "
            "Please create a .env file or set the environment variable."
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise ValueError(
            "JWT_SECRET_KEY environment variable is not set. "
            "Please create a .env file or set the environment variable."
        )
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)