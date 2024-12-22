from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

class Track(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    artist: Mapped[str] = mapped_column(unique=False)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.get("/tracks")
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
    
@app.get("/tracks/<int:id>")
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

@app.put("/tracks")
def upload_track():
    """Uploads a track to the Track table of the database with the data provided 
    alongside the PUT request. 

    Returns
    -------
    str 
        an HTML display text.
    """

    try:
        parameters = request.get_json()
        track = Track(
            name=parameters['name'],
            artist=parameters['artist']
        )
        db.session.add(track)
        db.session.commit()
        return render_template("tracks.html", track=track, method=request.method)
    except Exception as e:
        return str(e)


@app.delete("/tracks/<int:id>")
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
        return str(e)

@app.delete("/tracks")
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
    
@app.route("/")
def index():
    return "<p>Hello, world!</p>"

if __name__ == "__main__":
    app.run(debug=True)