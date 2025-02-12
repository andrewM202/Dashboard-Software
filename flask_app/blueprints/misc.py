from flask import render_template, Blueprint, send_from_directory, request
from flask_login import  current_user
from flask_security import login_required
from models import UserSettings, db
from os import environ

########################### Global Variables #####################################

bp = Blueprint("misc", __name__)

db_name = environ['MONGODB_DB']
collections = db.get_database(db_name).list_collection_names()

########################### Misc Routes #####################################

# Path for our main Svelte page
@bp.route("/")
def base():
    return send_from_directory('client/public', 'index.html')
    
@bp.route("/robots.txt")
def robots():
    return send_from_directory('client/public', 'robots.txt')

@bp.route("/landing")
def landing():
    return send_from_directory('client/public', 'index.html')

@bp.route("/profile")
@login_required
def profile():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@bp.route("/<path:path>")
def home(path):
  return send_from_directory('client/public', path)

########################### Settings Page #####################################

@bp.route("/admin/settings")
@login_required
def settings():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/setting-changes", methods=["POST"])
@login_required
def change_settings():
    UserSettings.objects().update(
        sidebar_state = True if request.form.get('sidebar-state') == "on" else False,
        sidebar_color = request.form['sidebar-color'],
        archive_header_color = request.form['archive-header-color'],
        archive_table_color = request.form['archive-table-color'],
        archive_table_header_color = request.form['archive-table-header-color'],
        archive_table_alt_color = request.form['archive-table-alt-color'],
        archive_creation_color = request.form['archive-creation-color'],
        background_color = request.form['background-color'],
        footer_color = request.form['footer-color'],
        navigation_color = request.form['navigation-color'],
    )
    
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/settings-config")
@login_required
def settings_config():
    """ Returns JSON of the current settings configuration
    in the database """
    settings_config = UserSettings.objects()
    return settings_config.to_json()

@bp.route("/admin/set-default-settings", methods=["POST"])
@login_required
def set_default_settings():
    """ Set user settings back to default """
    UserSettings.objects().update(
        sidebar_state = False,
        sidebar_color = None,
        archive_header_color = None,
        archive_table_color = None,
        archive_table_header_color = None,
        archive_table_alt_color = None,
        archive_creation_color = None,
        background_color = None,
        footer_color = None,
        navigation_color = None,
    )
    return send_from_directory('client/public', 'index.html')