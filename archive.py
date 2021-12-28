from flask import render_template, Blueprint, send_from_directory, request, redirect, jsonify
from models import PeopleWatch, Countries, Organizations

bp = Blueprint("archive", __name__)

@bp.route("/admin/raw-archive")
def raw_archive():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/create-person", methods=['POST'])
def create_person():
    first_name = request.form['FirstName']
    last_name = request.form['LastName']
    organization = request.form['Organizations'].split(",")
    title = request.form['Titles'].split(",")
    PeopleWatch(
        first_name    = first_name,
        last_name     = last_name,
        organizations = organization,
        titles        = title
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-person", methods=['POST'])
def delete_person():
    delete_id = request.form['DeletionID']
    PeopleWatch(id=delete_id).delete()
    return redirect('/admin/raw-archive')

@bp.route("/admin/people")
def raw_people():
    people = PeopleWatch.objects()
    return people.to_json()

@bp.route("/admin/countries")
def raw_countries():
    countries = Countries.objects()
    parsed_countries = []
    for country in countries:
        new_country = {}
        # Country Name
        new_country["country_name"] = country.name['official']
        # Country Currencies
        country_currencies_list = list(country.currencies.values())
        country_currencies = []
        for currency in country_currencies_list:
            country_currencies.append(currency['name'])
        new_country["currencies"] = country_currencies 
        # Country Capital
        country_capitals = ""
        for capital in country.capital:
            country_capitals += " " + capital
        country_capitals = country_capitals.strip()
        new_country["country_capital"] = country_capitals
        # Country Subregion
        new_country["country_subregion"] = country.subregion
        # Country Languages
        country_languages = ""
        for language in country.languages.values():
            country_languages += " " + language
        country_languages = country_languages.strip().replace(" ", ", ")
        new_country["country_languages"] = country_languages
        # Country Latitude, Longitude
        new_country["country_latlng"] = country.latlng
        # Country Landlocked
        new_country["country_landlocked"] = country.landlocked
        # Country Area
        new_country["country_area"] = country.area
        # Country Population
        new_country["country_population"] = country.population
        # Append completed object to list
        parsed_countries.append(new_country)
    return jsonify(parsed_countries)

@bp.route("/admin/organizations")
def raw_organizations():
    organizations = Organizations.objects()
    return organizations.to_json()

@bp.route("/admin/create-organization", methods=['POST'])
def create_organization():
    name = request.form['Name']
    opinions = request.form['Opinions'].split(",")
    affiliations = request.form['Affiliations'].split(",")
    Organizations(
        name         = name,
        opinions     = opinions,
        affiliations = affiliations
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-organization", methods=['POST'])
def delete_organization():
    delete_id = request.form['DeletionID']
    print(delete_id)
    Organizations(id=delete_id).delete()
    return redirect('/admin/raw-archive')