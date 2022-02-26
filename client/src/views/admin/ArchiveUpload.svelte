<script>
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";

    let cardSettings = [
        {
            Subtitle: "Upload Files",
            Inputs: [
                {
                    type: "file",
                    placeholder: "Upload JSON",
                    name: "json_file",
                    value: "",
                    popoverMessage: "The JSON file itself to upload",
                    flexdatalistdisabled: true,
                },
                {
                    type: "text",
                    placeholder: "JSON Fields",
                    name: "json_fields",
                    value: "",
                    popoverMessage:
                        "Which outer fields/keys in the JSON should be uploaded?",
                    // flexdatalistdisabled: true,
                },
            ],
        },
        {
            Subtitle: "Upload Data",
            Inputs: [
                {
                    type: "submit",
                    placeholder: "Fie Upload",
                    name: "data_file",
                    value: "Send File",
                    popoverMessage: "Press this button to upload the file",
                    postURL: "/admin/archive-upload/upload-file",
                },
            ],
        },
    ];
</script>

<HeaderStats
    title={"Archive Upload"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
/>

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    <CardSettings
        title={"Archive Upload"}
        settings={cardSettings}
        clearForm={false}
    />
</div>
