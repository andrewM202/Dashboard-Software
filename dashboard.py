from flask import render_template, Blueprint, send_from_directory

bp = Blueprint("dashboard", __name__)

@bp.route("/admin/dashboard")
def dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/settings")
def settings():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/maps")
def maps():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard/people")
def people_dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/tables")
def tables():
    return send_from_directory('client/public', 'index.html')