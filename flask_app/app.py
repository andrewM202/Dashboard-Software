from flask import Flask, Blueprint
from config import Config
from models import login, user_datastore
from flask_security import Security
from flask_paranoid import Paranoid
from flask_wtf.csrf import CSRFProtect, generate_csrf
import flask, gzip

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
    SECURITY_RECOVERABLE = True,
    SECURITY_TRACKABLE = True,
    SECURITY_CHANGEABLE = True,
    SECURITY_CONFIRMABLE = True,
    SECURITY_REGISTERABLE = True,
    SECURITY_UNIFIED_SIGNIN = True,
    # enforce CSRF protection for session / browser - but allow token-based
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

@app.after_request
def compress(response):
    """ Compress all requests """
    accept_encoding = flask.request.headers.get('accept-encoding','').lower()
    if response.status_code < 200 or response.status_code >= 300 or response.direct_passthrough or 'gzip' not in accept_encoding or 'Content-Encoding' in response.headers:  return response
    content = gzip.compress(response.get_data(), compresslevel=9)  # 0: no compression, 1: fastest, 9: slowest. Default: 9
    response.set_data(content)
    response.headers['content-length']   = len(content)
    response.headers['content-encoding'] = 'gzip'
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')