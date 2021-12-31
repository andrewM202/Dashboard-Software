<script>
    // core components
    // import Tree from "../../components/Plugin/Tree.svelte";
    j$(function () {
        j$("#tree").fancytree({
            extensions: ["dnd5"],
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
        });
    });
</script>

<!-- <Tree /> -->

<div class="mt-4 w-full h-500-px">
    <div id="tree">
        <ul id="treeData" style="display: none;">
            <li id="1">Node 1</li>
            <li id="2" class="folder">
                Folder 2
                <ul>
                    <li id="3">Node 2.1</li>
                    <li id="4">Node 2.2</li>
                </ul>
            </li>
        </ul>
    </div>
</div>
