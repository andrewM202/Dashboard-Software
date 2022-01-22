<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import { collectionKeysStore, collectionsStore } from "../../stores.js";

    // The collections in the database
    let collections, collectionKeys;
    $: collections = $collectionsStore;
    $: collectionKeys = $collectionKeysStore;
    $: if (collectionKeys !== undefined) {
        collectionKeys = collectionKeys.KeyPairs;
    }

    let tableData = [];
    $: tableData = [collections, collectionKeys];

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
    ];

    // Each object inside is a section
    let cardSettings;
    $: cardSettings = [
        {
            Subtitle: "Misc",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Collection Name",
                    name: "CollectionName",
                    value: "",
                    popoverMessage:
                        "Name of the collection. This will show in the top navigation of the raw archive",
                    flexdatalistdisabled: true,
                },
            ],
        },
        {
            Subtitle: "Header Search Inputs",
            SubtitlePopoverMessage:
                "Value set must be equal in length to other header search input fields. Values separated by commas, no spaces.",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Header Search Input Types",
                    name: "HeaderSearchInputTypes",
                    value: "",
                    popoverMessage:
                        "What type of input is allowed for this component of the search form?",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Header Search Input Placeholders",
                    name: "HeaderSearchInputPlaceholders",
                    value: "",
                    popoverMessage:
                        "Individual value may be any string, no commas",
                },
            ],
        },
        {
            Subtitle: "Header Cards",
            SubtitlePopoverMessage:
                "Each field represents a component of the cards in the raw archive. Value set must be equal in length to other header search input fields. Separate values separated by commas",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Header Card Subtitles",
                    name: "HeaderCardSubtitles",
                    value: "",
                    popoverMessage:
                        "The subtitle of each header card in the raw archive for this collection.",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Amounts",
                    name: "HeaderCardAmounts",
                    value: "",
                    popoverMessage: "Value is a number",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Increases",
                    name: "HeaderCardIncreases",
                    value: "",
                    popoverMessage:
                        "Value is a number that represents a percentage",
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
            SubtitlePopoverMessage:
                "Each field represents a component of the table that holds the data",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Table Title",
                    name: "TableTitle",
                    value: "",
                    flexdatalistdisabled: true,
                },
            ],
        },
        {
            Subtitle: "Creation Card",
            SubtitlePopoverMessage: "The misc parts of the creation card",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Creation Card Title",
                    name: "CreationCardTitle",
                    value: "",
                    flexdatalistdisabled: true,
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Required Field",
                    name: "CreationCardRequiredField",
                    value: "",
                    popoverMessage:
                        "true indicates that the field is required, false indicates it is not",
                    flexdatalistdata: ["true", "false"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
            ],
        },
        {
            Subtitle: "Creation Card Inputs",
            SubtitlePopoverMessage: "Define the inputs for creating a document",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Creation Card Input Types",
                    name: "CreationCardInputTypes",
                    value: "",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Names",
                    name: "CreationCardInputNames",
                    value: "",
                    popoverMessage:
                        "This defines the actual name of the field. Choose it wisely!",
                },
                // {
                //     type: "Text",
                //     placeholder: "Creation Card Input Placeholders",
                //     name: "CreationCardInputPlaceholders",
                //     value: "",
                // },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Flexdatalist data",
                    name: "CreationCardFlexdatalistData",
                    value: "",
                    dbFieldNames: ["collection_name"],
                    flexdatalistdata: collections,
                    flexdatanonedata: true, // Adds a "None value"
                    flexdataid: Math.random().toString(36).substring(2, 8),
                    popoverMessage:
                        "If this is a flexdatalist, which collection should the data be from? Fill out 'None' if not a flexdatalist.",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Flexdatalist Field",
                    name: "CreationCardFlexdatalistField",
                    value: "",
                    // dbFieldNames: ["collection_name"],
                    flexdatalistdata: collectionKeys,
                    flexdatanonedata: true, // Adds a "None value"
                    flexdataid: Math.random().toString(36).substring(2, 8),
                    popoverMessage:
                        "If this is a flexdatalist and the collection is chosen, which field from the collection should be used? Values in 'Collection Name': 'Field' pairs",
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
    {#if tableData.includes(undefined) !== true}
        <CardSettings
            title={"Archive Creation"}
            postURL={"/admin/archive-data/create-collection"}
            settings={cardSettings}
        />
    {/if}
</div>
