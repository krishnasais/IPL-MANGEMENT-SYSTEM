# 🏏 IPL Management System (Flask Version)

A web application built with **Flask** for managing and displaying detailed information about the **Indian Premier League (IPL)**, including teams, players, matches, sponsors, and awards like Orange Cap and Purple Cap.

## 📌 Project Overview

This project demonstrates a modular and scalable IPL management portal using Python Flask. The system handles CRUD operations for teams and players, and dynamically showcases league data with real-time interactions.

## ⚙️ Features

- Franchise and player management (CRUD)
- Team and league sponsors
- Orange Cap & Purple Cap leaderboards
- Match schedule and results
- Umpire and venue listings
- RESTful route structure with clean UI
- SQLAlchemy ORM for database operations

## 🛠 Tech Stack

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Jinja2 Templates
- **Database**: SQLite / MySQL
- **Tools**: Flask-Migrate, WTForms (optional), Bootstrap (optional for styling)

## 🗃 Database Schema

Includes tables like:

- `teams`
- `players`
- `matches`
- `venues`
- `umpires`
- `sponsors`
- `orange_cap`
- `purple_cap`
- `team_sponsors`
- `league_sponsors`

> SQL schema available in `database/ipl_schema.sql`.

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8+
- pip
- Virtualenv (recommended)

### 🛠 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/ipl-flask-system.git
cd ipl-flask-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database (for SQLite)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Or import `ipl_schema.sql` if using MySQL
