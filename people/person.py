from mongoengine import *
from sys import argv

def add_person():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")

    class PeopleWatch(Document):
        first_name = StringField(required=True)
        last_name = StringField(required=True)
        organizations = ListField()
        titles = ListField()

    first_name = input('---First Name---\n> ').strip().title()
    last_name = input('---Last Name---\n> ').strip().title()
    organizations = input('---Organizations (Comma Separated)---\n> ').strip().title().split(", ")
    organizations = [organization.strip(' ') for organization in organizations]
    titles = input('---Titles (Comma Separated)---\n> ').strip().title().split(",")
    titles = [title.strip(' ') for title in titles]

    # See if this person alreayd exists
    person = PeopleWatch.objects(first_name = first_name, last_name = last_name)
    if len(person) == 0:
        PeopleWatch(
            first_name    = first_name,
            last_name     = last_name,
            organizations = organizations,
            titles        = titles
        ).save()

        print(f"{first_name} {last_name} was added.")
    else:
        person = person.first()
        print(f"""
This Person Was Already Added.

Field Values:
- First Name: {person.first_name}
- Last Name: {person.last_name}
- Organizations: {person.organizations}
- Titles: {person.titles}
    """)

def update_person():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")

    class PeopleWatch(Document):
        first_name = StringField(required=True)
        last_name = StringField(required=True)
        organizations = ListField()
        titles = ListField()

    person_to_update = input("Person to update? First and Last Name. \n> ").title().split(" ")
    fname = person_to_update[0] # First name is first index
    lname = person_to_update[1] # Last name is last index
    person_to_update = PeopleWatch.objects(first_name = fname, last_name = lname).first()
    print(f"""
Current Field Values:
- First Name: {person_to_update.first_name}
- Last Name: {person_to_update.last_name}
- Organizations: {person_to_update.organizations}
- Titles: {person_to_update.titles}
    """)

    update_field = ""
    while update_field not in ['1', '2', '3', '4']:
        update_field = input(
"""Update Which Field:
1. First Name
2. Last Name 
3. Organizations 
4. Titles
> """)

    new_value = input("What Would You Like to Update it To?\n> ").strip().title()
    old_value_fname = fname
    old_value_lname = lname
    if update_field == "1":
        person_to_update.first_name = new_value
        fname = new_value
    elif update_field == "2": 
        person_to_update.last_name = new_value
        lname = new_value
    elif update_field == "3":
        new_value = new_value.split(",")
        new_value = [i.strip(' ') for i in new_value]
        person_to_update.organizations = new_value.split(",")
    elif update_field == "4":
        new_value = new_value.split(",")
        new_value = [i.strip(' ') for i in new_value]
        print(new_value)
        person_to_update.titles = new_value

    person_to_update.save()
    print(f"\n(Previously) {old_value_fname} {old_value_lname} Was Updated!")

    person_to_update = PeopleWatch.objects(first_name = fname, last_name = lname).first()
    print(f"""
New Field Values:
- First Name: {person_to_update.first_name}
- Last Name: {person_to_update.last_name}
- Organizations: {person_to_update.organizations}
- Titles: {person_to_update.titles}""")

def delete_person():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")

    class PeopleWatch(Document):
        first_name = StringField(required=True)
        last_name = StringField(required=True)
        organizations = ListField()
        titles = ListField()

    person_to_delete = input("Person to Delete? First and Last Name.\n> ").title().split(" ")
    fname = person_to_delete[0] # First name is first index
    lname = person_to_delete[1] # Last name is last index
    person_to_delete = PeopleWatch.objects(first_name = fname, last_name = lname).first()

    print(f"""
This Person's Values:
- First Name: {person_to_delete.first_name}
- Last Name: {person_to_delete.last_name}
- Organizations: {person_to_delete.organizations}
- Titles: {person_to_delete.titles}
    """)

    confirm = input("Confirm? Type Y If So.\n> ")
    if confirm == "Y":
        PeopleWatch.objects(first_name=fname, last_name=lname).delete()
        print("Successfully Deleted.")
    else:
        print("Canceled.")

def list_people():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")

    class PeopleWatch(Document):
        first_name = StringField(required=True)
        last_name = StringField(required=True)
        organizations = ListField()
        titles = ListField()

    people = PeopleWatch.objects()
    for person in people:
        print(f"""First Name: {person.first_name}
Last Name: {person.last_name}
Organizations: {person.organizations}
Titles: {person.titles}
""")

def main():
    print() # Printing an empty space for style
    if len(argv) == 1:
        print("""Add Following As Arguments:
- \"c\" : To Create A Person      
- \"r\" : To Read All People  
- \"u\" : To Update A Person
- \"d\" : To Delete A Person""")
    elif argv[1] == "c":
        add_person()
    elif argv[1] == "r":
        list_people()
    elif argv[1] == "u":
        update_person()
    elif argv[1] == "d":
        delete_person()
    else:
        print("""Add Following As Arguments:
- \"c\" : To Create A Person      
- \"r\" : To Read All People  
- \"u\" : To Update A Person
- \"d\" : To Delete A Person""")

if __name__ == "__main__":
    main()
