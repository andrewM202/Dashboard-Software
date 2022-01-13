from flask import jsonify, render_template, Blueprint, send_from_directory, request, redirect, jsonify
from models import PeopleWatch, PersonType, Countries, Organizations, OrganizationType, ArchiveCollections, ArchiveCollectionSettings, db
# from mongoengine import *
from bson import json_util, objectid
from os import environ

########################### Global Variables #####################################

bp = Blueprint("archive", __name__)

db_name = environ['MONGODB_DB']
collections = db.get_database(db_name).list_collection_names()

########################### Base Route #####################################

@bp.route("/admin/raw-archive")
def raw_archive():
    return send_from_directory('client/public', 'index.html')

########################### People #####################################

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

###########################  People Types #####################################

@bp.route("/admin/create-person-type", methods=['POST'])
def create_person_type():
    person_type_name = request.form['PersonTypeName']
    person_type_acronyms = request.form['PersonTypeAcronyms'].split(",")
    PersonType(
        person_type_name     = person_type_name,
        person_type_acronyms = person_type_acronyms,
    ).save()
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

###########################  Organization Types #####################################

@bp.route("/admin/create-organization-type", methods=['POST'])
def create_organization_type():
    organization_type_name = request.form['OrganizationTypeName']
    organization_type_acronyms = request.form['OrganizationTypeAcronyms'].split(",")
    OrganizationType(
        organ_type_name     = organization_type_name,
        organ_type_acronyms = organization_type_acronyms,
    ).save()
    return redirect('/admin/raw-archive')

########################### Archive Designer #####################################

@bp.route("/admin/archive-designer")
def archive_designer_home():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/archive-data/<collection>")
def retrieve_specific_archive_data(collection):
    """ Retrieve specific archive data """
    if(collection in collections):
        test_col = db.get_database(db_name).get_collection(collection)
        # return json.loads(json_util.dumps(test_col.find_one()))
        return json_util.dumps(test_col.find())
    else: 
        return "Invalid Collection"

@bp.route("/admin/archive-data/create-collection", methods=['POST'])
def create_archive_collection():
    """ Returns all of the collections for the archive 
    Goals:
    - Make it so input "set" lists should all be same length. For instance, 
    all the header_search_input lists should have same length, otherwise return error
    """
    try:
        # Add collection name to archive_collections collection
        ArchiveCollections(
            collection_name = request.form['CollectionName'],
            uploaded_data = False,
            base_collection = False
        ).save()

        ArchiveCollectionSettings(
            collection_name = request.form['CollectionName'],
            header_search_input_types = request.form['HeaderSearchInputTypes'].split(","),
            header_search_input_placeholders = request.form['HeaderSearchInputPlaceholders'].split(","),
            header_search_input_names = request.form['HeaderSearchInputNames'].split(","),

            header_card_subtitles = request.form['HeaderCardSubtitles'].split(","),
            header_card_amounts = request.form['HeaderCardAmounts'].split(","),
            header_card_increases = request.form['HeaderCardIncreases'].split(","),
            header_card_descriptions = request.form['HeaderCardDescriptions'].split(","),

            table_awaitdata = request.form['TableAwaitData'],
            table_headers = request.form['TableHeaders'].split(","),
            table_title = request.form['TableTitle'],
            table_deletion_url = request.form['TableDeletionURL'],
            table_refresh_url = request.form['TableRefreshURL'],
            table_updated_url = request.form['TableUpdatedURL'],
            table_update_form_names = request.form['TableDBFormNames'].split(","),
            table_db_field_names = "Placeholder".split(","),

            creationcard_awaitdata = request.form['CreationCardAwaitData'],
            creationcard_url = request.form['CreationCardURL'],
            creationcard_refreshurl = request.form['CreationCardRefreshURL'],
            creationcard_title = request.form['CreationCardTitle'],
            creationcard_flexdatalistdata = request.form['CreationCardFlexdatalistData'].split(","),
            creationcard_inputs = request.form['CreationCardInputs'].split(",")
        ).save()
    except Exception as e:
        return e
    return redirect('/admin/archive-designer')

@bp.route("/admin/archive-configuration")
def retrieve_archive_configuration():
    """ Returns configuration JSON for the archive """
    try:
        archive_settings = ArchiveCollectionSettings.objects()

        return_settings = {}
        for collection in archive_settings:
            dict_collection = dict(collection.to_mongo())
            dict_collection_keys = dict_collection.keys()
            return_settings[collection["collection_name"]] = {"CollectionName": collection["collection_name"],"HeaderSearchInputs": [], "Cards": [], "Table": {}, "CreationCard": {}}
            # All header search input fields should be same length
            for i in range(0, len(collection.header_search_input_types)):
                return_settings[collection["collection_name"]]["HeaderSearchInputs"].append({ "type": collection.header_search_input_types[i], "placeholder": collection.header_search_input_placeholders[i], "name": collection.header_search_input_names[i] })
            # All card input fields should be same length
            for i in range(0, len(collection.header_card_subtitles)):
                return_settings[collection["collection_name"]]["Cards"].append({ "subtitle": collection.header_card_subtitles[i], "amount": collection.header_card_subtitles[i], "increase": collection.header_card_increases[i], "description": collection.header_card_descriptions[i] })
            for key in dict_collection_keys:
                if key != "_id":
                    print(f"Key: {key}")
                    print(f"Value: {collection[key]}")
        return return_settings
    except Exception as e:
        return e

# Temp route to return archive_settings, will delete after testing finished
@bp.route("/admin/archive-config-collection")
def testing_route():
    """ Will delete this route later """
    archive_settings = ArchiveCollectionSettings.objects()
    return archive_settings.to_json()

@bp.route("/admin/archive-data/collections")
def retrieve_all_archive_data():
    """ Returns all of the collections for the archive """
    archive_collections = ArchiveCollections.objects().only('collection_name')
    return archive_collections.to_json()

# @bp.route("/admin/archive-data/")
# def retrieve_archive_collections():
#     """ Retrieve all archive data """
#     pass

@bp.route("/admin/archive-data/update", methods=["POST"])
def update_specific_archive_data():
    """ Update a specific archive data 
    Takes the collection and id data is in, as well as data
    in the form of a serialized array
    """
    collection_name = request.form['CollectionName']
    updateid = request.form['UpdateID']
    col = db.get_database(db_name).get_collection(collection_name)
    request_dict = request.form.to_dict()
    request_keys = request_dict.keys()
    update_json = {"$set": {} }
    for field in request_keys:
        if field != "CollectionName" and field != "UpdateID":
            update_json["$set"][field] = request_dict[field]
    col.update_one({"_id": objectid.ObjectId(updateid)}, update_json)
    return redirect('/admin/raw-archive')

@bp.route("/admin/archive-data/delete", methods=["POST"])
def delete_specific_archive_data():
    """ Delete a specific archive data 
    Takes the collection and id data is in
    """
    collection = request.form['CollectionName']
    id = request.form['DeletionID']
    col = db.get_database(db_name).get_collection(collection)
    col.delete_one({'_id': objectid.ObjectId(id)})
    return redirect('/admin/raw-archive')
    