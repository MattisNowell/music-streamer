from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Common.track import create_track_model
from base64 import b64encode

# Initialise database
db = SQLAlchemy()
Track = create_track_model(db)

def create_app():
    """Creates the database microservice's flask app with its configuration, initialises the database's tables,  
    and links the app to the routes in the views file.   

    Returns
    -------
    Flask
        the database microservice's Flask app 
    """

    app = Flask(__name__)   
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"

    db.init_app(app)

    # Checks if an instance of the database already exists.
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Point to the routes in the views file. 
    from src.views import main
    app.register_blueprint(main)

    # Setting up a new filter for jinja to decode base64 images in HTML files. TO BE PUT IN AN extensions.py FILE IN THE FUTURE WITH OTHER EXTENSIONS AND CONFIG COMMANDS.
    @app.template_filter('to_base64')
    def to_base64_filter(binary_data):
        return b64encode(binary_data).decode('utf-8')

    app.jinja_env.filters['to_base64'] = to_base64_filter

    return app