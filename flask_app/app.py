from flask import Flask, Blueprint
from config import Config
from models import login, user_datastore
from flask_security import Security
from flask_paranoid import Paranoid
# Generate CSRF tokens with flask_wtf
from flask_wtf.csrf import CSRFProtect, generate_csrf
from os import environ

app = Flask(__name__)

# Variable to determine if we want to launch as a desktop app or not.
# If so then run as python3 app.py
use_desktop = True

app.config.from_object('config.DevelopmentConfig')
app.config.update(
    DEBUG=True,
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
    SECURITY_RECOVERABLE = True,
    SECURITY_TRACKABLE = True,
    SECURITY_CHANGEABLE = True,
    SECURITY_CONFIRMABLE = True,
    SECURITY_REGISTERABLE = True,
    SECURITY_UNIFIED_SIGNIN = True,
    # Enforce CSRF protection for session / browser - but allow token-based
    # API calls to go through
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"],
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True,
)

# Register Routes / Import Blueprints
# Raw Archive routes
from blueprints.archive import bp as archive_bp
app.register_blueprint(archive_bp)

# Dashboard routes
from blueprints.dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp)

# Not yet organized
from blueprints.misc import bp as misc_bp
app.register_blueprint(misc_bp)

# Notes page
from blueprints.notes import bp as notes_bp
app.register_blueprint(notes_bp)

# Authentication routes
from blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

# Create Flask-Login instance
login.init_app(app)
login.login_view = 'auth.login'
login.refresh_view = "auth.login"
login.session_protection = None

# Flask Security
security = Security(app, user_datastore)

# Flask Paranoid
paranoid = Paranoid(app)
paranoid.redirect_view = 'auth.login'

# Flask-WTF CSRF protection
csrf = CSRFProtect(app)

if __name__ == "__main__":
    if use_desktop == True:
        # Import flask-desktop's WebUI class
        from webui import WebUI 
        WebUI(app, debug=True).run()
    else:
        app.run(debug=True, host=environ['FLASK_HOST'])