import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(_name_)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key")

# Configure database connection
app.config.from_object('config.Config')

# Initialize SQLAlchemy with the app
db.init_app(app)

with app.app_context():
    # Import models to register them with SQLAlchemy
    from models import (Team, Player, Match, Stadium, Ticket, 
                       TeamOwner, TeamSponsor, LeagueSponsor, 
                       IPLCommittee, HeadCoach, ContractDetails, 
                       Stats, RunsStats, OrangeCap, PurpleCap)
    
    # Import routes
    from routes import *
    
    # Create all database tables
    db.create_all()
