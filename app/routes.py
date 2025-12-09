from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Song
import requests
from datetime import datetime, timedelta
import random

main_bp = Blueprint("main", __name__)

MOODS = [
    "Chill",
    "Happy",
    "Hype",
    "Heartbreak",
    "Focus",
    "Nostalgic"
]

def itunes_search(term, limit=20):
    if not term:
        return []
    url = "https://itunes.apple.com/search"
    params = {
        "term": term,
        "entity": "song",
        "limit": limit
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        cleaned = []
        for item in results:
            cleaned.append({
                "trackId": item.get("trackId"),
                "trackName": item.get("trackName"),
                "artistName": item.get("artistName"),
                "collectionName": item.get("collectionName"),
                "artworkUrl100": item.get("artworkUrl100"),
                "previewUrl": item.get("previewUrl")
            })
        return cleaned
    except Exception:
        return []

@main_bp.route("/")
def home():
    latest = Song.query.order_by(Song.created_at.desc()).limit(3).all()
    return render_template("home.html", latest_songs=latest, moods=MOODS)

@main_bp.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = itunes_search(q) if q else []
    return render_template("search.html", query=q, results=results)

def find_duplicate(track_id, title, artist, mood):
    if track_id:
        return Song.query.filter_by(track_id=track_id, mood=mood).first()
    if title and artist and mood:
        return Song.query.filter(
            Song.title.ilike(title),
            Song.artist.ilike(artist),
            Song.mood == mood
        ).first()
    return None

@main_bp.route("/add", methods=["GET", "POST"])
def add_song():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        album = request.form.get("album", "").strip()
        artwork_url = request.form.get("artwork_url", "").strip()
        preview_url = request.form.get("preview_url", "").strip()
        mood = request.form.get("mood", "").strip()
        note = request.form.get("note", "").strip()
        track_id_raw = request.form.get("track_id", "").strip()

        if not title:
            flash("That song needs a title to exist in this universe.")
            return redirect(url_for("main.search"))

        if not mood:
            flash("Pick a mood so your future self understands the vibe.")
            return redirect(url_for("main.add_song", title=title, artist=artist, album=album,
                                    artwork_url=artwork_url, preview_url=preview_url, track_id=track_id_raw))

        track_id = None
        try:
            track_id = int(track_id_raw) if track_id_raw else None
        except ValueError:
            track_id = None

        dup = find_duplicate(track_id, title, artist, mood)
        if dup:
            flash("You already saved this one in that mood. Your taste is consistent.")
            return redirect(url_for("main.vault", highlight_id=dup.id, mood=mood))

        song = Song(
            track_id=track_id,
            title=title,
            artist=artist if artist else None,
            album=album if album else None,
            artwork_url=artwork_url if artwork_url else None,
            preview_url=preview_url if preview_url else None,
            mood=mood,
            note=note if note else None
        )
        db.session.add(song)
        db.session.commit()

        flash("Saved. Your vault just got cooler.")
        return redirect(url_for("main.vault", highlight_id=song.id, mood=mood))

    track_data = {
        "track_id": request.args.get("track_id", ""),
        "title": request.args.get("title", ""),
        "artist": request.args.get("artist", ""),
        "album": request.args.get("album", ""),
        "artwork_url": request.args.get("artwork_url", ""),
        "preview_url": request.args.get("preview_url", "")
    }
    return render_template("add_song.html", moods=MOODS, track=track_data)

@main_bp.route("/vault")
def vault():
    selected_mood = request.args.get("mood", "").strip()
    if selected_mood and selected_mood not in MOODS:
        selected_mood = ""

    q = request.args.get("q", "").strip()

    songs_query = Song.query.order_by(Song.created_at.desc())

    if selected_mood:
        songs_query = songs_query.filter_by(mood=selected_mood)

    if q:
        like = f"%{q}%"
        songs_query = songs_query.filter(
            (Song.title.ilike(like)) |
            (Song.artist.ilike(like)) |
            (Song.note.ilike(like))
        )

    songs = songs_query.all()

    grouped = {}
    for s in songs:
        grouped.setdefault(s.mood, []).append(s)

    highlight_id = request.args.get("highlight_id", "")
    return render_template(
        "vault.html",
        grouped=grouped,
        moods=MOODS,
        highlight_id=highlight_id,
        selected_mood=selected_mood,
        query=q
    )


@main_bp.route("/moods")
def mood_map():
    songs = Song.query.all()
    counts = {m: 0 for m in MOODS}
    latest_by_mood = {m: None for m in MOODS}

    for s in songs:
        if s.mood in counts:
            counts[s.mood] += 1

    for m in MOODS:
        latest_by_mood[m] = Song.query.filter_by(mood=m).order_by(Song.created_at.desc()).first()

    total = sum(counts.values())

    top_mood = None
    if total > 0:
        top_mood = max(counts.items(), key=lambda x: x[1])[0]

    return render_template(
        "moods.html",
        moods=MOODS,
        counts=counts,
        latest_by_mood=latest_by_mood,
        total=total,
        top_mood=top_mood
    )


@main_bp.route("/delete/<int:song_id>", methods=["POST"])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    mood = song.mood
    db.session.delete(song)
    db.session.commit()

    next_url = request.form.get("next") or ""
    flash("Removed. Sometimes growth is just editing.")
    if next_url:
        return redirect(next_url)
    return redirect(url_for("main.vault", mood=mood))
