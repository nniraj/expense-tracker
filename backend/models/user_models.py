from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User model for storing user account information."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        """Hash and store the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the provided password against the stored hash.
        
        Args:
            password (str): The plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)