from flask import jsonify, abort, Response, render_template, Blueprint, send_from_directory, request, redirect, jsonify
from models import PeopleWatch, PersonType, Countries, Organizations, OrganizationType, ArchiveCollections, ArchiveCollectionSettings, db
# from mongoengine import *
from bson import json_util, objectid
from os import environ
from uuid import uuid1
# regex
from re import search
# from flask_login import current_user
from flask_security import login_required, current_user

########################### Global Variables #####################################

bp = Blueprint("archive", __name__)

db_name = environ['MONGODB_DB']
collections = db.get_database(db_name).list_collection_names()

########################### Base Route #####################################

@bp.route("/admin/raw-archive")
@login_required
def raw_archive():
    return send_from_directory('client/public', 'index.html')

###########################  Countries #####################################

@bp.route("/admin/countries")
@login_required
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

########################### Archive Designer #####################################

@bp.route("/admin/archive-designer")
@login_required
def archive_designer_home():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/archive-data/<collection>")
@login_required
def retrieve_specific_archive_data(collection):
    """ Retrieve specific archive data """
    if(collection in collections):
        test_col = db.get_database(db_name).get_collection(collection)
        # return json.loads(json_util.dumps(test_col.find_one()))
        return json_util.dumps(test_col.find())
    else: 
        return "Invalid Collection"

@bp.route("/admin/archive-data/create-collection", methods=['POST'])
@login_required
def create_archive_collection():
    """ Returns all of the collections for the archive 
    Goals:
    - Make it so input "set" lists should all be same length. For instance, 
    all the header_search_input lists should have same length, otherwise return error
    """ 

    collection_name = request.form['CollectionName'].lower().replace(" ", "_")

    ArchiveCollectionSettings(
        # Collection_name is db-friendly collection title
        collection_name = collection_name,
        # Title is just regular collection name
        collection_title = request.form['CollectionName'],
        header_search_input_types = [i for i in request.form['HeaderSearchInputTypes'].split(",")],
        header_search_input_placeholders = [i for i in request.form['HeaderSearchInputPlaceholders'].split(",")],
        # Header search input names are just the creation card ones
        header_search_input_names = [i.lower().replace(" ", "_") for i in request.form['CreationCardInputNames'].split(",")],

        header_card_subtitles = [i for i in request.form['HeaderCardSubtitles'].split(",")],
        header_card_amounts = [round(float(i), 2) for i in request.form['HeaderCardAmounts'].split(",")],
        header_card_increases = [round(float(i), 2) for i in request.form['HeaderCardIncreases'].split(",")],
        header_card_descriptions = [i for i in request.form['HeaderCardDescriptions'].split(",")],

        # The await data is just the data from the collection. For now it should be blank
        # because when a collection is created it should be empty
        table_title = request.form['TableTitle'],
        table_update_form_names = list(),
        # The table field names are also just the creation card names
        table_db_field_names = [i.lower().replace(" ", "_") for i in request.form['CreationCardInputNames'].split(",")],

        # Awaitdata is the data required for flexdatalist
        creationcard_title = request.form['CreationCardTitle'],
        creationcard_flexdatalistdata = [i for i in request.form['CreationCardFlexdatalistData'].split(",")],
        creationcard_flexdatalistfield = [i.partition(" ")[2] for i in request.form['CreationCardFlexdatalistField'].split(",")],
        creationcard_required_field = [i for i in request.form['CreationCardRequiredField'].split(",")],

        creationcard_input_types = [i for i in request.form['CreationCardInputTypes'].split(",")],
        # The names are just db-friendly placeholders
        creationcard_input_names = [i.lower().replace(" ", "_") for i in request.form['CreationCardInputNames'].split(",")],
        creationcard_input_placeholders = [i.lower().replace(" ", "_") for i in request.form['CreationCardInputNames'].split(",")],
    ).save()

    # Add collection name to archive_collections collection
    ArchiveCollections(
        collection_name = collection_name,
        uploaded_data = False,
        base_collection = False,
    ).save()

    # Create collection
    newcol = db.get_database(db_name)[collection_name]
    col = db.get_database(db_name).get_collection(collection_name)
    insert_json = {}
    # for field in request.form['CreationCardInputNames'].split(","):
    for field in [i.lower().replace(" ", "_") for i in request.form['CreationCardInputNames'].split(",")]:
        insert_json[field] = "Sample Value"
    col.insert_one(insert_json)

    return redirect('/admin/archive-designer')

