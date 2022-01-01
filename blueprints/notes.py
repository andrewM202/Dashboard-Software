from flask import render_template, Blueprint, send_from_directory

bp = Blueprint("notes", __name__)

@bp.route("/admin/notes")
def notes():
    return send_from_directory('client/public', 'index.html')