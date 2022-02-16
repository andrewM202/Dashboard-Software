from flask import render_template, Blueprint, send_from_directory
from flask_login import  current_user
from flask_security import login_required
from bson import json_util

bp = Blueprint("notes", __name__)

@bp.route("/admin/notes")
@login_required
def notes():
    return send_from_directory('client/public', 'index.html')

@bp.route("/admin/load-notes", methods=["GET", "POST"])
@login_required
def load_notes():
    # return send_from_directory('client/public', 'index.html')
    notes = [ { "title": "Node 1", "key": "1", "qty": 5 },
                    { "title": "Node 2", "key": "2" },
                    { "title": "Node 3", "key": "3" },
                    { "title": "Node 4", "key": "4" },
                    {
                        "title": "Folder 2",
                        "key": "2",
                        "folder": True,
                        "children": [
                            { "title": "Node 2.1", "key": "3" },
                            { "title": "Node 2.2", "key": "4" },
                        ],
                    },
                    { "title": "Node 5", "key": "5" } ], 
    return json_util.dumps(notes)