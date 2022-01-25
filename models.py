from mongoengine import *
from os import environ
from flask_login import UserMixin, LoginManager
from flask_security import RoleMixin, MongoEngineUserDatastore
from passlib.context import CryptContext # Password hashing

# Connect to MongoDB
db = connect(host = environ['MONGODB_HOST'])   

# flask-login initialization
login = LoginManager()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")

########################### Raw Archive #####################################

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
    collection_title = StringField(required=True)

    header_search_input_types = ListField()
    header_search_input_placeholders = ListField()
    header_search_input_names = ListField()
    header_search_enabled = BooleanField(required=True)

    header_card_subtitles = ListField()
    header_card_amounts = ListField()
    header_card_increases = ListField()
    header_card_descriptions = ListField()

    # Table fields
    table_title = StringField(required=True)
    table_update_form_names = ListField()
    table_db_field_names = ListField(required=True)
    
    # Creation card fields
    creationcard_title = StringField(required=True)
    creationcard_flexdatalistdata = ListField()
    creationcard_flexdatalistfield = ListField()
    creationcard_required_field = ListField()

    # Creation card inputs
    creationcard_input_types = ListField()
    # These are the actual names in the database
    creationcard_input_names = ListField()
    # These are the names that appear as the title of the creation card
    creationcard_input_placeholders = ListField()

########################### Authentication #####################################

class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)
    permissions = StringField(max_length=255)

class User(Document, UserMixin):
    """ Login Information """
    email = StringField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
