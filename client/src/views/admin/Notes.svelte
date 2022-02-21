<script>
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    // core components

    /*
    Commands when focused on node:
    - enter :                                           edit title of node
    - control + shift + n :                             create new node
    - control + n :                                     create sibling node
    - control + shift + up/down/left/right arrow key:   move node around
    - command + backspace :                             delete node
    */

    let lastSelectedNode; // Set to the last selected node by the focus event
    let editingNote = false; // Whether or not we are currently editing a node
    j$(function () {
        // Attach the fancytree widget to an existing <div id="tree"> element
        // and pass the tree options as an argument to the fancytree() function:
        j$("#treegrid")
            .fancytree({
                extensions: ["dnd5", "edit", "table", "gridnav"],
                dnd5: {
                    preventVoidMoves: true,
                    preventRecursion: true,
                    autoExpandMS: 400,
                    dragStart: function (node, data) {
                        return true;
                    },
                    dragEnter: function (node, data) {
                        // return ["before", "after"];
                        return true;
                    },
                    dragDrop: function (node, data) {
                        data.otherNode.moveTo(node, data.hitMode);
                    },
                },
                edit: {
                    triggerStart: ["f2", "shift+click", "mac+enter"],
                    close: function (event, data) {
                        if (data.save && data.isNew) {
                            // Quick-enter: add new nodes until we hit [enter] on an empty title
                            j$("#tree").trigger("nodeCommand", {
                                cmd: "addSibling",
                            });
                        }
                    },
                    adjustWidthOfs: 4, // null: don't adjust input size to content
                    inputCss: { minWidth: "3em" },
                    beforeEdit: j$.noop, // Return false to prevent edit mode
                    edit: j$.noop, // Editor was opened (available as data.input)
                    beforeClose: function (event, data) {
                        if (data.originalEvent.type === "mousedown") {
                            // We could prevent the mouse click from generating a blur event
                            // (which would then again close the editor) and return `false` to keep
                            // the editor open:
                            //      data.originalEvent.preventDefault();
                            //      return false;
                            // Or go on with closing the editor, but discard any changes:
                            data.save = false;
                        }
                    },
                },
                modifyChild: function (event, data) {
                    // Check if we are deleting node
                    console.log(data.operation);
                    if (data.operation === "remove") {
                        // This operation is for deleting nodes
                        let updateJson;
                        if (
                            data.childNode !== undefined &&
                            data.childNode !== null
                        ) {
                            updateJson = {
                                data: {
                                    key: data.childNode.key,
                                },
                            };
                        } else {
                            updateJson = {
                                data: {
                                    key: lastSelectedNode.key, //data.node.key,
                                },
                            };
                        }
                        // let tree = j$.ui.fancytree.getTree();
                        console.log(updateJson);
                        j$.ajax({
                            type: "POST",
                            url: `${location.origin}/admin/delete-note`,
                            data: updateJson,
                            error: function (e) {
                                error = "Server Error During Creation.";
                                // Error logging
                                console.log(e.statusText);
                                console.log(e.responseText);
                            },
                        });
                    } else if (data.operation === "rename") {
                        // This operation is for creating and renaming nodes

                        let newData_children = [];
                        if (data.childNode.children !== null) {
                            for (let child of data.childNode.children) {
                                newData_children.push({
                                    title: child.title,
                                    key: child.key,
                                });
                            }
                        } else {
                            newData_children = null;
                        }
                        console.log(newData_children);
                        let updateJson = {
                            data: {
                                title: data.childNode.title,
                                desc:
                                    data.childNode.data.desc === undefined
                                        ? data.childNode.desc
                                        : data.childNode.data.desc,
                                text:
                                    data.childNode.data.text === undefined
                                        ? data.childNode.text
                                        : data.childNode.data.text,
                                folder:
                                    data.childNode.folder === undefined
                                        ? false
                                        : data.childNode.folder,
                                key: data.childNode.key,
                                data: data.childNode.data,
                                children: newData_children,
                                parent_title: data.childNode?.parent?.title,
                                parent_key: data.childNode?.parent?.key,
                            },
                        };
                        j$.ajax({
                            type: "POST",
                            url: `${location.origin}/admin/update-notes`,
                            data: updateJson,
                            success: function (e) {
                                if (e !== "Updated Node") {
                                    // We just created a new node
                                    let tree = j$.ui.fancytree.getTree();
                                    tree.getActiveNode().key = e;
                                    tree.getActiveNode().text = "";
                                    tree.getActiveNode().desc = "";
                                    data.node.text = "";
                                    data.node.desc = "";
                                }
                            },
                            error: function (e) {
                                error = "Server Error During Creation.";
                                // Error logging
                                console.log(e.statusText);
                                console.log(e.responseText);
                            },
                        });
                    } else if (data.operation === "add") {
                        // This operation is solely for moving nodes

                        // console.log(data);
                        // console.log(data.node.tree);
                        // console.log(data.childNode.key);

                        // Check if this is really a new node or
                        // if this is a node that just moved
                        // Its a moved node its key does not have an underscore
                        if (data.childNode.key.indexOf("_") === -1) {
                            console.log("This is an already created node");
                            // console.log(data.childNode);

                            function nodeMoveCreation(startNode) {
                                let newData_children = [];
                                if (startNode.children !== null) {
                                    for (let child of startNode.children) {
                                        newData_children.push({
                                            title: child.title,
                                            key: child.key,
                                        });
                                    }
                                } else {
                                    newData_children = null;
                                }
                                let updateJson = {
                                    data: {
                                        title: startNode.title,
                                        desc:
                                            startNode.desc === undefined
                                                ? startNode.data.desc
                                                : startNode.desc,
                                        text:
                                            startNode.text === undefined
                                                ? startNode.data.text
                                                : startNode.text,
                                        folder:
                                            startNode.folder === undefined
                                                ? false
                                                : startNode.folder,
                                        key: startNode.key,
                                        data: startNode.data,
                                        children: newData_children,
                                        parent_title: startNode?.parent?.title,
                                        parent_key: startNode?.parent?.key,
                                    },
                                };
                                j$.ajax({
                                    type: "POST",
                                    url: `${location.origin}/admin/create-moved-note`,
                                    data: updateJson,
                                    success: function (e) {
                                        if (e !== "Updated Node") {
                                            // We just created a new node
                                            let tree =
                                                j$.ui.fancytree.getTree();
                                            // tree.getActiveNode().key = e;
                                            // tree.getActiveNode().text = "";
                                            // tree.getActiveNode().desc = "";
                                            // tree.getNodeByKey()
                                            // data.node.text = "";
                                            // data.node.desc = "";
                                        }
                                    },
                                    error: function (e) {
                                        error = "Server Error During Creation.";
                                        // Error logging
                                        console.log(e.statusText);
                                        console.log(e.responseText);
                                    },
                                });
                                // Re call the function for all of the child nodes
                                if (startNode.children !== null) {
                                    for (let child of startNode.children) {
                                        nodeMoveCreation(child);
                                    }
                                }
                            }

                            setTimeout(function () {
                                nodeMoveCreation(data.childNode);
                            }, 50);
                        }

                        // Event trigger for moving a node.

                        // Recursively make server requests for each
                        // child node of the moved node, as they
                        // were just deleted
                    }
                    console.log("------");
                },
                focus: function (event, data) {
                    lastSelectedNode = data.node;

                    // Make text of selected node white for
                    // easier visibility
                    let node = data.node,
                        j$tdList = j$(node.tr).find(">td");

                    j$tdList.eq(3).css({
                        color: "white",
                    });
                    j$tdList.eq(2).find("span.fancytree-title").css({
                        color: "white",
                    });
                    j$tdList.eq(1).css({
                        color: "white",
                    });
                },
                blur: function (event, data) {
                    // Once the node is no longer selected,
                    // change the text color to black for
                    // easier visibility

                    let node = data.node,
                        j$tdList = j$(node.tr).find(">td");

                    j$tdList.eq(3).css({
                        color: "",
                    });
                    j$tdList.eq(2).find("span.fancytree-title").css({
                        color: "",
                    });
                    j$tdList.eq(1).css({
                        color: "",
                    });
                },
                checkbox: true,
                table: {
                    indentation: 20, // indent 20px per node level
                    nodeColumnIdx: 2, // render the node title into the 2nd column
                    checkboxColumnIdx: 0, // render the checkboxes into the 1st column
                },
                source: {
                    url: "/admin/load-notes",
                    dataType: "json",
                    cache: false,
                },
                postProcess: function (event, data) {
                    // Process data from load-notes route
                    data.result = j$.parseJSON(
                        JSON.stringify(data.response)
                    )[0];
                },
                tooltip: function (event, data) {
                    return data.node.data.author;
                },
                renderColumns: function (event, data) {
                    let node = data.node,
                        j$tdList = j$(node.tr).find(">td");

                    // (index #0 is rendered by fancytree by adding the checkbox)
                    j$tdList.eq(1).text(node.getIndexHier());
                    // (index #2 is rendered by fancytree)
                    j$tdList.eq(3).text(node.data.desc);
                    // When you click on edit node button, unbind click event
                    // and rebind it to fix bug where a new node's click event
                    // is fired twice for some reason
                    j$tdList
                        .eq(4)
                        .unbind("click")
                        .click(function (e) {
                            if (editingNote === false) {
                                // Not currently editing a node, so lets start
                                editingNote = true;
                                j$tdList.eq(3).html(`
                            <input
                                type="text"
                                name="desc"
                                value="${
                                    node.data.desc === undefined
                                        ? ""
                                        : node.data.desc
                                }"
                                placeholder="Note Description"
                                style="color: black;"
                                class="w-full h-full text-dark"
                            />`);
                                j$tdList.eq(4).find("input").attr({
                                    value: "Save Edit",
                                });

                                // CKEditor
                                j$("#noteText")
                                    .html(`<div class="document-editor">
                                        <div class="document-editor__toolbar"></div>
                                        <div class="document-editor__editable-container">
                                            <div class="document-editor__editable">
                                                ${j$("#noteText").html()}
                                            </div>
                                        </div>
                                    </div>`);

                                // Prevent tabbing in the editor
                                j$("#noteText").keydown(function (e) {
                                    if (e.keyCode === 9) {
                                        // tab was pressed
                                        // get caret position/selection
                                        var start = this.selectionStart;
                                        var end = this.selectionEnd;

                                        var value = j$(this).val();

                                        // set textarea value to: text before caret + tab + text after caret
                                        j$(this).val(
                                            value.substring(0, start) +
                                                "\t" +
                                                value.substring(end)
                                        );

                                        // put caret at right position again (add one for the tab)
                                        this.selectionStart =
                                            this.selectionEnd = start + 1;

                                        // prevent the focus lose
                                        e.preventDefault();
                                    }
                                });

                                DecoupledEditor.create(
                                    document.querySelector(
                                        ".document-editor__editable"
                                    ),
                                    {}
                                )
                                    .then((editor) => {
                                        const toolbarContainer =
                                            document.querySelector(
                                                ".document-editor__toolbar"
                                            );

                                        toolbarContainer.appendChild(
                                            editor.ui.view.toolbar.element
                                        );

                                        window.editor = editor;
                                    })
                                    .catch((err) => {
                                        console.error(err);
                                    });
                            } else {
                                // We are currently editing, so lets
                                // save the edits
                                editingNote = false;
                                console.log("Finished Editing");

                                let newDesc = j$tdList
                                    .eq(3)
                                    .find("input")
                                    .val();
                                j$tdList.eq(3).html(newDesc);

                                j$tdList.eq(4).find("input").attr({
                                    value: "Edit Note",
                                });

                                let noteTextValue = j$(
                                    "#noteText .document-editor__editable"
                                ).html();
                                node.data.text = noteTextValue;
                                j$("#noteText").html(noteTextValue);

                                let updateJson = {
                                    key: node.key,
                                    desc: newDesc,
                                    text: noteTextValue,
                                };

                                // Update server
                                j$.ajax({
                                    type: "POST",
                                    url: `${location.origin}/admin/update-note-details`,
                                    data: updateJson,
                                    success: function (e) {
                                        console.log("Success");
                                    },
                                    error: function (e) {
                                        error = "Server Error During Creation.";
                                        // Error logging
                                        console.log(e.statusText);
                                        console.log(e.responseText);
                                    },
                                });
                            }
                        });
                },
                activate: function (event, data) {
                    let activeNode = data.tree.activeNode;
                    // console.log(data.tree.activeNode);
                    if (activeNode) {
                        let noteText = activeNode.data.text;
                        j$("#noteText").html(noteText ? noteText : "");
                    }
                },
            })
            .on("nodeCommand", function (event, data) {
                // Custom event handler that is triggered by keydown-handler and
                // context menu:
                var refNode,
                    moveMode,
                    tree = j$.ui.fancytree.getTree(this),
                    node = tree.getActiveNode();

                switch (data.cmd) {
                    case "addChild":
                    case "addSibling":
                    case "indent":
                    case "moveDown":
                    case "moveUp":
                    case "outdent":
                    case "remove":
                    case "rename":
                        tree.applyCommand(data.cmd, node);
                        break;
                    case "cut":
                        CLIPBOARD = { mode: data.cmd, data: node };
                        break;
                    case "copy":
                        CLIPBOARD = {
                            mode: data.cmd,
                            data: node.toDict(true, function (dict, node) {
                                delete dict.key;
                            }),
                        };
                        break;
                    case "clear":
                        CLIPBOARD = null;
                        break;
                    case "paste":
                        if (CLIPBOARD.mode === "cut") {
                            // refNode = node.getPrevSibling();
                            CLIPBOARD.data.moveTo(node, "child");
                            CLIPBOARD.data.setActive();
                        } else if (CLIPBOARD.mode === "copy") {
                            node.addChildren(CLIPBOARD.data).setActive();
                        }
                        break;
                    default:
                        alert("Unhandled command: " + data.cmd);
                        return;
                }
            })
            .on("keydown", function (e) {
                var cmd = null;
                // console.log(e.type, $.ui.fancytree.eventToString(e));
                switch (j$.ui.fancytree.eventToString(e)) {
                    case "ctrl+shift+n":
                    case "meta+shift+n": // mac: cmd+shift+n
                        cmd = "addChild";
                        break;
                    case "ctrl+c":
                    case "meta+c": // mac
                        cmd = "copy";
                        break;
                    case "ctrl+v":
                    case "meta+v": // mac
                        cmd = "paste";
                        break;
                    case "ctrl+x":
                    case "meta+x": // mac
                        cmd = "cut";
                        break;
                    case "ctrl+n":
                    case "meta+n": // mac
                        cmd = "addSibling";
                        break;
                    case "del":
                    case "meta+backspace": // mac
                        cmd = "remove";
                        break;
                    // case "f2":  // already triggered by ext-edit pluging
                    //   cmd = "rename";
                    //   break;
                    case "ctrl+up":
                    case "ctrl+shift+up": // mac
                        cmd = "moveUp";
                        break;
                    case "ctrl+down":
                    case "ctrl+shift+down": // mac
                        cmd = "moveDown";
                        break;
                    case "ctrl+right":
                    case "ctrl+shift+right": // mac
                        cmd = "indent";
                        break;
                    case "ctrl+left":
                    case "ctrl+shift+left": // mac
                        cmd = "outdent";
                }
                if (cmd) {
                    // console.log(cmd);
                    j$(this).trigger("nodeCommand", { cmd: cmd });
                    return false;
                }
            });

        /* Handle custom checkbox clicks */
        j$("#treegrid").on("click", "input[name=like]", function (e) {
            var node = j$.ui.fancytree.getNode(e),
                j$input = j$(e.target);

            e.stopPropagation(); // prevent fancytree activate for this row
            if (j$input.is(":checked")) {
                // alert("like " + node);
            } else {
                // alert("dislike " + node);
            }
        });
    });

    // Fancytree Edit Styling
    setInterval(function () {
        j$(".fancytree-edit-input").css(
            { color: "black" },
            { height: "50px" },
            { width: "100px" }
        );
        j$(".fancytree-edit-input").css("min-width", "100px");
    }, 100);

    let titleSearchInputs = [
        {
            type: "Text",
            placeholder: "Note Title",
            name: "NoteTitle",
        },
        {
            type: "Text",
            placeholder: "Note Description",
            name: "NoteDesc",
        },
        {
            type: "Text",
            placeholder: "Note Text",
            name: "NoteText",
        },
    ];

    function HeaderSearchFunction(e) {
        e.preventDefault();

        let form;
        // Instead of hard coding form selector, find first form element
        // and set that as selector
        for (let i = 0; i < e.path.length; i++) {
            if (e.path[i].tagName === "FORM") {
                form = e.path[i];
                break;
            }
        }

        j$.ajax({
            type: "POST",
            url: `${location.origin}/admin/note-search`,
            data: j$(form).serialize(),
            success: function (e) {
                // Load fancytree with data from search
                let tree = j$.ui.fancytree.getTree();
                tree.reload([j$.parseJSON(e)]);
                j$(form)[0].reset();
            },
            error: function (e) {
                error = "Server Error During Creation.";
                // Error logging
                console.log(e.statusText);
                console.log(e.responseText);
            },
        });
    }
