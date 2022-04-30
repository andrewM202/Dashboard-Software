from flask import render_template, Blueprint, send_from_directory
from flask_login import  current_user
from flask_security import login_required

bp = Blueprint("dashboard", __name__)

@bp.route("/admin/dashboard")
@login_required
def dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/maps")
@login_required
def maps():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard/people")
@login_required
def people_dashboard():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/tables")
@login_required
def tables():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard-reviser")
@login_required
def dashboard_reviser():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard-designer")
@login_required
def dashboard_designer():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/chart-designer")
@login_required
def chart_designer():
    return send_from_directory('client/public', 'index.html')