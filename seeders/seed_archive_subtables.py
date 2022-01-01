import sys
sys.path.append("..")
from models import OrganizationType, PersonType
from mongoengine import *

class SeedSubtables():
    def __init__(self):
        self.organ_type_names = ["Non-Government Organization", "Corporation", "Government Agency"]
        self.people_type_names = ["Politician", "Government Worker", "Elite", "CEO", "Owner"]

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


def main():
    Sst = SeedSubtables()
    # Sst.SeedOrganizationTypes()
    # Sst.SeedPeopleTypes()

if __name__ == "__main__":
    main()