from flask import render_template, Blueprint, send_from_directory
from flask_login import  current_user
from sys import path
path.append('../')
from app import app

bp = Blueprint("notes", __name__)

@bp.route("/admin/notes")
def notes():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')