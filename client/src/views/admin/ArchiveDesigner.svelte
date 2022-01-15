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
                    popoverMessage: "Value may be: 'text'",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substr(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Header Search Input Placeholders",
                    name: "HeaderSearchInputPlaceholders",
                    value: "",
                    popoverMessage:
                        "Individual value may be any string, no commas",
                },
                {
                    type: "Text",
                    placeholder: "Header Search Input Names",
                    name: "HeaderSearchInputNames",
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
                    placeholder: "Table Headers",
                    name: "TableHeaders",
                    value: "",
                },
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
                // {
                //     type: "Text",
                //     placeholder: "Creation Card Await Data",
                //     name: "CreationCardAwaitData",
                //     value: "",
                // },
                {
                    type: "Text",
                    placeholder: "Creation Card Title",
                    name: "CreationCardTitle",
                    value: "",
                    flexdatalistdisabled: true,
                },
                // {
                //     type: "Text",
                //     placeholder: "Creation Card Flexdatalist Data",
                //     name: "CreationCardFlexdatalistData",
                //     value: "",
                //     popoverMessage:
                //         "Type the name of the collection this field will have flexdata from",
                // },
                // {
                //     type: "Text",
                //     placeholder: "Creation Card Flexdatalist Data",
                //     name: "CreationCardFlexdatalistData",
                //     value: "",
                //     popoverMessage:
                //         "Type the name of the collection this field will have flexdata from",
                // },
                {
                    type: "Text",
                    placeholder: "Creation Card Required Field",
                    name: "CreationCardRequiredField",
                    value: "",
                    popoverMessage:
                        "true indicates that the field is required, false indicates it is not",
                    flexdatalistdata: ["true", "false"],
                    flexdataid: Math.random().toString(36).substr(2, 8),
                },
            ],
        },
        {
            Subtitle: "Creation Card Inputs",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Creation Card Input Types",
                    name: "CreationCardInputTypes",
                    value: "",
                },
            ],
            Subtitle: "Creation Card Inputs",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Creation Card Input Types",
                    name: "CreationCardInputTypes",
                    value: "",
                    flexdatalistdata: ["text"],
                    flexdataid: Math.random().toString(36).substr(2, 8),
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Names",
                    name: "CreationCardInputNames",
                    value: "",
                },
                {
                    type: "Text",
                    placeholder: "Creation Card Input Placeholders",
                    name: "CreationCardInputPlaceholders",
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
