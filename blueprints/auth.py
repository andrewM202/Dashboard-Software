from flask import render_template, redirect, Blueprint, \
    send_from_directory, request
from models import User, db
from flask_security import login_user, current_user, logout_user

########################### Global Variables #####################################

bp = Blueprint("auth", __name__)

########################### Base Route #####################################

@bp.route("/auth/register")
def register_page():
    return send_from_directory('client/public', 'index.html')

@bp.route("/login")
def redirect_security_login():
    return redirect('/auth/login')

@bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """ Login as owner """
    if current_user.is_authenticated:
        return redirect('/admin/dashboard')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is not None and password is not None:
            try:
                db_user = User.objects().first().email
                db_pass = User.objects().first().password
                if username == db_user and password == db_pass:
                    loggedin_user = User.objects().first()
                    print()
                    login_user(loggedin_user)
                    return redirect('/admin/dashboard')
                else:
                    return redirect('/auth/login')
            except Exception as e:
                return e
        else:
            return redirect('/auth/login')
    else:
        return send_from_directory('client/public', 'index.html')

@bp.route("/auth/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('/auth/login')
    else:
        return redirect('/auth/login')

@bp.route("/auth/register-user", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return redirect('/admin/dashboard')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usernamealready = None

        try:
            usernamealready = User.objects.get(username=username)
        except Exception as e:
            pass

        if usernamealready:
            error = "Sorry, that username is already present."
            return send_from_directory('client/public', 'index.html')
        else:
            user = User(
                email=username,
                password=password,
            ).save()

            login_user(user)

            db.session.add(user)
            db.session.commit()

            return redirect('/admin/dashboard')
    else:
        return send_from_directory('client/public', 'index.html')

