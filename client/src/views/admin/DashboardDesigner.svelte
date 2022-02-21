<script>
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";

    let titleSearchInputs;
    $: titleSearchInputs = [
        {
            type: "Text",
            placeholder: "New Dashboard Name",
            name: "DashboardName",
            // flexdatalistdata: collectionTitles,
            // flexdataid: Math.random().toString(36).substring(2, 8),
            // flexdatafields: ["collection_name"],
        },
    ];

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
            Subtitle: "Create Collection",
            Inputs: [
                {
                    type: "submit",
                    placeholder: "Collection Creation",
                    name: "header_card_subtitles",
                    value: "Create Collection",
                    popoverMessage:
                        "Press this button to create the collection",
                    postURL: "/admin/archive-data/create-collection",
                },
            ],
        },
    ];

    function HeaderSearchFunction(e) {
        e.preventDefault();
    }
</script>

<HeaderStats
    title={"Dashboard Designer"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
    submitValue={"Start Dashboard Creation"}
    SearchFunction={HeaderSearchFunction}
/>

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    <CardSettings
        title={"Archive Upload"}
        descButtonTitle={"Collection Upload"}
        settings={cardSettings}
    />
</div>
