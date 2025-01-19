import base64
from flask import Blueprint, request, render_template, jsonify
from src import db
from src.models import Track
from datetime import date

main = Blueprint('main', __name__)

@main.get("/tracks")
def list_tracks():
    """Lists all tracks from the Track table of the database. 

    Returns
    -------
    JSON or HTML 
        JSON response if requested, otherwise renders an HTML template.
    """
    try:
        tracks = Track.query.all()
        
        if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
            tracks_data = [
                {
                    "id": track.id,
                    "name": track.name,
                    "artist": track.artist,
                    "data": base64.b64encode(track.data).decode('utf-8') if track.data else None,
                    "cover": base64.b64encode(track.cover).decode('utf-8') if track.cover else None,
                    "release_date": track.release_date.isoformat() if track.release_date else None
                } for track in tracks                           
            ]
            
            return jsonify(tracks_data), 200
        
        return render_template('tracks.html', tracks=tracks, method=request.method)
    except Exception as e:
        return {"error": str(e)}, 500
    
@main.get("/tracks/<int:id>")
def get_track(id):
    """Gets a specific track from the Track table of the database.

    Parameters
    ----------
    id : int 
        The id of the track to be retrieved from the database. 

    Returns
    -------
    JSON or HTML 
        JSON response if requested, otherwise renders an HTML template.
    """

    try:    
        track = db.session.execute(db.select(Track).filter_by(id=id)).scalar_one()
        
        if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
            return jsonify ({
                "id": track.id,
                "name": track.name,
                "artist": track.artist,
                "data": base64.b64encode(track.data).decode('utf-8') if track.data else None,
                "cover": base64.b64encode(track.cover).decode('utf-8') if track.cover else None,
                "release_date": track.release_date.isoformat() if track.release_date else None
            }), 200
        
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
        return {"error": str(e)}, 500


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
        return {"error": str(e)}, 500

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
        return {"error": str(e)}, 500
    
@main.route("/")
def index():
    return "<p>Hello, world!</p>"
    