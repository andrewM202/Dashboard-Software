from mongoengine import *
from os import environ

# Connect to MongoDB
db = connect(host = environ['MONGODB_HOST'])   

class PeopleWatch(Document):
    """ People """
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    person_type = ListField(required=True)
    organizations = ListField()
    titles = ListField()
    opinions = ListField()

class PersonType(Document):
    """ Types of People """
    person_type_name = StringField(required=True)
    person_type_acronyms = ListField()

class Countries(Document):
    """ Countries """
    name = StringField(required=True)
    currencies = StringField(required=True)
    capital = ListField(required=True)
    subregion = StringField(required=True)
    languages = StringField(required=True)
    latlng = ListField(required=True)
    landlocked = BooleanField(required=True)
    area = IntField(required=True)
    population = IntField(required=True)

class Organizations(Document):
    """ Organizations """
    name = StringField(required=True, unique=True)
    organ_type = StringField(required=True)
    opinions = ListField()
    affiliations = ListField()

class OrganizationType(Document):
    """ Types of organizations """
    organ_type_name = StringField(required=True)
    organ_type_acronyms = ListField()

class ArchiveCollections(Document):
    """ Holds all of the collections created for the archive """
    collection_name = StringField(required=True)
    uploaded_data = BooleanField(required=True)
    base_collection = BooleanField(required=True)

class ArchiveCollectionSettings(Document):
    """ Configuration settings for archive collections """
    # References ArchiveCollections.collection_name
    collection_name = StringField(required=True) 
    header_search_inputs = ListField()
    cards = ListField()
    # Table fields
    table_awaitdata = StringField()
    table_headers = ListField()
    table_title = StringField()
    table_deletion_url = StringField()
    table_refresh_url = StringField()
    table_updated_url = StringField()
    table_update_form_names = ListField()
    table_db_field_names = ListField()
    # Creation card fields
    creationcard_awaitdata = StringField()
    creationcard_url = StringField()
    creationcard_refreshurl = StringField()
    creationcard_title = StringField()
    creationcard_flexdatalistdata = ListField()
    creationcard_inputs = ListField()
