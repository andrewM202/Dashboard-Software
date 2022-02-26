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
from json import loads

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
        return json_util.dumps(test_col.find())
    else: 
        return "Invalid Collection"

@bp.route("/admin/archive-data/edit-collection", methods=["POST"])
@login_required
def edit_archive_collection():
    try:
        # Throw error if any of the collection names or titles
        # are not set 
        if(len(request.form['collection_name']) == 0):
            return jsonify("Collection name must be set"), 400

        if(len(request.form['table_title']) == 0):
            return jsonify("Table title must be set"), 400

        if(len(request.form['creationcard_title']) == 0):
            return jsonify("Creation card title must be set"), 400

        # Check if this collection name already exists. If it does,
        # throw error if its the collection name of a different document to the 
        # one we are editing
        collections = db.get_database(db_name).collection_names()
        new_col_name = "gen_" + request.form['collection_name'].lower().replace(" ", "_")

        collection_id = request.form['collectionEditID']
        same_doc = ArchiveCollectionSettings.objects(id=collection_id)
        same_doc = True if len(same_doc) == 1 else False
        if(new_col_name in collections):
            # Throw error if collection already exists
            if same_doc == False:
                return jsonify("Collection name already exists"), 400
        
        # Check inputs are the same length
        h_c_s_length = len(request.form['header_card_subtitles'].split(",")) if request.form['header_card_subtitles'].split(",") != [''] else []
        h_c_a_length = len(request.form['header_card_amounts'].split(",")) if request.form['header_card_amounts'].split(",") != [''] else []
        h_c_i_length = len(request.form['header_card_increases'].split(",")) if request.form['header_card_increases'].split(",") != [''] else []
        h_c_d_length = len(request.form['header_card_descriptions'].split(",")) if request.form['header_card_descriptions'].split(",") != [''] else []
        if(h_c_s_length != h_c_a_length or h_c_s_length != h_c_i_length or h_c_s_length != h_c_d_length):
            return jsonify("Header card lengths must be equal"), 400

        # Check if header search and creation card input 
        # lengths are the same
        c_i_t_length = len(request.form['creationcard_input_types'].split(",")) if request.form['creationcard_input_types'].split(",") != [''] else []
        c_i_n_length = len(request.form['creationcard_input_names'].split(",")) if request.form['creationcard_input_names'].split(",") != [''] else []
        c_fd_length = len(request.form['creationcard_flexdatalistdata'].split(",")) if request.form['creationcard_flexdatalistdata'].split(",") != [''] else []
        c_ff_length = len(request.form['creationcard_flexdatalistfield'].split(",")) if request.form['creationcard_flexdatalistfield'].split(",") != [''] else []
        c_r_f_length = len(request.form['creationcard_required_field'].split(",")) if request.form['creationcard_required_field'].split(",") != [''] else []
        h_s_i_t_length = len(request.form['header_search_input_types'].split(",")) if request.form['header_search_input_types'].split(",") != [''] else []
        h_s_e_length = len(request.form['header_search_enabled'].split(",")) if request.form['header_search_enabled'].split(",") != [''] else []
        if(c_i_t_length != c_i_n_length or c_i_t_length != c_fd_length or c_i_t_length != c_ff_length or c_i_t_length != c_r_f_length or c_i_t_length != h_s_i_t_length or c_i_t_length != h_s_e_length):
            return jsonify("Creation card and header search lengths must be equal"), 400

        # If we pass all the checks, go on

        # Gen for auto-generated, non-default collection
        collection_name = "gen_" + request.form['collection_name'].lower().replace(" ", "_")

        # Normalize flex data fields
        flex_fields = [i.partition(": ")[2].lower().replace(" ", "_") if i != "None" else i for i in request.form['creationcard_flexdatalistfield'].split(",")]
        flex_data = ["gen_" + i.lower().replace(" ", "_") if i != "None" else i for i in request.form['creationcard_flexdatalistdata'].split(",")]

        ArchiveCollectionSettingsID = request.form['collectionEditID']
        # Get old collection name for update purposes
        oldColName = ArchiveCollectionSettings.objects(id=ArchiveCollectionSettingsID).only("collection_name")[0].collection_name

        # If adding new field, put a sample value in or remove old fields
        col = db.get_database(db_name).get_collection(collection_name)
        new_field_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")]
        old_field_names = ArchiveCollectionSettings.objects(id=ArchiveCollectionSettingsID).only("table_db_field_names")[0].table_db_field_names

        # Add sample value to old documents that don't have new field
        update_json = { "$set": {}}
        for new_field in new_field_names:
            if new_field not in old_field_names:
                update_query = {new_field: {"$exists": False}}
                update_json["$set"][new_field] = "Sample Value"
                col.update_many(update_query, update_json)

        col_settings = ArchiveCollectionSettings.objects()
        # Remove fields from document that no longer exists
        update_json = { "$set": {}}
        for old_field in old_field_names:
            if old_field not in new_field_names:
                # Remove that field from this collection
                col.update_many( { }, { '$unset': { old_field: 1 } } )

                # If this old field is a flexdatalist reference 
                # in another collection, make the field a regular input 
                # with no flexdatalist reference. Leave all values intact however
                col_settings = ArchiveCollectionSettings.objects()
                for setting in col_settings:
                    for i in range(0, len(setting.creationcard_flexdatalistdata)):
                        if(setting.creationcard_flexdatalistdata[i] == oldColName):
                            if(setting.creationcard_flexdatalistfield[i] == old_field):
                                # We found the old field, lets update it to none in given collection
                                new_listdata = setting.creationcard_flexdatalistdata
                                new_listdata[i] = "None"
                                new_listfield = setting.creationcard_flexdatalistfield
                                new_listfield[i] = "None"
                                ArchiveCollectionSettings.objects(id=setting.id).update(
                                    creationcard_flexdatalistdata = new_listdata,
                                    creationcard_flexdatalistfield = new_listfield
                                )

        ArchiveCollectionSettings.objects(id=ArchiveCollectionSettingsID).update(
            # Collection_name is db-friendly collection title
            collection_name = collection_name,
            # Title is just regular collection name
            collection_title = request.form['collection_name'],
            header_search_input_types = [i for i in request.form['header_search_input_types'].split(",")],
            # Commented out so the header input placeholders 
            # just equal the creation card input placeholders
            header_search_input_placeholders = [i for i in request.form['creationcard_input_names'].split(",")],#[i for i in request.form['HeaderSearchInputPlaceholders'].split(",")],
            # Header search input names are just the creation card ones
            header_search_input_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],
            header_search_enabled = [i for i in request.form['header_search_enabled'].split(",")],

            header_card_subtitles = [i for i in request.form['header_card_subtitles'].split(",")] if len(request.form['header_card_subtitles']) > 0 else [],
            header_card_amounts = [round(float(i), 2) for i in request.form['header_card_amounts'].split(",")] if len(request.form['header_card_amounts']) > 0 else [],
            header_card_increases = [round(float(i), 2) for i in request.form['header_card_increases'].split(",")] if len(request.form['header_card_increases']) > 0 else [],
            header_card_descriptions = [i for i in request.form['header_card_descriptions'].split(",")] if len(request.form['header_card_descriptions']) > 0 else [],

            table_title = request.form['table_title'],
            # The table field names are also just the creation card names
            table_db_field_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],

            creationcard_title = request.form['creationcard_title'],
            creationcard_flexdatalistdata = flex_data, 
            creationcard_flexdatalistfield = flex_fields, 
            creationcard_required_field = [i for i in request.form['creationcard_required_field'].split(",")],

            creationcard_input_types = [i for i in request.form['creationcard_input_types'].split(",")],
            # The names are just db-friendly placeholders
            creationcard_input_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],
            creationcard_input_placeholders = [i for i in request.form['creationcard_input_names'].split(",")],
        )

        # Add collection name to archive_collections collection
        ArchiveCollections.objects(collection_name=oldColName).update(
            collection_name = collection_name,
            uploaded_data = False,
            base_collection = False,
        )

        # Rename collection if they are different
        if oldColName != collection_name:
            db.get_database(db_name).get_collection(oldColName).rename(collection_name)
    
    except Exception as e:
        return redirect('/admin/archive-designer')

    return redirect('/admin/archive-designer')
        

