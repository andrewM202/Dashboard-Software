<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import { getDBResource } from "../../stores.js";

    let collectionTitles, collectionPairs, archiveConfig;
    async function getDBData() {
        collectionTitles = await getDBResource(
            "/admin/archive-data/collection-titles"
        );
        collectionPairs = await getDBResource(
            "/admin/archive-data/collection-title-pairs"
        );
        archiveConfig = await getDBResource("/admin/archive-config-collection");
    }

    getDBData();

    let tableData = [];
    $: tableData = [collectionTitles, collectionPairs];

    // Is a collection being edited?
    // If so, which one?
    let postURL = "/admin/archive-data/create-collection";
    let archiveDesignerButtonTitle = "Collection Creation";
    let headerSubmitValue = "Edit Collection"; // Submit/Edit button in header search

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
            for (let col of archiveConfig) {
                // We found the right collection we are editing
                if (formData === col.collection_title) {
                    // Loop through each input and set to right value
                    for (let setting of cardSettings) {
                        for (let input of setting.Inputs) {
                            j$(`[name=${input.name}]`).val(
                                col[input.name].toString()
                            );
                        }
                    }
                    // Manually set the collection name
                    j$(`[name=collection_name]`).val(
                        col["collection_title"].toString()
                    );
                    // Manually set creation card input names, as
                    // this should be the placeholders in the UI
                    j$(`[name=creationcard_input_names]`).val(
                        col["creationcard_input_placeholders"].toString()
                    );
                    // Manually add a hidden input with the collection ID
                    // we are changing
                    j$("#archCreateForm").append(
                        `<input id="collectionEditID" type="hidden" value="${col["_id"].$oid}" name="collectionEditID">`
                    );
                }
            }

            // Change postURL to the edit URL
            postURL = "/admin/archive-data/edit-collection";
            // Change button title
            archiveDesignerButtonTitle = "Edit Collection";
            // Header search button
            headerSubmitValue = "Reset / Switch Form";
        } else {
            // Reset form if blank
            for (let setting of cardSettings) {
                for (let input of setting.Inputs) {
                    j$(`[name=${input.name}]`).val("");
                }
            }
            // Reset postURL
            postURL = "/admin/archive-data/create-collection";

            // Remove hidden collection ID
            j$(form).find("#archCreateForm").remove();

            // Change button title
            archiveDesignerButtonTitle = "Collection Creation";

            headerSubmitValue = "Edit Collection";
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
                    name: "collection_name",
                    value: "",
                    popoverMessage:
                        "Name of the collection. This will show in the top navigation of the raw archive",
                    flexdatalistdisabled: true,
                },
                {
                    type: "Text",
                    placeholder: "Table Title",
                    name: "table_title",
                    value: "",
                    flexdatalistdisabled: true,
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Title",
                    name: "creationcard_title",
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
                    name: "creationcard_input_types",
                    value: "",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Names",
                    name: "creationcard_input_names",
                    value: "",
                    popoverMessage:
                        "This defines the actual name of the field. Choose it wisely!",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Flexdatalist data",
                    name: "creationcard_flexdatalistdata",
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
                    name: "creationcard_flexdatalistfield",
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
                    name: "creationcard_required_field",
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
                    name: "header_search_input_types",
                    value: "",
                    popoverMessage:
                        "What type of input is allowed for this component of the search form?",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Header Input Searchable",
                    name: "header_search_enabled",
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
                    name: "header_card_subtitles",
                    value: "",
                    popoverMessage:
                        "The subtitle of each header card in the raw archive for this collection.",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Amounts",
                    name: "header_card_amounts",
                    value: "",
                    popoverMessage: "Value is a number",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Increases",
                    name: "header_card_increases",
                    value: "",
                    popoverMessage:
                        "Value is a number that represents a percentage",
                },
                {
                    type: "Text",
                    placeholder: "Header Card Descriptions",
                    name: "header_card_descriptions",
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
        submitValue={headerSubmitValue}
        SearchFunction={HeaderSearchFunction}
    />
{:else}
    <HeaderStats
        title={"Archive Designer"}
        titleFontSize={"text-6xl"}
        titleColor={"text-black"}
    />
{/if}

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    {#if tableData.includes(undefined) !== true}
        <CardSettings
            title={"Archive Creation"}
            {postURL}
            settings={cardSettings}
            buttonTitle={archiveDesignerButtonTitle}
        />
    {:else}
        <CardSettings
            title={"Archive Creation"}
            {postURL}
            buttonTitle={"Collection Creation"}
        />
    {/if}
</div>
