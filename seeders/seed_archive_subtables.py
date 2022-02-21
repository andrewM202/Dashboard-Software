import sys
sys.path.append("..")
from models import ArchiveCollections, ArchiveCollectionSettings
from mongoengine import *

class SeedSubtables():
    def __init__(self):
        pass

    def SeedArchiveCollections(self):
        db_name = environ['MONGODB_DB']
        collections = db.get_database(db_name).list_collection_names()

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


def main():
    Sst = SeedSubtables()
    # Sst.SeedOrganizationTypes()
    # Sst.SeedPeopleTypes()
    Sst.SeedArchiveCollections()

if __name__ == "__main__":
    main()
