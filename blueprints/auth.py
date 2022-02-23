from flask import jsonify, render_template, redirect, Blueprint, \
    send_from_directory, request
from models import User, db, pwd_context, user_datastore, Role
from flask_security import login_user, current_user, logout_user, login_required
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
                db_user = User.objects(email=username).first().email
                db_pass = User.objects(email=username).first().password
                db_active = User.objects(email=username).first().active
                # Verify password with hashing
                if username == db_user and pwd_context.verify(password, db_pass) and db_active:
                    loggedin_user = User.objects().first()
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
            print("Sorry, that username is already present.")
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
            # login_user(user)

            return '/admin/dashboard'
    else:
        print("Please send a valid request")
        return "Please send a valid request", 404


# Get CSRF token
@bp.route("/auth/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response

@login_required
@bp.route("/auth/unapproved-users", methods=["GET"])
def unapproved_users():
    """ Returns all of the users that have 
    not gone through the approval process """
    users = User.objects(active=False).only("email").to_json()
    return users

@login_required
@bp.route("/auth/approve-user", methods=["POST"])
def approve_user():
    """ Approve a user """
    data = request.form.to_dict()
    data_keys = request.form.keys()

    print(data)
    print(Role.objects(name=data["role"])[0])

    User.objects(email=data["username"]).update(
        email=data["username"],
        roles=Role.objects(name=data["role"]),
        active=True,
    )

    return ""

@login_required
@bp.route("/auth/deny-user", methods=["POST"])
def deny_user():
    """ Deny a user """
    data = request.form.to_dict()
    data_keys = request.form.keys()

    User.objects(email=data["username"]).delete()
    
    return ""