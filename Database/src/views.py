from flask import Blueprint, request, render_template
from src import db
from src.models import Track
from datetime import date

main = Blueprint('main', __name__)

@main.get("/tracks")
def list_tracks():
    """Lists all tracks from the Track table of the database. 

    Returns
    -------
    str 
        an HTML display text.
    """
    try:
        tracks = Track.query.all()
        return render_template('tracks.html', tracks=tracks, method=request.method)
    except Exception as e:
        return str(e)
    
@main.get("/tracks/<int:id>")
def get_track(id):
    """Gets a specific track from the Track table of the database.

    Parameters
    ----------
    id : int 
        The id of the track to be retrieved from the database. 

    Returns
    -------
    str 
        an HTML display text.
    """

    try:    
        track = db.session.execute(db.select(Track).filter_by(id=id)).scalar_one()
        return render_template('tracks.html', track=track, method=request.method)
    except Exception as e:
        return str(e)

@main.post("/tracks")
def upload_track():
    """Uploads a track to the Track table of the database with the data provided in the upload form. 

    Returns
    -------
    str 
        an HTML display text.
    """

    try:
        artist = request.form["artist"]
        name = request.form["name"]
        release_date = date.fromisoformat(request.form["release_date"])

        data_file = request.files["data"]
        data = data_file.read()

        cover_file = request.files["cover"]
        cover = cover_file.read()

        track = Track(
            name=name,
            artist=artist,
            data=data,
            cover = cover,
            release_date = release_date
        )
        db.session.add(track)
        db.session.commit()
        return render_template("tracks.html", track=track, method=request.method)
    except Exception as e:
        db.session.rollback()
        return str(e)


@main.delete("/tracks/<int:id>")
def delete_track(id):
    """Deletes a specific track from the Track table of the database. 

    Parameters
    ----------
    id : int 
        The id of the track to be deleted in the database. 

    Returns
    -------
    str 
        an HTML display text. 
    """

    try:
        track = db.session.get(Track, id)
        db.session.delete(track)
        db.session.commit()
        return render_template("tracks.html", track=track, method=request.method)
    except Exception as e:
        db.session.rollback()
        return str(e)

@main.delete("/tracks")
def clear_tracks():
    """Clears the Track database from all its entries.

    Returns
    -------
    str 
        an HTML display text.
    """

    try:
        db.drop_all()
        return render_template("tracks.html", method=request.method)
    except Exception as e:
        return str(e)
    
@main.route("/")
def index():
    return "<p>Hello, world!</p>"
    