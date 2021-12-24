from mongoengine import *
from os import environ

# Connect to MongoDB
db = connect(host = environ['MONGODB_HOST'])   

class People(Document):
    """ People """
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    organizations = ListField()
    titles = ListField()