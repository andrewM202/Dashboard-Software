from flask import Flask, send_from_directory, redirect, Blueprint
from config import Config
import random

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Register Routes / Import Blueprints
# Raw Archive routes
from archive import bp as archive_bp
app.register_blueprint(archive_bp)

# Dashboard routes
from dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp)

from misc import bp as misc_bp
app.register_blueprint(misc_bp)

if __name__ == "__main__":
    app.run(debug=True)