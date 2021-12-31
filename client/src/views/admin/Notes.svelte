<script>
    // core components
    // import Tree from "../../components/Plugin/Tree.svelte";
    j$(function () {
        j$("#tree").fancytree({
            extensions: ["dnd5", "edit"],
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
            },
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
</script>

<!-- <Tree /> -->

<div class="mt-4 w-full h-500-px">
    <div id="tree">
        <ul id="treeData" style="display: none;">
            <li>Node 1</li>
            <li class="folder">
                Folder 2
                <ul>
                    <li id="3 text-black">Node 2.1</li>
                    <li id="4">Node 2.2</li>
                </ul>
            </li>
        </ul>
    </div>
</div>
