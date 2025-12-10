x# VibeVault

VibeVault is a personal music journaling web app that lets you search for songs, play short previews and save them into mood-based vaults with optional notes.

## Features
- Search for songs using the iTunes Search API
- Play a short preview before saving (when available)
- Save tracks into one of six mood categories
- Add personal notes alongside songs
- Browse your vault by mood
- Search within your vault
- Remove songs
- View a quick overview of your saved moods in Mood Map
- See recent saves on the home page via Quick Previews

## Project context
This is my coursework Part 2 for SET09103 Advanced Web Technologies, an individual Flask web application with a focus on cohesive design, server-side persistence and appropriate use of external APIs/libraries.

## Tech stack
- Python
- Flask
- Jinja2
- Flask-SQLAlchemy
- SQLite
- HTML/CSS/JavaScript
- Requests

## Setup & Run

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate geh
pip install -r requirements.txt
python run.py

