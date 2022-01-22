from flask import render_template, redirect, Blueprint, send_from_directory, request
from models import User
from flask_login import current_user, login_user, logout_user

########################### Global Variables #####################################

bp = Blueprint("auth", __name__)

########################### Base Route #####################################

@bp.route("/auth/register")
def register():
    return send_from_directory('client/public', 'index.html')

@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """ Login as owner """
    if current_user.is_authenticated:
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['user-name']
        password = request.form['user-password']
        if username is not None and password is not None:
            db_user = User.objects().first().username
            db_pass = User.objects().first().password
            if username == db_user and password == db_pass:
                loggedin_user = User.objects().first()
                login_user(loggedin_user)
                return redirect('/admin/dashboard')
            else:
                return redirect('/auth/login')
        else:
            return redirect('/auth/login')
    else:
        return send_from_directory('client/public', 'index.html')

@bp.route('/auth/logout', methods=['POST'])
def logout():
    """ Logout as owner """
    logout_user()
    return send_from_directory('client/public', 'index.html')