@bp.route("/admin/archive-configuration")
@login_required
def retrieve_archive_configuration():
    """ Returns configuration JSON for the archive """
    # try:
    archive_settings = ArchiveCollectionSettings.objects()

    return_settings = {}
    for collection in archive_settings:
        dict_collection = dict(collection.to_mongo())
        dict_collection_keys = dict_collection.keys()
        ######### Collection Name #########
        return_settings[collection["collection_title"]] = {"CollectionName": collection["collection_name"],"HeaderSearchInputs": [], "Cards": [], "Table": {}, "CreationCard": {}}
        ######### Header #########
        # All header search input fields should be same length
        for i in range(0, len(collection.header_search_input_types)):
            return_settings[collection["collection_title"]]["HeaderSearchInputs"].append({ "type": collection.header_search_input_types[i], "placeholder": collection.header_search_input_placeholders[i], "name": collection.header_search_input_names[i] })
        # All card input fields should be same length
        for i in range(0, len(collection.header_card_subtitles)):
            return_settings[collection["collection_title"]]["Cards"].append({ "subtitle": collection.header_card_subtitles[i], "amount": collection.header_card_amounts[i], "increase": collection.header_card_increases[i], "description": collection.header_card_descriptions[i] })
        ######### Table #########
        return_settings[collection["collection_title"]]["Table"]["Data"] = [db.get_database(db_name).get_collection(collection["collection_name"]).find()]
        for i in range(0, len(collection.table_db_field_names)):
            return_settings[collection["collection_title"]]["Table"]["Headers"] = sorted([i.title().replace("_", " ") for i in collection.table_db_field_names])
            return_settings[collection["collection_title"]]["Table"]["DBFieldNames"] = [i.lower().replace(' ', '_') for i in collection.table_db_field_names] 
            return_settings[collection["collection_title"]]["Table"]["Title"] = collection.table_title
        ######### Creation Card #########
        return_settings[collection["collection_title"]]["CreationCard"]["Title"] = f"Create {collection.collection_title}"
        return_settings[collection["collection_title"]]["CreationCard"]["Inputs"] = []
        for i in range(0, len(collection.creationcard_input_types)):
            if collection.creationcard_flexdatalistdata[i] == "None":
                return_settings[collection["collection_title"]]["CreationCard"]["Inputs"].append({ "type": collection.creationcard_input_types[i], "placeholder": collection.creationcard_input_placeholders[i].title().replace("_", " "), "name": collection.table_db_field_names[i].lower().replace(' ', '_'), "required": collection.creationcard_required_field[i] == "true" })
            else:
                return_settings[collection["collection_title"]]["CreationCard"]["Inputs"].append({ "type": collection.creationcard_input_types[i], "placeholder": collection.creationcard_input_placeholders[i].title().replace("_", " "), "name": collection.table_db_field_names[i].lower().replace(' ', '_'), "required": collection.creationcard_required_field[i] == "true", "flexdatalistdata": (db.get_database(db_name).get_collection(collection.creationcard_flexdatalistdata[i]).find({}, { f"{collection.creationcard_flexdatalistfield[i]}": 1}) ), "flexdatafields": collection.creationcard_flexdatalistfield[i], "flexdataid": str(uuid1()) })
    return json_util.dumps(return_settings, indent=4, sort_keys=True)
    # except Exception as e:
    #     return e

# Temp route to return archive_settings, will delete after testing finished
@bp.route("/admin/archive-config-collection")
@login_required
def testing_route():
    """ Will delete this route later """
    archive_settings = ArchiveCollectionSettings.objects()
    return archive_settings.to_json()

@bp.route("/admin/archive-collection-key-pairs")
@login_required
def archive_collection_keys():
    """ Will delete this route later """
    key_pairs = {}
    key_pairs["KeyPairs"] = []
    collections = ArchiveCollections.objects().only('collection_name')
    for collection in collections:
        col = db.get_database(db_name).get_collection(collection.collection_name)
        doc = col.find_one()
        # key_pairs[collection.collection_name] = []
        doc_key_values = doc.items()
        for key_value_pair in doc_key_values:
            if key_value_pair[0] != "_id":
                # key_pairs[collection.collection_name].append(f"{collection.collection_name}: {key_value_pair[0]}")
                key_pairs["KeyPairs"].append(f"{collection.collection_name}: {key_value_pair[0]}")
    return key_pairs

@bp.route("/admin/archive-data/collections")
@login_required
def retrieve_all_archive_data():
    """ Returns all of the collections for the archive """
    archive_collections = ArchiveCollections.objects().only('collection_name')
    return archive_collections.to_json()

@bp.route("/admin/archive-data/update", methods=["POST"])
@login_required
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
@login_required
def delete_specific_archive_data():
    """ Delete a specific archive data 
    Takes the collection and id data is in
    """
    collection = request.form['CollectionName']
    id = request.form['DeletionID']
    col = db.get_database(db_name).get_collection(collection)
    if col.count() > 1:
        col.delete_one({'_id': objectid.ObjectId(id)})
    else: 
        return abort(Response("Cannot delete last value in collection"))
    return redirect('/admin/raw-archive')

@bp.route("/admin/archive-data/create", methods=["POST"])
@login_required
def create_specific_archive_data():
    """ Creates a specific archive data point
    Takes the collection and id data is in
    """
    request_dict = request.form.to_dict()
    request_keys = request_dict.keys()
    collection = request.form['CollectionName']
    col = db.get_database(db_name).get_collection(collection)

    creation_dict = {}

    for key in request_keys:
        # Make sure no flexdatalist- fields get added with regex
        if key != "CollectionName" and (bool(search(r'\bflexdatalist-\b', key)) != True):
            creation_dict[key] = request_dict[key]
    col.insert_one(creation_dict)
    return redirect('/admin/raw-archive')
    
    