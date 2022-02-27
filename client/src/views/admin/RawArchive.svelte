<script>
    // core components
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardTable from "components/Cards/CardTable.svelte";
    import DataCreationCard from "components/Cards/DataCreationCard.svelte";

    import { dataSettingsStore, userSettingsStore } from "../../stores.js";

    // Defines input buttons for HeaderStats
    let DataSettings, UserSettings;

    $: DataSettings = $dataSettingsStore;
    $: UserSettings = $userSettingsStore;

    let navItems = [];
    $: if (DataSettings !== undefined) {
        let entries = Object.entries(DataSettings);
        for (let entry of entries) {
            // Only add the item if its not already in there
            if (!navItems.includes(entry[0])) {
                navItems.push(entry[0]);
            }
        }
    }

    // Searh function for headerstats
    function SearchResults(e) {
        e.preventDefault();
        let formSelector;
        // Instead of hard coding form selector, find first form element
        // and set that as selector
        for (let i = 0; i < e.path.length; i++) {
            if (e.path[i].tagName === "FORM") {
                formSelector = e.path[i];
                break;
            }
        }
        // console.log(selector);
        // Get data from form
        let data = j$(formSelector).serialize(); //j$(`form#${formID}`).serialize();
        // Clear form
        j$(formSelector).trigger("reset"); // j$(`form#${formID}`).trigger("reset");
        // Get search results for collection
        j$.ajax({
            type: "POST",
            url: "/admin/archive-data/search-data/",
            data: data,
            success: function (data) {
                // Data returns as string, turn into JSON
                data = JSON.parse(data);
                // On success, replace the correlating collection
                // data in the dataSettingsStore to the updated,
                // filtered data
                for (let entry of Object.entries($dataSettingsStore)) {
                    if (entry[1].CollectionName === data.CollectionName) {
                        $dataSettingsStore[entry[0]].Table.Data = [data.data];
                    }
                }
            },
            error: function (error) {
                console.log("Error");
                console.log(error);
            },
        });
    }

    // Create a mapping for the table so we know
    // form input -> input type

    // Bind openTab to AdminNavbar component
    let openTab = 0;
</script>

{#if DataSettings !== undefined && UserSettings !== undefined}
    <AdminNavbar
        bind:openTab
        {navItems}
        navBarBGColor={UserSettings[0].navigation_color !== undefined &&
        UserSettings[0].navigation_color !== null
            ? `Background-color: ${UserSettings[0].navigation_color}`
            : undefined}
    />
    {#each Object.entries(DataSettings) as section}
        <div class={navItems[openTab] === section[0] ? "block" : "hidden"}>
            <HeaderStats
                id={section[0]}
                cards={section[1].Cards}
                title={navItems[openTab]}
                titleFontSize={"text-4xl"}
                inputs={section[1].HeaderSearchInputs}
                CollectionName={section[1].CollectionName}
                SearchFunction={SearchResults}
                headerBGColor={UserSettings[0].archive_header_color !==
                    undefined && UserSettings[0].archive_header_color !== null
                    ? `Background-color: ${UserSettings[0].archive_header_color}`
                    : undefined}
            />
            <div
                style={UserSettings[0].background_color !== undefined &&
                UserSettings[0].background_color !== null
                    ? `Background-color: ${UserSettings[0].background_color}`
                    : undefined}
                class="block lg:px-10 mx-auto w-full my-12"
            >
                <div class="flex flex-wrap ml-8 w-full">
                    <div
                        class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-6"
                    >
                        <CardTable
                            color="dark"
                            data={section[1].Table.Data[0]}
                            CollectionName={section[1].CollectionName}
                            headers={section[1].Table.Headers}
                            DBFieldNames={section[1].Table.DBFieldNames}
                            title={section[1].Table.Title}
                            tableBGColor={UserSettings[0]
                                .archive_table_color !== undefined &&
                            UserSettings[0].archive_table_color !== null
                                ? `Background-color: ${UserSettings[0].archive_table_color}`
                                : undefined}
                            tableHeaderColor={UserSettings[0]
                                .archive_table_header_color !== undefined &&
                            UserSettings[0].archive_table_header_color !== null
                                ? `Background-color: ${UserSettings[0].archive_table_header_color}`
                                : undefined}
                            tableAltColor={UserSettings[0]
                                .archive_table_alt_color !== undefined &&
                            UserSettings[0].archive_table_alt_color !== null
                                ? UserSettings[0].archive_table_alt_color
                                : undefined}
                            inputs={section[1].CreationCard.Inputs}
                        />
                    </div>
                </div>
            </div>
            <div
                style={UserSettings[0].background_color !== undefined &&
                UserSettings[0].background_color !== null
                    ? `Background-color: ${UserSettings[0].background_color}`
                    : undefined}
                class="lg:px-10 mx-auto w-full"
            >
                <div class="flex flex-wrap ml-8">
                    <div class="w-full h-auto bg-blueGray-700 mb-12 p-6">
                        {#if section[1].CreationCard !== undefined}
                            <DataCreationCard
                                CollectionName={section[1].CollectionName}
                                flexdata={section[1].CreationCard
                                    .Flexdatalistdata}
                                title={section[1].CreationCard.Title}
                                inputs={section[1].CreationCard.Inputs}
                                creationColor={UserSettings[0]
                                    .archive_creation_color !== undefined &&
                                UserSettings[0].archive_creation_color !== null
                                    ? `Background-color: ${UserSettings[0].archive_creation_color}`
                                    : undefined}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/each}
{/if}
