from flask import render_template, Blueprint, send_from_directory

bp = Blueprint("misc", __name__)

# Path for our main Svelte page
@bp.route("/")
def base():
    return send_from_directory('client/public', 'index.html')
    # return redirect('/admin/dashboard')

@bp.route("/landing")
def landing():
    return send_from_directory('client/public', 'index.html')

@bp.route("/profile")
def profile():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@bp.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@bp.route("/rand")
def hello():
    return str(random.randint(0, 100))