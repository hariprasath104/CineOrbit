# config.py

import os
from dotenv import load_dotenv

# Unga laptop la run pannum pothu .env file la irundhu settings ah edukuradhuku
load_dotenv()

class Config:
    """Base configuration settings."""
    
    # Idhu unga website oda security kaga thevaiyana oru secret password maari.
    # Render la idhu Environment Variable la irundhu varum.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    
    # --- Database Configuration (Render kuaga sariyaga amaikapattadhu) ---
    
    # Indha line thaan Render oda Environment Variables kulla poi,
    # DATABASE_URL nu neenga kudutha address ah eduthutu varum.
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Idhu oru chinna technical fix. Render oda URL la 'postgres://' nu irukum,
    # aana nammodaya program ku 'postgresql://' nu venum. Indha code adha automatic ah maathidum.
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    # Indha line thaan final decision edukum:
    #   - DATABASE_URL (Render oda address) irundha, adha use pannu.
    #   - Illana, 'sqlite:///database.db' ah (unga laptop oda database) use pannu.
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///database.db'
    
    # Idhu SQLAlchemy oda oru extra feature ah disable pannum, appo unga app fast ah irukum.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
