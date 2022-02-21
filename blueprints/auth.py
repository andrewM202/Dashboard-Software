from flask import jsonify, render_template, redirect, Blueprint, \
    send_from_directory, request
from models import User, db, pwd_context, user_datastore
from flask_security import login_user, current_user, logout_user
from passlib.context import CryptContext # Password hashing
from flask_wtf.csrf import CSRFProtect, generate_csrf

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
                # Verify password with hashing
                if username == db_user and pwd_context.verify(password, db_pass):
                    loggedin_user = User.objects().first()
                    print()
                    login_user(loggedin_user)
                    return '/admin/dashboard'
                else:
                    return '/auth/login'
            except Exception as e:
                return e
        else:
            return '/auth/login'
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
        usernamealready = True if len(User.objects(email=username)) > 0 else False

        if usernamealready:
            return "Sorry, that username is already present.", 404
        else:
            user = User(
                email=username,
                password=pwd_context.hash(password), # Hash password
            ).save()
            
            # user_datastore.create_user(
            #     email=username,
            #     password=pwd_context.hash(password), # Hash password
            # )

            login_user(user)

            return '/admin/dashboard'
    else:
        return "Please send a valid request", 404


# Get CSRF token
@bp.route("/auth/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response