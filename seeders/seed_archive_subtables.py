import sys
sys.path.append("..")
from models import OrganizationType, PersonType, ArchiveCollections
from mongoengine import *

class SeedSubtables():
    def __init__(self):
        self.organ_type_names = ["Non-Government Organization", "Corporation", "Government Agency"]
        self.people_type_names = ["Politician", "Government Worker", "Elite", "CEO", "Owner"]
        self.collection_names = ['organization_type', 'countries', 'organizations', 'person_type', 'people_watch']

    def SeedOrganizationTypes(self):
        for organ_type_name in self.organ_type_names:
            OrganizationType(
                organ_type_name = organ_type_name
            ).save()
    
    def SeedPeopleTypes(self):
        for person_type_name in self.people_type_names:
            PersonType(
                person_type_name = person_type_name
            ).save()

    def SeedArchiveCollections(self):
        for collection_name in self.collection_names:
            ArchiveCollections(
                collection_name = collection_name,
                uploaded_data   = 0,
                base_collection = 1
            ).save()


def main():
    Sst = SeedSubtables()
    # Sst.SeedOrganizationTypes()
    # Sst.SeedPeopleTypes()
    Sst.SeedArchiveCollections()

if __name__ == "__main__":
    main()
