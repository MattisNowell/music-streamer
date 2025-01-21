from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from src import db, bcrypt
from src.models import User
from src.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import base64

main = Blueprint('main', __name__)


# ***** Authentication and Registration Backend ******

@main.get("/register")
def register():
    """Display the register page and form. 

    Returns
    -------
    HTML 
        an HTML template, either retrieved directly or indirectly from redirections. 
    """

    # If the user is already authenticated:
    if current_user.is_authenticated:
        return redirect(url_for("main.account"))
    
    # If not show register form:
    form = RegistrationForm()
    return render_template("register.html", form=form)

@main.post("/register")
def registering():
    """Handles the posted registration data form to register the new user attempting to create an account.

    Returns
    -------
    HTML 
        an HTML template, retrieved from redirections. 
    """

    # If the user is already authenticated:
    if current_user.is_authenticated:
        return redirect(url_for("main.get_current_user"))

    # If not verify registration details:
    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data, 
            email = form.email.data,
            password = hashed_password 
        )    
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.login")) # Redirect to login page 

   # If details not valid: 
    print(form.errors)
    return redirect(url_for("main.register"))

@main.get("/login")
def login():
    """Displays the login page and form.

    Returns
    -------
    HTML 
        an HTML template, either retrieved directly or indirectly from redirections. 
    """

    # If the user is already authenticated:
    if current_user.is_authenticated:
        return redirect(url_for("main.account"))
    
    # If not show login form:
    form = LoginForm()
    return render_template("login.html", form=form)
    
@main.post("/login")
def authenticating():
    """Handles the posted login data form to authenticate a user attempting to login.

    Returns
    -------
    HTML 
        an HTML template, retrieved from redirections.
    """
    
    # If the user is already authenticated:
    if current_user.is_authenticated:
        return redirect(url_for("main.get_current_user"))

    # If not verify login details:
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("main.get_current_user"))
        else:
            print("The password and email address don't match.")
    
    # If details not valid. 
    print("Invalid fields.")
    return redirect(url_for("main.login"))

@main.route("/logout")
def logout():
    """Logs out the current user.

    Returns
    -------
    HTML 
        HTML template 
    """

    logout_user()
    return redirect(url_for("main.login"))


# ***** Account Backend ******

@main.get("/<int:id>")
def get_user(id):
    """Gets a specific user from the User table of the database.

    Returns
    -------
    JSON or HTML 
        JSON response if requested, otherwise renders an HTML template.

    """

    try:    

        if id == current_user.id:
            return redirect(url_for("main.get_current_user"))
        
        user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
        if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
            return jsonify ({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "picture": base64.b64encode(user.picture).decode('utf-8') if user.picture else None,
            }), 200
        
        return render_template('account.html', user=user)
    except Exception as e:
        return str(e), 500


@main.get("/")
@login_required
def get_current_user():
    """Gets the logged-in user from the current session.

    Returns
    -------
    JSON or HTML 
        JSON response if requested, otherwise renders an HTML template.

    """

    try:    
        if request.headers.get("Accept") == "application/json" or request.args.get("format") == "json":
            return jsonify ({
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "password": current_user.password,
                "picture": base64.b64encode(current_user.picture).decode('utf-8') if current_user.picture else None,
            }), 200
        
        return render_template('account.html', user=current_user)
    except Exception as e:
        return str(e), 500