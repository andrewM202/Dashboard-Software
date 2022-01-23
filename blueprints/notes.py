from flask import render_template, Blueprint, send_from_directory
from flask_login import  current_user
from flask_security import login_required

bp = Blueprint("notes", __name__)

@bp.route("/admin/notes")
@login_required
def notes():
    return send_from_directory('client/public', 'index.html')