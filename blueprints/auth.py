from flask import render_template, Blueprint, send_from_directory

########################### Global Variables #####################################

bp = Blueprint("auth", __name__)

########################### Base Route #####################################

@bp.route("/auth/register")
def register():
    return send_from_directory('client/public', 'index.html')