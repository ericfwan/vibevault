from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)

    track_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=True)
    album = db.Column(db.String(200), nullable=True)

    artwork_url = db.Column(db.String(500), nullable=True)
    preview_url = db.Column(db.String(500), nullable=True)

    mood = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
