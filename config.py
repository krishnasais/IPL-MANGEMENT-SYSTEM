import os

class Config:
    """Configuration settings for the application."""
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:#Dhoni@7@localhost/ipl_management')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'development-key')
    DEBUG = True