@bp.route("/admin/archive-data/create-collection", methods=['POST'])
@login_required
def create_archive_collection():
    """ Create a collection for the archive
    Goals:
    - Make it so input "set" lists should all be same length. For instance, 
    all the header_search_input lists should have same length, otherwise return error
    """ 

    try:
        # Throw error if any of the collection names or titles
        # are not set 
        if(len(request.form['collection_name']) == 0):
            return jsonify("Collection name must be set"), 400

        if(len(request.form['table_title']) == 0):
            return jsonify("Table title must be set"), 400

        if(len(request.form['creationcard_title']) == 0):
            return jsonify("Creation card title must be set"), 400

        # Check if this collection name already exists
        collections = db.get_database(db_name).collection_names()
        new_col_name = "gen_" + request.form['collection_name'].lower().replace(" ", "_")
        if(new_col_name in collections):
            # Throw error if collection already exists
            return jsonify("Collection name already exists"), 400
        
        # Check inputs are the same length
        h_c_s_length = len(request.form['header_card_subtitles'].split(",")) if request.form['header_card_subtitles'].split(",") != [''] else []
        h_c_a_length = len(request.form['header_card_amounts'].split(",")) if request.form['header_card_amounts'].split(",") != [''] else []
        h_c_i_length = len(request.form['header_card_increases'].split(",")) if request.form['header_card_increases'].split(",") != [''] else []
        h_c_d_length = len(request.form['header_card_descriptions'].split(",")) if request.form['header_card_descriptions'].split(",") != [''] else []
        if(h_c_s_length != h_c_a_length or h_c_s_length != h_c_i_length or h_c_s_length != h_c_d_length):
            return jsonify("Header card lengths must be equal"), 400

        # Check if header search and creation card input 
        # lengths are the same
        c_i_t_length = len(request.form['creationcard_input_types'].split(",")) if request.form['creationcard_input_types'].split(",") != [''] else []
        c_i_n_length = len(request.form['creationcard_input_names'].split(",")) if request.form['creationcard_input_names'].split(",") != [''] else []
        c_fd_length = len(request.form['creationcard_flexdatalistdata'].split(",")) if request.form['creationcard_flexdatalistdata'].split(",") != [''] else []
        c_ff_length = len(request.form['creationcard_flexdatalistfield'].split(",")) if request.form['creationcard_flexdatalistfield'].split(",") != [''] else []
        c_r_f_length = len(request.form['creationcard_required_field'].split(",")) if request.form['creationcard_required_field'].split(",") != [''] else []
        h_s_i_t_length = len(request.form['header_search_input_types'].split(",")) if request.form['header_search_input_types'].split(",") != [''] else []
        h_s_e_length = len(request.form['header_search_enabled'].split(",")) if request.form['header_search_enabled'].split(",") != [''] else []
        if(c_i_t_length != c_i_n_length or c_i_t_length != c_fd_length or c_i_t_length != c_ff_length or c_i_t_length != c_r_f_length or c_i_t_length != h_s_i_t_length or c_i_t_length != h_s_e_length):
            return jsonify("Creation card and header search lengths must be equal"), 400

        # Check if lengths are more than 0
        if(c_i_t_length == 0):
            return jsonify("Creation card and header search inputs cannot be empty"), 400

        # All checks have passed, create collection    

        # Gen for auto-generated, non-default collection
        collection_name = "gen_" + request.form['collection_name'].lower().replace(" ", "_")

        # Normalize flex data fields
        flex_fields = [i.partition(": ")[2].lower().replace(" ", "_") if i != "None" else i for i in request.form['creationcard_flexdatalistfield'].split(",")]
        flex_data = ["gen_" + i.lower().replace(" ", "_") for i in request.form['creationcard_flexdatalistdata'].split(",")]

        ArchiveCollectionSettings(
            # Collection_name is db-friendly collection title
            collection_name = collection_name,
            # Title is just regular collection name
            collection_title = request.form['collection_name'],
            header_search_input_types = [i for i in request.form['header_search_input_types'].split(",")],
            # Commented out so the header input placeholders 
            # just equal the creation card input placeholders
            header_search_input_placeholders = [i for i in request.form['creationcard_input_names'].split(",")],
            # Header search input names are just the creation card ones
            header_search_input_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],
            header_search_enabled = [eval(i) for i in request.form['header_search_enabled'].split(",")],

            header_card_subtitles = [i for i in request.form['header_card_subtitles'].split(",")] if len(request.form['header_card_subtitles']) > 0 else [],
            header_card_amounts = [round(float(i), 2) for i in request.form['header_card_amounts'].split(",")] if len(request.form['header_card_amounts']) > 0 else [],
            header_card_increases = [round(float(i), 2) for i in request.form['header_card_increases'].split(",")] if len(request.form['header_card_increases']) > 0 else [],
            header_card_descriptions = [i for i in request.form['header_card_descriptions'].split(",")] if len(request.form['header_card_descriptions']) > 0 else [],

            # The await data is just the data from the collection. For now it should be blank
            # because when a collection is created it should be empty
            table_title = request.form['table_title'],
            # The table field names are also just the creation card names
            table_db_field_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],

            # Awaitdata is the data required for flexdatalist
            creationcard_title = request.form['creationcard_title'],
            creationcard_flexdatalistdata = flex_data, 
            creationcard_flexdatalistfield = flex_fields, 
            creationcard_required_field = [i for i in request.form['creationcard_required_field'].split(",")],

            creationcard_input_types = [i for i in request.form['creationcard_input_types'].split(",")],
            # The names are just db-friendly placeholders
            creationcard_input_names = [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")],
            creationcard_input_placeholders = [i for i in request.form['creationcard_input_names'].split(",")],
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

        for field in [i.lower().replace(" ", "_") for i in request.form['creationcard_input_names'].split(",")]:
            insert_json[field] = "Sample Value"
        col.insert_one(insert_json)
    
    except Exception as e:
        return redirect('/admin/archive-designer')
    
    return redirect('/admin/archive-designer')

@bp.route("/admin/archive-data/delete-collection", methods=["POST"])
@login_required
def delete_collection():
    """ Delete a collection """

    # get archive collection settings document ID
    acs_docid = request.form['collectionEditID']
    # get collection name of collection we are deleting
    collection_name = ArchiveCollectionSettings.objects(id=acs_docid)[0].collection_name

    # Make all inputs that reference a field from this deleted collection
    # as a flexdatalist input be regular inputs
    old_field_names = ArchiveCollectionSettings.objects(id=acs_docid).only("table_db_field_names")[0].table_db_field_names
    update_json = { "$set": {}}
    for old_field in old_field_names:
        # If this old field is a flexdatalist reference 
        # in another collection, make the field a regular input 
        # with no flexdatalist reference. Leave all values intact however
        col_settings = ArchiveCollectionSettings.objects()
        for setting in col_settings:
            for i in range(0, len(setting.creationcard_flexdatalistdata)):
                if(setting.creationcard_flexdatalistdata[i] == collection_name):
                    if(setting.creationcard_flexdatalistfield[i] == old_field):
                        # We found the old field, lets update it to none in given collection
                        new_listdata = setting.creationcard_flexdatalistdata
                        new_listdata[i] = "None"
                        new_listfield = setting.creationcard_flexdatalistfield
                        new_listfield[i] = "None"
                        ArchiveCollectionSettings.objects(id=setting.id).update(
                            creationcard_flexdatalistdata = new_listdata,
                            creationcard_flexdatalistfield = new_listfield
                        )

    # Delete from ArchiveCollectionSettings
    ArchiveCollectionSettings.objects(id=acs_docid).delete()   

    # Delete from ArchiveCollections
    ArchiveCollections.objects(collection_name=collection_name).delete()

    # Delete the actual collection from mongoengine
    col = db.get_database(db_name).get_collection(collection_name)
    col.drop()

    return redirect('/admin/archive-designer')

@bp.route("/admin/archive-configuration")
@login_required
def retrieve_archive_configuration():
    """ Returns configuration JSON for the archive """
    archive_settings = ArchiveCollectionSettings.objects()

    return_settings = {}
    for collection in archive_settings:
        dict_collection = dict(collection.to_mongo())
        dict_collection_keys = dict_collection.keys()
        ######### Collection Name #########
        return_settings[collection["collection_title"]] = {
            "CollectionName": collection["collection_name"],
            "HeaderSearchInputs": [], 
            "Cards": [], 
            "Table": {}, 
            "CreationCard": {}
        }
        ######### Header #########
        # All header search input fields should be same length
        for i in range(0, len(collection.header_search_input_types)):
            return_settings[collection["collection_title"]]["HeaderSearchInputs"].append({ 
                "type": collection.header_search_input_types[i], 
                "placeholder": collection.header_search_input_placeholders[i], 
                "name": collection.header_search_input_names[i] 
            })
        # All card input fields should be same length
        for i in range(0, len(collection.header_card_subtitles)):
            return_settings[collection["collection_title"]]["Cards"].append({ 
                "subtitle": collection.header_card_subtitles[i], 
                "amount": collection.header_card_amounts[i], 
                "increase": collection.header_card_increases[i], 
                "description": collection.header_card_descriptions[i] 
            })
        ######### Table #########
        return_settings[collection["collection_title"]]["Table"]["Data"] = [db.get_database(db_name).get_collection(collection["collection_name"]).find()]
        for i in range(0, len(collection.table_db_field_names)):
            return_settings[collection["collection_title"]]["Table"]["Headers"] = sorted([i.title().replace("_", " ") for i in collection.table_db_field_names])
            return_settings[collection["collection_title"]]["Table"]["DBFieldNames"] = sorted([i.lower().replace(' ', '_') for i in collection.table_db_field_names]) 
            return_settings[collection["collection_title"]]["Table"]["Title"] = collection.table_title
        ######### Creation Card #########
        return_settings[collection["collection_title"]]["CreationCard"]["Title"] = collection.creationcard_title
        return_settings[collection["collection_title"]]["CreationCard"]["Inputs"] = []
        for i in range(0, len(collection.creationcard_input_types)):
            if collection.creationcard_flexdatalistdata[i] == "gen_none" or collection.creationcard_flexdatalistdata[i] == "None":
                return_settings[collection["collection_title"]]["CreationCard"]["Inputs"].append({ 
                    "type": collection.creationcard_input_types[i], 
                    "placeholder": collection.creationcard_input_placeholders[i].title().replace("_", " "), 
                    "name": collection.table_db_field_names[i].lower().replace(' ', '_'), 
                    "required": collection.creationcard_required_field[i] == "true" 
                })
            else:
                return_settings[collection["collection_title"]]["CreationCard"]["Inputs"].append({ 
                    "type": collection.creationcard_input_types[i], 
                    "placeholder": collection.creationcard_input_placeholders[i].title().replace("_", " "), 
                    "name": collection.table_db_field_names[i].lower().replace(' ', '_'), 
                    "required": collection.creationcard_required_field[i] == "true", 
                    "flexdatalistdata": (db.get_database(db_name).get_collection(collection.creationcard_flexdatalistdata[i]).find({}, { f"{collection.creationcard_flexdatalistfield[i]}": 1}) ), 
                    "flexdatafields": collection.creationcard_flexdatalistfield[i], 
                    "flexdataid": str(uuid1()) 
                })
    return json_util.dumps(return_settings, indent=4, sort_keys=True)

# Temp route to return archive_settings, will delete after testing finished
@bp.route("/admin/archive-config-collection")
@login_required
def testing_route():
    """ Will delete this route later """
    archive_settings = ArchiveCollectionSettings.objects()
    return archive_settings.to_json()

@bp.route("/admin/archive-data/collection-title-pairs")
@login_required
def retrieve_collection_pairs():
    """ Returns the titles for all of the collections 
    in the archive """
    archive_collections = ArchiveCollections.objects().only('collection_name')

    # Get names of all collections
    collection_names = []
    for col in archive_collections:
        collection_names.append(col.collection_name)

    # Get titles based off of those names
    collection_titles = []
    for name in collection_names:
        col_title = ArchiveCollectionSettings.objects(collection_name=name).only('collection_title')[0]
        collection_titles.append(col_title.collection_title)

    # Make key pairs
    key_pairs = []
    for title in collection_titles:
        # Get field in each collection
        fields = ArchiveCollectionSettings.objects(collection_title=title)[0]
        for field in fields.header_search_input_placeholders:
            pair = f"{title}: {field}"
            key_pairs.append(pair)

    return json_util.dumps(key_pairs)

@bp.route("/admin/archive-data/collection-titles")
@login_required
def retrieve_collection_titles():
    """ Returns the titles for all of the collections 
    in the archive """
    archive_collections = ArchiveCollections.objects().only('collection_name')

    # Get names of all collections
    collection_names = []
    for col in archive_collections:
        collection_names.append(col.collection_name)

    # Get titles based off of those names
    collection_titles = []
    for name in collection_names:
        col_title = ArchiveCollectionSettings.objects(collection_name=name).only('collection_title')[0]
        collection_titles.append(col_title.collection_title)

    return json_util.dumps(collection_titles)

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

@bp.route("/admin/archive-data/search-data/", methods=["POST"])
@login_required
def search_archive():
    """ Retrieves search results for given collection """
    data = request.form.to_dict()
    data_keys = request.form.keys()
    collection = request.form['CollectionName']
    # print(data)
    col = db.get_database(db_name).get_collection(collection)

    # Build filter JSON
    filter_json = {
        "$and": [

        ]
    }

    for field in data_keys:
        if field != "CollectionName":# and data[field] != "":
            filter_json["$and"].append({
                field: {
                    "$regex": data[field], "$options": 'i'
                }
            })

    filtered_data = col.find(filter_json)

    # Can't return plain list as it will return empty list (glitch?)
    return_obj = {"data": [], "CollectionName": request.form['CollectionName']}
    for data in filtered_data:
        # Sort the results alphabetically so they match table headers
        data = {key: val for key, val in sorted(data.items(), key = lambda ele: ele[0])}
        return_obj["data"].append(data)

    return json_util.dumps(return_obj)
    
########################### Archive Upload #####################################

@bp.route("/admin/archive-upload")
@login_required
def archive_upload():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/archive-upload/upload-file", methods=["POST"])
@login_required
def archive_file_upload():
    data = request.form.to_dict()
    data_keys = request.form.keys()
    file = request.files['json_file']
    json = file.read().decode("utf-8")

    # Turn json string into python data structure
    json_obj = loads(json)
    # print(json_obj)

    # # Flatten the JSON and get all the keys
    flat_json = flatten_json(json_obj)
    # print(json_obj)
    # print(flat_json)
    unique_keys = []
    nums = "0123456789"
    for key in flat_json:
        temp = ""
        for letter in key:
            if letter not in nums:
                temp = temp + letter
        if(temp.startswith("_")):
            l = list(temp)
            l[0] = ""
            temp = "".join(l)
        if(temp.endswith("_")):
            l = list(temp)
            l[:-1] = ""
            temp = "".join(l)
        if(temp not in unique_keys):
            unique_keys.append(temp)
        # print(f"Key: {key} Value: {flat_json[key]}")

    print(unique_keys)
    print(len(unique_keys))

    return jsonify([json_obj, unique_keys])
    
def flatten_json(y):
    out = {}
  
    def flatten(x, name = ''):
          
        # If the Nested key-value 
        # pair is of dict type
        if type(x) is dict:
              
            for a in x:
                flatten(x[a], name + a + '_')
                  
        # If the Nested key-value
        # pair is of list type
        elif type(x) is list:
            i = 0
            if(all( isinstance(item, str) or isinstance(item, int) or isinstance(item, float) for item in x )):
                out[name[:-1]] = x
            else:
                for a in x:  
                    flatten(a, name + str(i) + '_')
                    i += 1
        else:
            out[name[:-1]] = x
  
    flatten(y)
    return out