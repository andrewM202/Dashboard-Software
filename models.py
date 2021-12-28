from mongoengine import *
from os import environ

# Connect to MongoDB
db = connect(host = environ['MONGODB_HOST'])   

class PeopleWatch(Document):
    """ People """
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    organizations = ListField()
    titles = ListField()
    opinions = ListField()

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
    opinions = ListField()
    affiliations = ListField()