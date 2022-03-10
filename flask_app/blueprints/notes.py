from flask import render_template, Blueprint, send_from_directory, request
from flask_login import  current_user
from flask_security import login_required
from bson import json_util
from models import Notes
from textwrap import dedent

bp = Blueprint("notes", __name__)

@bp.route("/admin/notes")
@login_required
def notes():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/load-notes", methods=["GET", "POST"])
@login_required
def load_notes():
    """ 
    This route returns all of the notes to load for the tree in Notes.svelte
    Example notes below
    notes = [   { "title": "Node 1", "folder": False, "key": "1", "qty": 5, "text": "testing text here" },
                { "title": "Node 2", "key": "2" },
                { "title": "Node 3", "key": "3" },
                { "title": "Node 4", "key": "4", "qty": 3 },
                {
                    "title": "Folder 2",
                    "key": "2",
                    "folder": True,
                    "children": [
                        { "title": "Node 2.1", "key": "3" },
                        { "title": "Node 2.2", "key": "4" },
                    ],
                },
                { "title": "Node 5", "key": "5" } 
            ], 
    """
    return_notes = []
    for note in Notes.objects():
        # print(note.sub_nodes)
        # print(note.parent_node)
        if("root" in note.parent_node): # root_! is root node
            note_config = {
                "title": note.title,
                "desc": note.description,
                "folder": note.folder,
                "text": note.text,
                "key": note.key,
            }
            # If this note has child notes add them to the config
            # using recursion
            def parse_child_nodes(node):
                notes = []
                for child in node.sub_nodes:
                    curr_node = Notes.objects(key=child)[0]
                    if(len(curr_node.sub_nodes) > 0):
                        child_note = {
                        "title": curr_node.title,
                        "desc": curr_node.description,
                        "folder": curr_node.folder,
                        "text": curr_node.text,
                        "key": curr_node.key,
                        "children": parse_child_nodes(curr_node)
                    }
                    else:
                        child_note = {
                            "title": curr_node.title,
                            "desc": curr_node.description,
                            "folder": curr_node.folder,
                            "text": curr_node.text,
                            "key": curr_node.key,
                        }
                    notes.append(child_note)
                return notes

            if(len(note.sub_nodes) > 0):
                note_config["children"] = parse_child_nodes(note)

            return_notes.append(note_config)
    return json_util.dumps(return_notes)

@bp.route("/admin/update-notes", methods=["POST"])
@login_required
def update_notes():
    """ Route for editing or creating a new note """
    data = request.form.to_dict()
    data_keys = request.form.keys()

    # All the keys substructure come in arrays, so instead of 
    # trying to make an actual JSON as it should be, lets just make
    # the arrays ourself 
    new_data_children = []

    for key in data_keys:
        # print(dedent(f"""
        # Key: {key} 
        # Data: {data[key]}
        # """))

        if "data[children]" in key and "[key]" in key:
            new_data_children.append(key)

    # Check if new node by if key exists already
    note_key = data["data[key]"]
    is_new = False if len(Notes.objects(key=note_key)) > 0 else True

    # If this is a new node
    if(is_new):
        new_note_key = str(Notes.objects().count() + 1)
        Notes(
            title = data["data[title]"],
            description = "", # data["data[description]"],
            key = new_note_key, # data["data[key]"], # Make the key an index in Notes
            folder = True if data["data[folder]"] == "true" else False,
            text = "",
            sub_nodes = [],
            parent_node = data["data[parent_key]"],
        ).save()
        # If this new note has a parent node, add that to the 
        # parent node's sub_nodes field
        parent_nodes_len = len(Notes.objects(key=data["data[parent_key]"]))
        # Append key of new sub node
        if(parent_nodes_len > 0):
            parent_node_sub_nodes = list(Notes.objects(key=data["data[parent_key]"])[0].sub_nodes)
            parent_node_sub_nodes.append(new_note_key)
            Notes.objects(key=data["data[parent_key]"]).update(
                sub_nodes = parent_node_sub_nodes
            )

        # Return the new note key
        return new_note_key
    # If this is updating an existing node
    else:
        Notes.objects(key=data["data[key]"]).update(
            title = data["data[title]"],
            description = data["data[desc]"],
            folder = True if data["data[folder]"] == "true" else False,
            text = data["data[text]"],
            sub_nodes = [data[key] for key in new_data_children],
            parent_node = data["data[parent_key]"],
        )

    return "Updated Node"

