from flask import Flask, send_from_directory, redirect, Blueprint
from config import Config
import random
from models import login

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Create Flask-Login instance
login.init_app(app)
login.login_view = 'auth.login'

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

from blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)