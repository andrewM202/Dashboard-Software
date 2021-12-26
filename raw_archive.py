from flask import render_template, Blueprint, send_from_directory, request, redirect
from models import PeopleWatch

bp = Blueprint("raw_archive", __name__)

@bp.route("/admin/raw-archive")
def raw_archive():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/create-person", methods=['POST'])
def create_person():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    organization = list(request.form['organization'])
    title = list(request.form['title'])
    PeopleWatch(
        first_name    = first_name,
        last_name     = last_name,
        organizations = organization,
        titles        = title
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/raw-archive/people")
def raw_people():
    people = PeopleWatch.objects()
    return people.to_json()