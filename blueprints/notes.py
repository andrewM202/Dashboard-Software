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
        if(note.parent_node == "root_1"): # root_! is root node
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
                print(node.title)
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
                # print(parse_child_nodes(note))
            # child_nodes = parse_child_nodes(note)
            # print(child_nodes)

            # if(len(note.sub_nodes) > 0):
            #     note_config["children"] = []
            #     for sub_node in note.sub_nodes:
            #         # print(sub_node)
            #         child_node = Notes.objects(key=sub_node)[0]
            #         child_note = {
            #             "title": child_node.title,
            #             "desc": child_node.description,
            #             "folder": child_node.folder,
            #             "text": child_node.text,
            #             "key": child_node.key,
            #         }
            #         note_config["children"].append(child_note)

            return_notes.append(note_config)
    return json_util.dumps(return_notes)

@bp.route("/admin/update-notes", methods=["POST"])
@login_required
def update_notes():
    """ Route for editing or creating a new note """
    data = request.form.to_dict()
    data_keys = request.form.keys()
    print(data)
    # print(data_keys)

    """
    # If this is a new node
    if(data["isNew"] == "true"):
        new_note_key = str(Notes.objects().count() + 1)
        Notes(
            title = data["data[title]"],
            description = "", # data["data[description]"],
            key = new_note_key, # data["data[key]"], # Make the key an index in Notes
            folder = data["data[folder]"],
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
    # If this is updating an existing node
    else:
        print(data["newData[key]"])
        print(data["newData[title]"])
        Notes.objects(key=data["newData[key]"]).update(
            title = data["newData[title]"],
            description = data["newData[data][desc]"],
            key = data["newData[key]"], 
            folder = True if data["newData[folder]"] == "true" else False,
            text = data["newData[data][text]"],
            sub_nodes = [i.key for i in data["newData[children]"]],
            parent_node = data["newData[parent_key]"],
        )
    """

    # for key in data_keys:
    #     print(dedent(f"""
    #     Key: {key} 
    #     Data: {data[key]}
    #     """))
    return send_from_directory('client/public', 'index.html')