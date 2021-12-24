from flask import Flask, send_from_directory, redirect, Blueprint
from config import Config
import random

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Register Routes / Import Blueprints
# Raw Archive routes
from raw_archive import bp as raw_archive_bp
app.register_blueprint(raw_archive_bp)

# Dashboard routes
from dashboard import bp as dashboard_bp
app.register_blueprint(dashboard_bp)

from misc import bp as misc_bp
app.register_blueprint(misc_bp)

if __name__ == "__main__":
    app.run()