@bp.route("/admin/delete-note", methods=["POST"])
@login_required
def delete_note():
    """ Delete a note """

    # Can only delete a note if there is more than 1 left
    if(len(Notes.objects()) > 1):

        data = request.form.to_dict()
        data_keys = request.form.keys()
        delete_key = data["data[key]"]

        # If this note has any child nodes delete them recursively
        def delete_nodes(node):
            if (len(node.sub_nodes) > 0):
                for sub_node_key in node.sub_nodes:
                    delete_nodes(Notes.objects(key=sub_node_key)[0])
            Notes.objects(key=node.key).delete()

        delete_nodes(Notes.objects(key=delete_key)[0])

        # If this note has a parent note delete it from its list
        for note in Notes.objects():
            if(delete_key in note.sub_nodes):
                old_sub_nodes = note.sub_nodes
                old_sub_nodes.remove(delete_key)
                Notes.objects(key=note.key).update(
                    sub_nodes = old_sub_nodes
                )

        print(f"Deleted Node: {data['data[key]']}")
    else:
        return "Cannot delete last note"

    return "Deleted Note"

@bp.route("/admin/create-moved-note", methods=["POST"])
@login_required
def create_moved_note():
    """ When a note is moved, they are deleted because
    a remove event is triggered by fancytree 
    so they must be recreated """
    data = request.form.to_dict()
    data_keys = request.form.keys()

    new_data_children = []

    for key in data_keys:
        if "newData[children]" in key and "[key]" in key:
            new_data_children.append(key)

    Notes(
        title = data["data[title]"],
        key = data["data[key]"],
        description = data["data[desc]"],
        folder = True if data["data[folder]"] == "true" else False,
        text = data["data[text]"],
        sub_nodes = [data[key] for key in new_data_children],
        parent_node = data["data[parent_key]"],
    ).save()
    # If this new note has a parent node, add that to the 
    # parent node's sub_nodes field
    parent_nodes_len = len(Notes.objects(key=data["data[parent_key]"]))
    if(parent_nodes_len > 0):
        print(f"Parent Key: {data['data[parent_key]']}")
        print(f"Current Node: {data['data[key]']}")
        print()
        parent_node_sub_nodes = list(Notes.objects(key=data["data[parent_key]"])[0].sub_nodes)
        # If you spam moving a node back and forth this route can 
        # be called before the previous one was completed, causing 
        # duplicates to be created. To prevent that, don't add this
        # moved node to the parent's sub_nodes list if its already in there
        if data["data[key]"] not in parent_node_sub_nodes:
            parent_node_sub_nodes.append(data["data[key]"])
            Notes.objects(key=data["data[parent_key]"]).update(
                sub_nodes = parent_node_sub_nodes
            )

    return data["data[key]"]

@bp.route("/admin/update-note-details", methods=["POST"])
@login_required
def update_note_details():
    """ Update note details 
    like title, description """

    data = request.form.to_dict()
    data_keys = request.form.keys()

    Notes.objects(key=data["key"]).update(
        key = data["key"],
        description = data["desc"],
        text = data["text"],
    )

    return "Success"

@bp.route("/admin/note-search", methods=["POST"])
@login_required
def note_search():
    """ Search for notes and return 
    corresponding JSON payload of notes """

    data = request.form.to_dict()

    # If the form is empty reload the entire tree, else do the search
    if(data["NoteText"] == "" and data["NoteDesc"] == "" and data["NoteTitle"] == ""):
        return_notes = []
        for note in Notes.objects():
            # print(note.sub_nodes)
            # print(note.parent_node)
            if("root" in note.parent_node): # root_! is root node
                print(note.description)
                note_config = {
                    "title": note.title,
                    "desc": note.description,
                    "folder": note.folder,
                    "text": note.text,
                    "key": note.key,
                }
                # If this note has child notes add them to the config
                # using recursion
                def parse_child_nodes(node):
                    notes = []
                    for child in node.sub_nodes:
                        curr_node = Notes.objects(key=child)[0]
                        if(len(curr_node.sub_nodes) > 0):
                            child_note = {
                            "title": curr_node.title,
                            "desc": curr_node.description,
                            "folder": curr_node.folder,
                            "text": curr_node.text,
                            "key": curr_node.key,
                            "children": parse_child_nodes(curr_node)
                        }
                        else:
                            child_note = {
                                "title": curr_node.title,
                                "desc": curr_node.description,
                                "folder": curr_node.folder,
                                "text": curr_node.text,
                                "key": curr_node.key,
                            }
                        notes.append(child_note)
                    return notes

                if(len(note.sub_nodes) > 0):
                    note_config["children"] = parse_child_nodes(note)

                return_notes.append(note_config)
        return json_util.dumps(return_notes)

    else:
        return_notes = []
        for note in Notes.objects():
            if(data["NoteText"].lower() in note.text.lower() and data["NoteDesc"].lower() in note.description.lower() and data["NoteTitle"].lower() in note.title.lower()): 
                note_config = {
                    "title": note.title,
                    "desc": note.description,
                    "folder": note.folder,
                    "text": note.text,
                    "key": note.key,
                    "children": [],
                }
                return_notes.append(note_config)

        return json_util.dumps(return_notes)
