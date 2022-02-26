import sys
sys.path.append("..")
from os import environ
from models import Role
from mongoengine import *

class SeedSubtables():
    def __init__(self):
        pass

    def SeedRoles(self):
        Role(
            name = "Admin",
            description = "Admin",
            permissions = []
        ).save()

        Role(
            name = "User",
            description = "User",
            permissions = []
        ).save()

        Role(
            name = "Guest",
            description = "Guest",
            permissions = []
        ).save()

def main():
    Sst = SeedSubtables()
    Sst.SeedRoles()

if __name__ == "__main__":
    main()
