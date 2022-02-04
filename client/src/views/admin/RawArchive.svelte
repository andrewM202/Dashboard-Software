<script>
    // core components
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardTable from "components/Cards/CardTable.svelte";
    import DataCreationCard from "components/Cards/DataCreationCard.svelte";

    import { dataSettingsStore } from "../../stores.js";

    // Defines input buttons for HeaderStats
    let DataSettings;

    $: DataSettings = $dataSettingsStore;

    let navItems = [];
    $: if (DataSettings !== undefined) {
        let entries = Object.entries(DataSettings);
        for (let entry of entries) {
            navItems.push(entry[0]);
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

    // Bind openTab to AdminNavbar component
    let openTab = 0;
</script>

{#if DataSettings !== undefined}
    <AdminNavbar bind:openTab {navItems} />
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
            />
            <div class="block lg:px-10 mx-auto w-full my-12">
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
                        />
                    </div>
                </div>
            </div>
            <div class="lg:px-10 mx-auto w-full">
                <div class="flex flex-wrap ml-8">
                    <div class="w-full h-auto bg-blueGray-700 mb-12 p-6">
                        {#if section[1].CreationCard !== undefined}
                            <DataCreationCard
                                CollectionName={section[1].CollectionName}
                                flexdata={section[1].CreationCard
                                    .Flexdatalistdata}
                                title={section[1].CreationCard.Title}
                                inputs={section[1].CreationCard.Inputs}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    {/each}
{/if}
