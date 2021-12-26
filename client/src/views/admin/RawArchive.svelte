<script>
    import { onMount } from "svelte";
    // core components
    import CardLineChart from "components/Cards/CardLineChart.svelte";
    import CardBarChart from "components/Cards/CardBarChart.svelte";
    import CardPageVisits from "components/Cards/CardPageVisits.svelte";
    import CardSocialTraffic from "components/Cards/CardSocialTraffic.svelte";

    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardTable from "components/Cards/CardTable.svelte";
    import DataCreationCard from "components/Cards/DataCreationCard.svelte";

    async function getPeople() {
        const response = await fetch(
            // `${location.origin}/admin/raw-archive/people`
            `http://127.0.0.1:5000/admin/raw-archive/people`
        );
        let people = await response.json();

        if (response.ok) {
            return people;
        } else {
            throw new error(people);
        }
    }

    const people = getPeople();

    // Defines input buttons for HeaderStats
    const DataSettings = {
        // People Start
        People: {
            // People Inputs
            Inputs: [
                {
                    type: "Text",
                    placeholder: "First Name",
                    name: "FirstName",
                },
                {
                    type: "Text",
                    placeholder: "Last Name",
                    name: "LastName",
                },
                {
                    type: "Text",
                    placeholder: "Organizations",
                    name: "Organizations",
                },
                {
                    type: "Text",
                    placeholder: "Titles",
                    name: "Titles",
                },
                {
                    type: "Text",
                    placeholder: "Opinions",
                    name: "Opinion",
                },
                {
                    type: "Submit",
                    placeholder: "Search",
                    name: "",
                },
            ],
            // People Inputs End
            // People Cards
            Cards: [
                {
                    subtitle: "First Name",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Last Name",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Organizations",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Titles",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
            ],
            // People Cards End
            Table: {
                Headers: ["First Name", "Last Name", "Organizations", "Titles"],
                Title: "People",
            },
        },
        // People End
    };

    const navItems = ["People", "Countries", "Organizations", "Maps"];

    // Bind openTab to AdminNavbar component
    let openTab = 0;
    $: console.log(openTab);

    export let location;
</script>

<AdminNavbar bind:openTab {navItems} />

<!-- People -->
<div class={navItems[openTab] === "People" ? "block" : "hidden"}>
    <HeaderStats
        id={"People"}
        cards={DataSettings.People.Cards}
        title={"People"}
        inputs={DataSettings.People.Inputs}
    />
    <div class="block px-4 md:px-10 mx-auto w-full m-12">
        <div class="flex flex-wrap ml-8">
            <div
                class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-8"
            >
                {#await people}
                    <p>Loading...</p>
                {:then people}
                    <CardTable
                        color="dark"
                        data={people}
                        headers={DataSettings.People.Table.Headers}
                        title={DataSettings.People.Table.Title}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
        </div>
    </div>

    <DataCreationCard />
</div>

<!-- Countries -->
<div class={navItems[openTab] === "Countries" ? "block" : "hidden"}>
    <HeaderStats id={"Countries"} title={"Countries"} />
    <div class="px-4 md:px-10 mx-auto w-full m-24">
        <div class="flex flex-wrap">
            <div class="w-full h-500-px bg-blueGray-700 mt-24 mb-24" />
        </div>
    </div>
</div>

<!-- Organizations -->
<div class={navItems[openTab] === "Organizations" ? "block" : "hidden"}>
    <HeaderStats id={"Organizations"} title={"Organizations"} />
    <div class="px-4 md:px-10 mx-auto w-full m-24">
        <div class="flex flex-wrap">
            <div class="w-full h-500-px bg-blueGray-700 mt-24 mb-24" />
        </div>
    </div>
</div>

<!-- Maps, Graphs, Charts -->
<div class={navItems[openTab] === "Maps" ? "block" : "hidden"}>
    <HeaderStats id={"Maps"} title={"Maps"} />
    <div class="px-4 md:px-10 mx-auto w-full m-24">
        <div class="flex flex-wrap">
            <div class="w-full h-500-px bg-blueGray-700 mt-24 mb-24">
                <h2
                    class="text-5xl font-normal leading-normal mt-0 mb-2 text-white"
                >
                    Test
                </h2>
            </div>
        </div>
    </div>
</div>
