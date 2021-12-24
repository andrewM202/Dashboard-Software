from flask import render_template, Blueprint, send_from_directory
from models import People

bp = Blueprint("raw_archive", __name__)

@bp.route("/admin/raw-archive")
def raw_archive():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/raw-archive/people")
def raw_people():
    people = People.objects.all()
    return people;