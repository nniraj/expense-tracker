import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/expense_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"