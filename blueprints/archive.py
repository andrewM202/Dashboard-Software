from flask import render_template, Blueprint, send_from_directory, request, redirect, jsonify
from models import PeopleWatch, PersonType, Countries, Organizations, OrganizationType

bp = Blueprint("archive", __name__)

@bp.route("/admin/raw-archive")
def raw_archive():
    return send_from_directory('client/public', 'index.html')

###########################  People #####################################

@bp.route("/admin/create-person", methods=['POST'])
def create_person():
    first_name = request.form['FirstName']
    last_name = request.form['LastName']
    person_type = request.form['PersonType'].split(",")
    organization = request.form['Organizations'].split(",")
    titles = request.form['Titles'].split(",")
    opinions = request.form['Opinions'].split(",")
    PeopleWatch(
        first_name    = first_name,
        last_name     = last_name,
        person_type   = person_type,
        organizations = organization,
        titles        = titles,
        opinions      = opinions
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-person", methods=['POST'])
def delete_person():
    delete_id = request.form['DeletionID']
    PeopleWatch(id=delete_id).delete()
    return redirect('/admin/raw-archive')

@bp.route("/admin/update-person", methods=['POST'])
def update_person():
    update_id = request.form['UpdateID']
    PeopleWatch(id=update_id).update(
        first_name    = request.form['FirstName'], 
        last_name     = request.form['LastName'],
        person_type   = request.form['PersonType'].split(","),
        organizations = request.form['Organizations'].split(","),
        titles        = request.form['Titles'].split(","),
        opinions      = request.form['Opinions'].split(",")
    )
    return redirect('/admin/raw-archive')

@bp.route("/admin/people")
def raw_people():
    people = PeopleWatch.objects()
    return people.to_json()

###########################  People Types #####################################

@bp.route("/admin/person-types")
def people_types():
    person_types = PersonType.objects()
    return person_types.to_json()

@bp.route("/admin/create-person-type", methods=['POST'])
def create_person_type():
    person_type_name = request.form['PersonTypeName']
    person_type_acronyms = request.form['PersonTypeAcronyms'].split(",")
    PersonType(
        person_type_name     = person_type_name,
        person_type_acronyms = person_type_acronyms,
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-person-type", methods=['POST'])
def delete_person_type():
    delete_id = request.form['DeletionID']
    PersonType(id=delete_id).delete()
    return redirect('/admin/raw-archive')

@bp.route("/admin/update-person-types", methods=['POST'])
def update_person_type():
    update_id = request.form['UpdateID']
    PersonType(id=update_id).update(
        person_type_name     = request.form['PersonTypeName'], 
        person_type_acronyms = request.form['PersonTypeAcronyms'].split(","),
    )
    return redirect('/admin/raw-archive')

###########################  Countries #####################################

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
        new_country["country_currencies"] = country_currencies 
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
        new_country["country_landlocked"] = "Yes" if country.landlocked else "No"
        # Country Area
        new_country["country_area"] = country.area
        # Country Population
        new_country["country_population"] = country.population
        # Append completed object to list
        parsed_countries.append(new_country)
    return jsonify(parsed_countries)

###########################  Organizations #####################################

@bp.route("/admin/organizations")
def raw_organizations():
    organizations = Organizations.objects()
    return organizations.to_json()

@bp.route("/admin/create-organization", methods=['POST'])
def create_organization():
    name = request.form['Name']
    organization_type = request.form['OrganizationType']
    opinions = request.form['Opinions'].split(",")
    affiliations = request.form['Affiliations'].split(",")
    Organizations(
        name         = name,
        organ_type   = organization_type,
        opinions     = opinions,
        affiliations = affiliations
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-organization", methods=['POST'])
def delete_organization():
    delete_id = request.form['DeletionID']
    Organizations(id=delete_id).delete()
    return redirect('/admin/raw-archive')

@bp.route("/admin/update-organization", methods=['POST'])
def update_organization():
    update_id = request.form['UpdateID']
    Organizations(id=update_id).update(
        name         = request.form['Name'], 
        organ_type   = request.form['OrganizationType'],
        opinions     = request.form['Opinions'].split(","),
        affiliations = request.form['Affiliations'].split(",")
    )
    return redirect('/admin/raw-archive')

###########################  Organization Types #####################################

@bp.route("/admin/organization-types")
def organization_types():
    organization_types = OrganizationType.objects()
    return organization_types.to_json()

@bp.route("/admin/create-organization-type", methods=['POST'])
def create_organization_type():
    organization_type_name = request.form['OrganizationTypeName']
    organization_type_acronyms = request.form['OrganizationTypeAcronyms'].split(",")
    OrganizationType(
        organ_type_name     = organization_type_name,
        organ_type_acronyms = organization_type_acronyms,
    ).save()
    return redirect('/admin/raw-archive')

@bp.route("/admin/delete-organization-type", methods=['POST'])
def delete_organization_type():
    delete_id = request.form['DeletionID']
    OrganizationType(id=delete_id).delete()
    return redirect('/admin/raw-archive')

@bp.route("/admin/update-organization-types", methods=['POST'])
def update_organization_type():
    update_id = request.form['UpdateID']
    OrganizationType(id=update_id).update(
        organ_type_name     = request.form['OrganizationTypeName'], 
        organ_type_acronyms = request.form['OrganizationTypeAcronyms'].split(","),
    )
    return redirect('/admin/raw-archive')