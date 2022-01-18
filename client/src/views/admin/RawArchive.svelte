<script>
    // core components
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardTable from "components/Cards/CardTable.svelte";
    import DataCreationCard from "components/Cards/DataCreationCard.svelte";

    import {
        peopleStore,
        peopleTypesStore,
        organizationsStore,
        organizationTypesStore,
        countriesStore,
    } from "../../stores.js";

    let organizations, organizationTypes, people, peopleTypes, countries;
    $: organizations = $organizationsStore;
    $: organizationTypes = $organizationTypesStore;
    $: people = $peopleStore;
    $: peopleTypes = $peopleTypesStore;
    $: countries = $countriesStore;

    let tableData = [];
    $: tableData = [
        organizations,
        organizationTypes,
        people,
        peopleTypes,
        countries,
    ];

    // Defines input buttons for HeaderStats
    let DataSettings;
    $: DataSettings = {
        // People Start
        People: {
            CollectionName: "people_watch",
            // People Inputs
            HeaderSearchInputs: [
                {
                    type: "Text",
                    placeholder: "First Name",
                    name: "first_name",
                },
                {
                    type: "Text",
                    placeholder: "Last Name",
                    name: "last_name",
                },
                {
                    type: "Text",
                    placeholder: "Organizations",
                    name: "organizations",
                },
                {
                    type: "Text",
                    placeholder: "Titles",
                    name: "titles",
                },
                {
                    type: "Text",
                    placeholder: "Opinions",
                    name: "opinions",
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
                AwaitData: [people],
                Headers: [
                    "First Name",
                    "Last Name",
                    "Person Type",
                    "Organizations",
                    "Titles",
                    "Opinions",
                ],
                Title: "People",
                DBFieldNames: [
                    "first_name",
                    "last_name",
                    "person_type",
                    "organizations",
                    "titles",
                    "opinions",
                ],
            },
            // People Table End
            // People CreationCard Begin
            CreationCard: {
                AwaitData: [organizations, peopleTypes],
                Title: "Create Person",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "First Name",
                        name: "first_name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Last Name",
                        name: "last_name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Person Type",
                        name: "person_type",
                        required: false,
                        flexdatalistdata: peopleTypes,
                        flexdatafields: ["person_type_name"],
                        flexdataid: Math.random().toString(36).substring(2, 8),
                    },
                    {
                        type: "Text",
                        placeholder: "Organizations",
                        name: "organizations",
                        required: false,
                        flexdatalistdata: organizations, // Which collection to use?
                        flexdatafields: ["name"], // Which field from collection?
                        flexdataid: Math.random().toString(36).substring(2, 8),
                    },
                    {
                        type: "Text",
                        placeholder: "Titles",
                        name: "titles",
                        required: false,
                    },
                    {
                        type: "Text",
                        placeholder: "Opinions",
                        name: "opinions",
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
        // People Types Start
        PeopleTypes: {
            CollectionName: "person_type",
            // People Types Inputs
            HeaderSearchInputs: [
                {
                    type: "Text",
                    placeholder: "Person Type Name",
                    name: "PersonTypeName",
                },
                {
                    type: "Text",
                    placeholder: "Acronyms",
                    name: "PersonTypeAcronyms",
                },
                {
                    type: "Submit",
                    placeholder: "Search",
                    name: "",
                },
            ],
            // People Types Inputs End
            // People Types Cards
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
            // People Types Cards End
            // People Types Table Begin
            Table: {
                AwaitData: [peopleTypes],
                Headers: ["Person Type Name", "Acronyms"],
                DBFieldNames: ["person_type_name", "person_type_acronyms"],
                Title: "People Types",
            },
            // People Types Table End
            // People Types CreationCard Begin
            CreationCard: {
                AwaitData: [peopleTypes],
                Title: "Create Person Type",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "Person Type Name",
                        name: "person_type_name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Acronyms",
                        name: "person_type_acronyms",
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
            // People Types CreationCard End
        },
        // People Types End
        // Organizations Start
        Organizations: {
            CollectionName: "organizations",
            // Organizations Inputs
            HeaderSearchInputs: [
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
                AwaitData: [organizations],
                Headers: [
                    "Name",
                    "Organization Type",
                    "Opinions",
                    "Affiliations",
                ],
                DBFieldNames: [
                    "name",
                    "organ_type",
                    "opinions",
                    "affiliations",
                ],
                Title: "Organizations",
            },
            // Organizations Table End
            // Organizations CreationCard Begin
            CreationCard: {
                AwaitData: [organizations],
                Title: "Create Organization",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "Name",
                        name: "name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Organization Type",
                        name: "organ_type",
                        required: true,
                        flexdatalistdata: organizationTypes, // Which collection to use?
                        flexdatafields: ["organ_type_name"], // Which field from collection?
                        flexdataid: Math.random().toString(36).substring(2, 8),
                    },
                    {
                        type: "Text",
                        placeholder: "Opinions",
                        name: "opinions",
                        required: false,
                    },
                    {
                        type: "Text",
                        placeholder: "Affiliations",
                        name: "affiliations",
                        required: false,
                        flexdatalistdata: organizations, // Which collection to use?
                        flexdatafields: ["name"], // Which field from collection?
                        flexdataid: Math.random().toString(36).substring(2, 8),
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
        // Organization Types Start
        OrganizationTypes: {
            CollectionName: "organization_type",
            // Organization Types Inputs
            HeaderSearchInputs: [
                {
                    type: "Text",
                    placeholder: "Organization Type Name",
                    name: "OrganizationTypeName",
                },
                {
                    type: "Text",
                    placeholder: "Acronyms",
                    name: "OrganizationTypeAcronyms",
                },
                {
                    type: "Submit",
                    placeholder: "Search",
                    name: "",
                },
            ],
            // Organization Types Inputs End
            // Organization Types Cards
            Cards: [
                {
                    subtitle: "Organization Type Name",
                    amount: 500,
                    increase: 4.5,
                    description: "Last Week",
                },
                {
                    subtitle: "Acronyms",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
            ],
            // Organization Types Cards End
            // Organization Types Table Begin
            Table: {
                AwaitData: [organizationTypes],
                Headers: ["Organization Type Name", "Acronyms"],
                DBFieldNames: ["organ_type_name", "organ_type_acronyms"],
                Title: "Organization Types",
            },
            // Organization Types Table End
            // Organization Types CreationCard Begin
            CreationCard: {
                AwaitData: [organizationTypes],
                Title: "Create Organization Type",
                Inputs: [
                    {
                        type: "Text",
                        placeholder: "Organization Type Name",
                        name: "organ_type_name",
                        required: true,
                    },
                    {
                        type: "Text",
                        placeholder: "Acronyms",
                        name: "organ_type_acronyms",
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
            // Organization Types CreationCard End
        },
        // Organization Types End
        // Countries Start
        Countries: {
            CollectionName: "countries",
            // Countries Inputs
            HeaderSearchInputs: [
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
                    subtitle: "Currencies",
                    amount: 1235,
                    increase: -523,
                    description: "Never",
                },
            ],
            // Countries Cards End
            // Countries Table Begin
            Table: {
                AwaitData: [countries],
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

    const navItems = [
        "People",
        "Countries",
        "Organizations",
        "People Types",
        "Organization Types",
    ];

    // Bind openTab to AdminNavbar component
    let openTab = 0;
</script>

<AdminNavbar bind:openTab {navItems} title={"Raw Archive"} />
{#if tableData.includes(undefined) !== true}
    {#each Object.entries(DataSettings) as section}
        <div
            class={navItems[openTab].replace(" ", "") === section[0]
                ? "block"
                : "hidden"}
        >
            <HeaderStats
                id={section[0]}
                cards={section[1].Cards}
                title={navItems[openTab]}
                titleFontSize={"text-4xl"}
                inputs={section[1].HeaderSearchInputs}
            />
            <div class="block px-4 md:px-10 mx-auto w-full m-12">
                <div class="flex flex-wrap ml-8">
                    <div
                        class="w-full h-600-px bg-blueGray-700 mt-12 mb-12 flex justify-center items-center p-8"
                    >
                        {#await section[1].Table.AwaitData[0]}
                            <p>Loading...</p>
                        {:then data}
                            <CardTable
                                color="dark"
                                {data}
                                CollectionName={section[1].CollectionName}
                                headers={section[1].Table.Headers}
                                DBFieldNames={section[1].Table.DBFieldNames}
                                title={section[1].Table.Title}
                            />
                        {:catch error}
                            <p style="color: red">{error.message}</p>
                        {/await}
                    </div>
                </div>
            </div>
            {#if section[1].CreationCard !== undefined}
                {#if section[1].CreationCard.AwaitData.includes(undefined) !== true}
                    <DataCreationCard
                        CollectionName={section[1].CollectionName}
                        flexdata={section[1].CreationCard.Flexdatalistdata}
                        title={section[1].CreationCard.Title}
                        inputs={section[1].CreationCard.Inputs}
                    />
                {/if}
            {/if}
        </div>
    {/each}
{/if}
