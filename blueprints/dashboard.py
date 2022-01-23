from flask import render_template, Blueprint, send_from_directory
from flask_login import  current_user
from sys import path
path.append('../')
from app import app

bp = Blueprint("dashboard", __name__)

@bp.route("/admin/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/settings")
def settings():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/maps")
def maps():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/dashboard/people")
def people_dashboard():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/tables")
def tables():
    if not current_user.is_authenticated:
        return app.login_manager.unauthorized()
    return send_from_directory('client/public', 'index.html')