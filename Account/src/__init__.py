from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
import os

# Initialise database
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    """Creates the account microservice's flask app with its configuration, initialises the database's tables,  
    and links the app to the routes in the views file.   

    Returns
    -------
    Flask
        the account microservice's Flask app 
    """

    app = Flask(__name__)   
    app.config['SECRET_KEY'] = os.urandom(12)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"

    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect to login page if not logged in
    login_manager.login_message_category = 'info'

    from src import models

    # Checks if an instance of the database already exists.
    with app.app_context():
        db.create_all()

    # Point to the routes in the views file. 
    from src.views import main
    app.register_blueprint(main)

    return app