</script>

<!-- <Tree /> -->

<HeaderStats
    title={"Notes"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
    SearchFunction={HeaderSearchFunction}
    submitValue={"Search Notes"}
/>
<div class="w-full h-auto">
    <!-- Add a <table> element where the tree should appear: -->
    <table id="treegrid" class="table-auto w-full">
        <colgroup>
            <col width="25px" />
            <col width="100px" />
            <col width="100px" />
            <col width="100px" />
            <col width="100px" />
        </colgroup>
        <thead>
            <tr class="bg-blueGray-200 text-left">
                <th
                    class="w-1/6 min-w-[160px] text-lg font-semibold text-black py-4 lg:py-7 px-3 lg:px-4 border-l border-transparent"
                />
                <th
                    class="w-1/6 min-w-[160px] text-lg font-semibold text-black py-4 lg:py-7 px-3 lg:px-4 border-l border-transparent"
                    >#</th
                >
                <th
                    class="w-1/6 min-w-[160px] text-lg font-semibold text-black py-4 lg:py-7 px-3 lg:px-4 border-l border-transparent"
                    >Folder</th
                >
                <th
                    class="w-1/6 min-w-[160px] text-lg font-semibold text-black py-4 lg:py-7 px-3 lg:px-4 border-l border-transparent"
                    >Description</th
                >
                <th
                    class="w-1/6 min-w-[160px] text-lg font-semibold text-black py-4 lg:py-7 px-3 lg:px-4 border-l border-transparent"
                    >Edit Note</th
                >
            </tr>
        </thead>
        <!-- Optionally define a row that serves as template, when new nodes are created: -->
        <tbody>
            <tr class="text-center">
                <td
                    class="text-center text-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
                />
                <td
                    class="text-left text-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
                />
                <td
                    class="text-left text-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
                />
                <td
                    class="text-left text-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
                />
                <td
                    class="text-center text-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
                    ><input
                        type="button"
                        name="like"
                        value="Edit Note"
                        style=""
                        class="w-full h-full cursor-pointer"
                    /></td
                >
            </tr>
        </tbody>
    </table>
</div>

<div class="mt-8 w-full overflow-x-auto md:w-11/12 h-auto px-4">
    <h1 class="text-2xl text-center font-medium text-base font-semibold">
        Note Text
    </h1>
    <div
        id="noteText"
        class="w-full p-4 overflow-x-auto border-8 border-blueGray-200 h-auto ck ck-content"
        style="border-radius: 8px; min-height: 500px;"
        contenteditable="false"
    />
</div>
