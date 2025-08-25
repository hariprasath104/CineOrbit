# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

class Config:
    """Base configuration settings."""
    
    # Secret key for signing session cookies and other security-related needs
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    
    # --- Database Configuration (Improved for Render) ---
    
    # Get the database URL from the environment variables
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Heroku/Render sometimes provide "postgres://" which SQLAlchemy doesn't like.
    # We need to change it to "postgresql://". This check makes it safe.
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    # Use the DATABASE_URL if it exists (for Render), otherwise fall back to SQLite (for local)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///database.db'
    
    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False