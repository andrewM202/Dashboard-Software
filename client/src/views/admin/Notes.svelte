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

    let lastSelectedNode;
    j$(function () {
        // Attach the fancytree widget to an existing <div id="tree"> element
        // and pass the tree options as an argument to the fancytree() function:
        let tree = j$("#treegrid")
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
                    //     save: function (event, data) {
                    //         // Update this node when saving
                    //         let updateJson;
                    //         // console.log(data);
                    //         if (data.isNew) {
                    //             // Have to do interval until title is not null, because
                    //             // title is not set immediately on new node
                    //             // because its updated asynchronously it seems
                    //             let interval = setInterval(function () {
                    //                 if (data.node.title !== "") {
                    //                     let newData_children = [];
                    //                     if (data.node.children !== null) {
                    //                         for (let child of data.node.children) {
                    //                             newData_children.push({
                    //                                 title: child.title,
                    //                                 key: child.key,
                    //                             });
                    //                         }
                    //                     } else {
                    //                         newData_children = null;
                    //                     }
                    //                     updateJson = {
                    //                         isNew: data.isNew,
                    //                         data: {
                    //                             title: data.node.title,
                    //                             folder:
                    //                                 data.node.folder === undefined
                    //                                     ? false
                    //                                     : data.node.folder,
                    //                             key: data.node.key,
                    //                             data: data.node.data,
                    //                             children: newData_children,
                    //                             parent_title:
                    //                                 data.node.parent.title,
                    //                             parent_key: data.node.parent.key,
                    //                         },
                    //                     };
                    //                     data.node.desc = "";
                    //                     data.node.text = "";
                    //                     clearInterval(interval);
                    //                     j$.ajax({
                    //                         type: "POST",
                    //                         url: `${location.origin}/admin/update-notes`,
                    //                         data: updateJson,
                    //                         success: function (e) {
                    //                             console.log("Success");
                    //                             // Set the key to the one returned from server
                    //                             data.node.key = e;
                    //                             data.node.text = "test";
                    //                         },
                    //                         error: function (e) {
                    //                             error =
                    //                                 "Server Error During Creation.";
                    //                             // Error logging
                    //                             console.log(e.statusText);
                    //                             console.log(e.responseText);
                    //                         },
                    //                     });
                    //                 }
                    //             }, 1);
                    //         } else {
                    //             // Get newData and oldData chilren's key and title pairs
                    //             // in separate json
                    //             setTimeout(function () {
                    //                 let oldData_children = [];
                    //                 if (data.tree.activeNode.children !== null) {
                    //                     for (let child of data.tree.activeNode
                    //                         .children) {
                    //                         oldData_children.push({
                    //                             title: child.title,
                    //                             key: child.key,
                    //                         });
                    //                     }
                    //                 } else {
                    //                     oldData_children = null;
                    //                 }
                    //                 let newData_children = [];
                    //                 if (data.node.children !== null) {
                    //                     for (let child of data.node.children) {
                    //                         newData_children.push({
                    //                             title: child.title,
                    //                             key: child.key,
                    //                         });
                    //                     }
                    //                 } else {
                    //                     newData_children = null;
                    //                 }

                    //                 updateJson = {
                    //                     isNew: data.isNew,
                    //                     oldData: {
                    //                         title: data.orgTitle,
                    //                         folder:
                    //                             data.tree.activeNode.folder ===
                    //                             undefined
                    //                                 ? false
                    //                                 : data.tree.activeNode.folder,
                    //                         key: data.tree.activeNode.key,
                    //                         children: oldData_children,
                    //                         parent_title:
                    //                             data.tree.activeNode.parent.title,
                    //                         parent_key:
                    //                             data.tree.activeNode.parent.key,
                    //                     },
                    //                     newData: {
                    //                         title: data.node.title,
                    //                         desc: data.node.desc,
                    //                         text: data.node.text,
                    //                         folder:
                    //                             data.node.folder === undefined
                    //                                 ? false
                    //                                 : data.node.folder,
                    //                         key: data.node.key,
                    //                         children: newData_children,
                    //                         parent_title: data.node.parent.title,
                    //                         parent_key: data.node.parent.key,
                    //                     },
                    //                 };
                    //                 console.log(updateJson);
                    //                 updateNodeData(
                    //                     updateJson,
                    //                     "/admin/update-notes"
                    //                 );
                    //             }, 250);
                    //         }
                    //     },
                },
                modifyChild: function (event, data) {
                    // Check if we are deleting node
                    console.log(data.operation);
                    if (data.operation === "remove") {
                        // This operation is for deleting nodes

                        console.log(data);
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
                        if (data.node.children !== null) {
                            for (let child of data.node.children) {
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
                                title: data.childNode.title,
                                desc: data.childNode.desc,
                                text: data.childNode.text,
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
                            console.log(data.childNode);

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
                                console.log(updateJson);
                                // updateNodeData(
                                //     updateJson,
                                //     "/admin/create-moved-note"
                                // );
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
                            }, 500);
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
                    // console.log(lastSelectedNode);
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
                    var node = data.node,
                        j$tdList = j$(node.tr).find(">td");

                    // (index #0 is rendered by fancytree by adding the checkbox)
                    j$tdList.eq(1).text(node.getIndexHier());
                    // (index #2 is rendered by fancytree)
                    j$tdList.eq(3).text(node.data.desc);
                    // When you click on edit node button
                    j$tdList.eq(4).click(function () {
                        console.log(data);
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

    function updateNodeData(data, route) {
        j$.ajax({
            type: "POST",
            url: `${location.origin}${route}`,
            data: data,
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
    ];

    function HeaderSearchFunction(e) {
        e.preventDefault();
        console.log("test");
    }
</script>

<!-- <Tree /> -->

<HeaderStats
    title={"Notes"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
    SearchFunction={HeaderSearchFunction}
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
                    class="text-lefttext-dark font-medium text-base bg-[#F3F6FF] border-b border-l border-[#E8E8E8]"
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
        class="w-full overflow-x-auto border-8 border-blueGray-200 h-auto"
        style="border-radius: 8px; min-height: 500px;"
    >
        <p>Text</p>
    </div>
</div>
