<script>
    // core components
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardTable from "components/Cards/CardTable.svelte";
    import DataCreationCard from "components/Cards/DataCreationCard.svelte";

    import {
        peopleStore,
        organizationsStore,
        countriesStore,
    } from "../../stores.js";

    let organizations, people, countries;
    $: organizations = $organizationsStore;
    $: people = $peopleStore;
    $: countries = $countriesStore;

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
                Headers: [
                    "First Name",
                    "Last Name",
                    "Organizations",
                    "Titles",
                    "Opinions",
                ],
                Title: "People",
                DeletionURL: "/admin/delete-person",
                RefreshURL: "/admin/people",
                UpdateURL: "/admin/update-person",
                UpdateFormNames: [
                    "FirstName",
                    "LastName",
                    "Organizations",
                    "Titles",
                    "Opinions",
                ],
                DBFieldNames: [
                    "first_name",
                    "last_name",
                    "organizations",
                    "titles",
                    "opinions",
                ],
            },
            // People Table End
            // People CreationCard Begin
            CreationCard: {
                URL: "/admin/create-person",
                RefreshURL: "/admin/people",
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
                        flexdatalist: true, // Is the flexdatalist enabled
                        flexdataid: "people_organizations", // The input id for the datalist
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
                        name: "Opinions",
                        required: false,
                    },
                    {
                        type: "Submit",
                        placeholder: "Submit",
                        name: "",
                        required: false,
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
                    subtitle: "Affiliations",
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
                DeletionURL: "/admin/delete-organization",
                RefreshURL: "/admin/organizations",
                UpdateURL: "/admin/update-organization",
                UpdateFormNames: ["Name", "Opinions", "Affiliations"],
                Title: "Organizations",
            },
            // Organizations Table End
            // Organizations CreationCard Begin
            CreationCard: {
                URL: "/admin/create-organization",
                RefreshURL: "/admin/organizations",
                Title: "Create Organization",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "Name",
                        name: "Name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Opinions",
                        name: "Opinions",
                        required: false,
                    },
                    {
                        type: "Text",
                        placeholder: "Affiliations",
                        name: "Affiliations",
                        required: false,
                        flexdatalist: true,
                        flexdataid: "organization_affiliations",
                    },
                    {
                        type: "Submit",
                        placeholder: "Submit",
                        name: "",
                        required: false,
                    },
                ],
            },
            // Organizations CreationCard End
        },
        // Organizations End
        // Countries Start
        Countries: {
            // Countries Inputs
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Name",
                    name: "Name",
                },
                {
                    type: "Text",
                    placeholder: "Landlocked",
                    name: "Landlocked",
                },
                {
                    type: "Text",
                    placeholder: "Capital",
                    name: "Capital",
                },
                {
                    type: "Submit",
                    placeholder: "Search",
                    name: "",
                },
            ],
            // Countries Inputs End
            // Countries Cards
            Cards: [
                {
                    subtitle: "Area",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Capital",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Landlocked",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Languages",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Lat Longitude",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Name",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Population",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
                {
                    subtitle: "Subregion",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
            ],
            // Countries Cards End
            // Countries Table Begin
            Table: {
                Headers: [
                    "Area",
                    "Capital",
                    "Currencies",
                    "Landlocked",
                    "Languages",
                    "Lat Long",
                    "Name",
                    "Population",
                    "Subregion",
                ],
                Title: "Countries",
                DeletionURL: "",
                RefreshURL: "",
                Modification: false,
                DBFieldNames: [
                    "country_area",
                    "country_capital",
                    "country_currencies",
                    "country_landlocked",
                    "country_languages",
                    "country_latlng",
                    "country_name",
                    "country_population",
                    "country_subregion",
                ],
            },
            // Countries Table End
        },
        // Countries End
    };

    const navItems = ["People", "Countries", "Organizations", "Maps"];

    // Bind openTab to AdminNavbar component
    let openTab = 0;
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
                        DeletionURL={DataSettings.People.Table.DeletionURL}
                        RefreshURL={DataSettings.People.Table.RefreshURL}
                        UpdateURL={DataSettings.People.Table.UpdateURL}
                        UpdateFormNames={DataSettings.People.Table
                            .UpdateFormNames}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
        </div>
    </div>
    {#if organizations !== undefined}
        <DataCreationCard
            flexdata={organizations}
            url={DataSettings.People.CreationCard.URL}
            title={DataSettings.People.CreationCard.Title}
            inputs={DataSettings.People.CreationCard.Inputs}
            refreshURL={DataSettings.People.CreationCard.RefreshURL}
        />
    {/if}
</div>

<!-- Countries -->
<div class={navItems[openTab] === "Countries" ? "block" : "hidden"}>
    <HeaderStats
        id={"Countries"}
        title={"Countries"}
        cards={DataSettings.Countries.Cards}
        inputs={DataSettings.Countries.Inputs}
    />
    <div class="block px-4 md:px-10 mx-auto w-full m-12">
        <div class="flex flex-wrap ml-8">
            <div
                class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-8"
            >
                {#await countries}
                    <p>Loading...</p>
                {:then countries}
                    <CardTable
                        color="dark"
                        data={countries}
                        headers={DataSettings.Countries.Table.Headers}
                        DBFieldNames={DataSettings.Countries.Table.DBFieldNames}
                        title={DataSettings.Countries.Table.Title}
                        DeletionURL={DataSettings.Countries.Table.DeletionURL}
                        RefreshURL={DataSettings.Countries.Table.RefreshURL}
                        Modification={DataSettings.Countries.Table.Modification}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
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
                        DeletionURL={DataSettings.Organizations.Table
                            .DeletionURL}
                        RefreshURL={DataSettings.Organizations.Table.RefreshURL}
                        UpdateURL={DataSettings.Organizations.Table.UpdateURL}
                        UpdateFormNames={DataSettings.Organizations.Table
                            .UpdateFormNames}
                    />
                {:catch error}
                    <p style="color: red">{error.message}</p>
                {/await}
            </div>
        </div>
    </div>
    {#await organizations}
        <p>Loading...</p>
    {:then organizations}
        <DataCreationCard
            flexdata={organizations}
            url={DataSettings.Organizations.CreationCard.URL}
            title={DataSettings.Organizations.CreationCard.Title}
            inputs={DataSettings.Organizations.CreationCard.Inputs}
            refreshURL={DataSettings.Organizations.CreationCard.RefreshURL}
        />
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
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
