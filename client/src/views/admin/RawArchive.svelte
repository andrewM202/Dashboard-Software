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

    async function getResource(pathname) {
        const response = await fetch(`${location.origin}${pathname}`);
        let payload = await response.json();

        if (response.ok) {
            return payload;
        } else {
            throw new error(payload);
        }
    }

    let people, organizations;
    j$(document).ready(function () {
        people = getResource("/admin/people");
        organizations = getResource("/admin/organizations");
    });

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
            // People Table Begin
            Table: {
                Headers: ["First Name", "Last Name", "Organizations", "Titles"],
                Title: "People",
                DBFieldNames: [
                    "first_name",
                    "last_name",
                    "organizations",
                    "titles",
                ],
            },
            // People Table End
            // People CreationCard Begin
            CreationCard: {
                URL: "/admin/create-person",
                Title: "Create Person",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "First Name",
                        name: "FirstName",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Last Name",
                        name: "LastName",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Organizations",
                        name: "Organizations",
                        required: false,
                    },
                    {
                        type: "Text",
                        placeholder: "Titles",
                        name: "Titles",
                        required: false,
                    },
                    {
                        type: "Text",
                        placeholder: "Opinions",
                        name: "Opinion",
                        required: false,
                    },
                    {
                        type: "Submit",
                        placeholder: "Submit",
                        name: "",
                    },
                ],
            },
            // People CreationCard End
        },
        // People End
        // Organizations Start
        Organizations: {
            // Organizations Inputs
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Name",
                    name: "FirstName",
                },
                {
                    type: "Text",
                    placeholder: "Opinions",
                    name: "Opinions",
                },
                {
                    type: "Text",
                    placeholder: "Affiliations",
                    name: "Affiliations",
                },
                {
                    type: "Submit",
                    placeholder: "Search",
                    name: "",
                },
            ],
            // Organizations Inputs End
            // Organizations Cards
            Cards: [
                {
                    subtitle: "Name",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Opinions",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Affiliatons",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
            ],
            // Organizations Cards End
            // Organizations Table Begin
            Table: {
                Headers: ["Name", "Opinions", "Affiliations"],
                DBFieldNames: ["name", "opinions", "affiliations"],
                Title: "Organizations",
            },
            // Organizations Table End
            // Organizations CreationCard Begin
            CreationCard: {
                URL: "/admin/create-organization",
                Title: "Create Organization",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "Name",
                        name: "Name",
                    },
                    {
                        type: "Text",
                        placeholder: "Opinions",
                        name: "Opinions",
                    },
                    {
                        type: "Text",
                        placeholder: "Affiliatons",
                        name: "Affiliatons",
                    },
                    {
                        type: "Submit",
                        placeholder: "Submit",
                        name: "",
                    },
                ],
            },
            // Organizations CreationCard End
        },
        // Organizations End
    };

    const navItems = ["People", "Countries", "Organizations", "Maps"];

    // Bind openTab to AdminNavbar component
    let openTab = 0;

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
                        DBFieldNames={DataSettings.People.Table.DBFieldNames}
                        title={DataSettings.People.Table.Title}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
        </div>
    </div>
    <DataCreationCard
        url={DataSettings.People.CreationCard.URL}
        title={DataSettings.People.CreationCard.Title}
        inputs={DataSettings.People.CreationCard.Inputs}
    />
</div>

<!-- Countries -->
<div class={navItems[openTab] === "Countries" ? "block" : "hidden"}>
    <HeaderStats id={"Countries"} title={"Countries"} />
    <div class="px-4 md:px-10 mx-auto w-full m-12">
        <div class="flex flex-wrap">
            <div class="w-full h-500-px bg-blueGray-700 mt-12 mb-12" />
        </div>
    </div>
</div>

<!-- Organizations -->
<div class={navItems[openTab] === "Organizations" ? "block" : "hidden"}>
    <HeaderStats
        id={"Organizations"}
        title={"Organizations"}
        cards={DataSettings.Organizations.Cards}
        inputs={DataSettings.Organizations.Inputs}
    />
    <div class="block px-4 md:px-10 mx-auto w-full m-12">
        <div class="flex flex-wrap ml-8">
            <div
                class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-8"
            >
                {#await organizations}
                    <p>Loading...</p>
                {:then organizations}
                    <CardTable
                        color="dark"
                        data={organizations}
                        DBFieldNames={DataSettings.Organizations.Table
                            .DBFieldNames}
                        headers={DataSettings.Organizations.Table.Headers}
                        title={DataSettings.Organizations.Table.Title}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
        </div>
    </div>
    <DataCreationCard
        url={DataSettings.Organizations.CreationCard.URL}
        title={DataSettings.Organizations.CreationCard.Title}
        inputs={DataSettings.Organizations.CreationCard.Inputs}
    />
</div>

<!-- Maps, Graphs, Charts -->
<div class={navItems[openTab] === "Maps" ? "block" : "hidden"}>
    <HeaderStats id={"Maps"} title={"Maps"} />
    <div class="px-4 md:px-10 mx-auto w-full m-12">
        <div class="flex flex-wrap">
            <div class="w-full h-500-px bg-blueGray-700 mt-12 mb-12">
                <h2
                    class="text-5xl font-normal leading-normal mt-0 mb-2 text-white"
                >
                    Test
                </h2>
            </div>
        </div>
    </div>
</div>
