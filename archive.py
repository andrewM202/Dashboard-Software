from flask import render_template, Blueprint, send_from_directory, request, redirect
from models import PeopleWatch, Countries

bp = Blueprint("archive", __name__)

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

@bp.route("/admin/people")
def raw_people():
    people = PeopleWatch.objects()
    return people.to_json()

@bp.route("/admin/countries")
def raw_countries():
    countries = Countries.objects()
    return countries.to_json()

@bp.route("/admin/organizations")
def raw_organizations():
    people = PeopleWatch.objects()
    return people.to_json()
