<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import { dataSettingsStore, getDBResource } from "../../stores.js";

    let collectionTitles, collectionPairs;
    async function getDBData() {
        collectionTitles = await getDBResource(
            "/admin/archive-data/collection-titles"
        );
        collectionPairs = await getDBResource(
            "/admin/archive-data/collection-title-pairs"
        );
    }

    getDBData();

    let tableData = [];
    $: tableData = [collectionTitles, collectionPairs];

    // Is a collection being edited?
    // If so, which one?
    let postURL = "/admin/archive-data/create-collection";

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
        let formData = j$(form)
            .find("input[name=flexdatalist-CollectionName]")
            .val();

        j$(form).trigger("reset");

        if (formData !== "") {
            for (let col of Object.entries($dataSettingsStore)) {
                // We found the right collection we are editing
                if (formData === col[1].CollectionName) {
                    /*
                    console.log(col[1]);
                    // Collection Name
                    cardSettings[0].Inputs[0].value = col[1].CreationCard.Title;
                    // Table title
                    cardSettings[0].Inputs[1].value = col[1].Table.Title;
                    // Creation Card Title
                    cardSettings[0].Inputs[2].value = col[1].CreationCard.Title;
                    // Creation Card Input Types
                    cardSettings[1].Inputs[0].value =  
                    // Creation Card Input Names
                    cardSettings[1].Inputs[1].value = 
                    // Creation Card Input Flexdatalist data
                    cardSettings[1].Inputs[2].value = 
                    // Creation Card Input Flexdatalist Field
                    cardSettings[1].Inputs[3].value = 
                    // Creation Card Required Field
                    cardSettings[1].Inputs[4].value = 
                    // Header Search Input Types
                    cardSettings[2].Inputs[0].value = 
                    // Header Input Searchable
                    cardSettings[2].Inputs[1].value = 
                    // Header Card Subtitles
                    cardSettings[3].Inputs[0].value = 
                    // Header Card Amounts
                    cardSettings[3].Inputs[0].value = 
                    // Header Card Increases
                    cardSettings[3].Inputs[0].value = 
                    // Header Card Descriptions
                    cardSettings[3].Inputs[0].value = 
                    */
                }
            }

            // Change CardSettings's values
            for (let setting of cardSettings) {
                for (let input of setting.Inputs) {
                    // console.log(input.name);
                    j$(`[name=${input.name}]`).val("test");
                }
            }
        }
    }

    let titleSearchInputs;
    $: titleSearchInputs = [
        {
            type: "Text",
            placeholder: "Collection Name",
            name: "CollectionName",
            flexdatalistdata: collectionTitles,
            flexdataid: Math.random().toString(36).substring(2, 8),
            flexdatafields: ["collection_name"],
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
                {
                    type: "Text",
                    placeholder: "Table Title",
                    name: "TableTitle",
                    value: "",
                    flexdatalistdisabled: true,
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Title",
                    name: "CreationCardTitle",
                    value: "",
                    flexdatalistdisabled: true,
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
                {
                    type: "Text",
                    placeholder: "Creation Card Input Flexdatalist data",
                    name: "CreationCardFlexdatalistData",
                    value: "",
                    dbFieldNames: ["collection_name"],
                    flexdatalistdata: collectionTitles,
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
                    flexdatalistdata: collectionPairs,
                    flexdatanonedata: true, // Adds a "None value"
                    flexdataid: Math.random().toString(36).substring(2, 8),
                    popoverMessage:
                        "If this is a flexdatalist and the collection is chosen, which field from the collection should be used? Values in 'Collection Name': 'Field' pairs",
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
            Subtitle: "Header Search Inputs",
            SubtitlePopoverMessage:
                "Corresponds to the search inputs in the header. Value set must be equal in length to creation card inputs",
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
                    placeholder: "Header Input Searchable",
                    name: "HeaderSearchEnabled",
                    value: "",
                    popoverMessage:
                        "Should this input even be searchable (True) or not at all (False)?",
                    flexdatalistdata: ["True", "False"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
            ],
        },
        {
            Subtitle: "Header Cards",
            SubtitlePopoverMessage:
                "Each field represents a component of the cards in the raw archive. Value set must be equal in length to other header search input fields.",
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
    ];
</script>

<AdminNavbar />
{#if tableData.includes(undefined) !== true}
    <HeaderStats
        title={"Archive Designer"}
        titleFontSize={"text-6xl"}
        titleColor={"text-black"}
        inputs={titleSearchInputs}
        submitValue={"Edit"}
        SearchFunction={HeaderSearchFunction}
    />
{/if}

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    {#if tableData.includes(undefined) !== true}
        <CardSettings
            title={"Archive Creation"}
            {postURL}
            settings={cardSettings}
        />
    {/if}
</div>
