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
            />
            <div class="block px-4 md:px-10 mx-auto w-full m-12">
                <div class="flex flex-wrap ml-8">
                    <div
                        class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-8"
                    >
                        <!-- {#await section[1].Table.Data[0]}
                            <p>Loading...</p>
                        {:then data} -->
                        <CardTable
                            color="dark"
                            data={section[1].Table.Data[0]}
                            CollectionName={section[1].CollectionName}
                            headers={section[1].Table.Headers}
                            DBFieldNames={section[1].Table.DBFieldNames}
                            title={section[1].Table.Title}
                        />
                        <!-- {:catch error}
                            <p style="color: red">{error.message}</p>
                        {/await} -->
                    </div>
                </div>
            </div>
            {#if section[1].CreationCard !== undefined}
                <!-- {#if section[1].CreationCard.Data.includes(undefined) !== true} -->
                <DataCreationCard
                    CollectionName={section[1].CollectionName}
                    flexdata={section[1].CreationCard.Flexdatalistdata}
                    title={section[1].CreationCard.Title}
                    inputs={section[1].CreationCard.Inputs}
                />
                <!-- {/if} -->
            {/if}
        </div>
    {/each}
{/if}
