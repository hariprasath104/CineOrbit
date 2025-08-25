# models.py
import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Define an Enum for our user roles
class UserRole(enum.Enum):
    CLIENT = 'client'
    CREATOR = 'creator'  # This is our "Employee"

class User(UserMixin, db.Model):
    """User model for storing user accounts."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # NEW: Add the role column
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CLIENT)

    def set_password(self, password):
        """Create a hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'