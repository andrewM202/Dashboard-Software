<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";

    let titleSearchInputs = [
        {
            type: "Text",
            placeholder: "Collection Name",
            name: "CollectionName",
        },
        {
            type: "Text",
            placeholder: "Last Name",
            name: "LastName",
        },
        {
            type: "Submit",
            placeholder: "Search",
            name: "",
        },
    ];

    // Each object inside is a section
    let cardSettings = [
        {
            Subtitle: "Misc",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Collection Name",
                    name: "CollectionName",
                    value: "",
                },
            ],
        },
        {
            Subtitle: "Header Search Inputs",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Header Search Input Types",
                    name: "HeaderSearchInputTypes",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Header Search Input Placeholders",
                    name: "HeaderSearchInputPlaceholders",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Header Search Input Names",
                    name: "HeaderSearchInputNames",
                    value: "",
                },
            ],
        },
        {
            Subtitle: "Header Cards",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Header Card Subtitles",
                    name: "HeaderCardSubtitles",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Amounts",
                    name: "HeaderCardAmounts",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Increases",
                    name: "HeaderCardIncreases",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Descriptions",
                    name: "HeaderCardDescriptions",
                    value: "",
                },
            ],
        },
        {
            Subtitle: "Table",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Table Await Data",
                    name: "TableAwaitData",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Headers",
                    name: "TableHeaders",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Title",
                    name: "TableTitle",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Deletion URL",
                    name: "TableDeletionURL",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Refresh URL",
                    name: "TableRefreshURL",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Updated URL",
                    name: "TableUpdatedURL",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Table Update Form Names",
                    name: "TableDBFormNames",
                    value: "",
                },
            ],
        },
        {
            Subtitle: "Creation Card",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Creation Card Await Data",
                    name: "CreationCardAwaitData",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card URL",
                    name: "CreationCardURL",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Refresh URL",
                    name: "CreationCardRefreshURL",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Title",
                    name: "CreationCardTitle",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Flexdatalist Data",
                    name: "CreationCardFlexdatalistData",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Inputs",
                    name: "CreationCardInputs",
                    value: "",
                },
            ],
        },
    ];
</script>

<AdminNavbar title={"Archive Designer"} />
<HeaderStats
    title={"Archive Designer"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
/>

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    <CardSettings
        title={"Archive Creation"}
        postURL={"/admin/archive-data/create-collection"}
        settings={cardSettings}
    />
    <!-- <CardSettings /> -->
</div>
