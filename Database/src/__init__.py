from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialise database
db = SQLAlchemy()

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

    from src import models

    # Checks if an instance of the database already exists.
    with app.app_context():
        db.create_all()

    # Point to the routes in the views file. 
    from src.views import main
    app.register_blueprint(main)

    return app