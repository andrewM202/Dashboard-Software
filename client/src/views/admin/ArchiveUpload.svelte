<script>
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import { userSettingsStore } from "../../stores.js";

    let settingsConfig;
    $: settingsConfig = $userSettingsStore;

    let cardSettings;
    $: cardSettings = [
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
                    submitFunction: fileSubmit,
                },
            ],
        },
    ];

    let alreadySubmitted = false;
    function fileSubmit(e) {
        e.preventDefault();
        let data = j$(`#archCreateForm`).serialize();
        let postURL = e.srcElement.attributes.posturl.nodeValue;
        data = new FormData(j$(`#archCreateForm`)[0]);
        j$.ajax({
            type: "POST",
            url: `${location.origin}${postURL}`,
            data: data,
            mimeType: "multipart/form-data",
            contentType: false,
            processData: false,
            success: function (data) {
                data = JSON.parse(data);
                // Reset form
                // j$(`#archCreateForm`).trigger("reset");
                // Scroll to top of window
                j$("html, body").animate({ scrollTop: "0px" }, 500);
                // Remove flexdatalist values
                // j$("li.value").remove();
                let cardSettingsClone = cardSettings;
                if (alreadySubmitted === false) {
                    alreadySubmitted = true;
                    cardSettingsClone[0].Inputs.push({
                        type: "text",
                        placeholder: "JSON Fields",
                        name: "json_fields",
                        value: "",
                        popoverMessage:
                            "Which outer fields/keys in the JSON should be uploaded?",
                        flexdatalistdata: data[1],
                        flexdataid: Math.random().toString(36).substring(2, 8),
                    });
                    cardSettingsClone[0].Inputs.push({
                        type: "textarea",
                        placeholder: "JSON Text",
                        name: "json_text",
                        value: JSON.stringify(data[0], undefined, 2),
                        popoverMessage: "The actual JSON text",
                        readonly: true,
                    });
                } else {
                    // Set flexdatalistdata for JSON Fields
                    cardSettingsClone[0].Inputs[1].flexdatalistdata = data[1];
                    // Set text area value to the uploaded JSON
                    cardSettingsClone[0].Inputs[2].value = JSON.stringify(
                        data[0],
                        undefined,
                        2
                    );
                }
                cardSettings = cardSettingsClone;
            },
            error: function (e) {
                // Error logging
                console.log(e.statusText);
                console.log(e.responseText);
                // Scroll to top of window
                j$("html, body").animate({ scrollTop: "0px" }, 500);
            },
        });
    }

    // Bind openTab to AdminNavbar component
    let openTab = 0;
    let navItems = ["Manual Upload", "Automatic Upload"];
</script>

{#if settingsConfig !== undefined}
    <AdminNavbar
        bind:openTab
        navBarBGColor={settingsConfig[0].navigation_color !== undefined &&
        settingsConfig[0].navigation_color !== null
            ? `Background-color: ${settingsConfig[0].navigation_color}`
            : undefined}
        {navItems}
    />
{:else}
    <AdminNavbar bind:openTab {navItems} />
{/if}

{#if openTab === 0}
    <HeaderStats
        title={"Archive Upload"}
        titleFontSize={"text-6xl"}
        titleColor={"text-black"}
    />

    <div class="mt-4 w-full md:w-11/12 h-auto px-4">
        <CardSettings
            title={"Manual Upload"}
            settings={cardSettings}
            clearForm={false}
        />
    </div>
{:else if openTab === 1}
    <HeaderStats
        title={"Archive Upload"}
        titleFontSize={"text-6xl"}
        titleColor={"text-black"}
    />

    <div class="mt-4 w-full md:w-11/12 h-auto px-4">
        <CardSettings
            title={"Automatic Upload"}
            settings={cardSettings}
            clearForm={false}
        />
    </div>
{/if}
