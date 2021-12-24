<script>
    // core components
    import CardLineChart from "components/Cards/CardLineChart.svelte";
    import CardBarChart from "components/Cards/CardBarChart.svelte";
    import CardPageVisits from "components/Cards/CardPageVisits.svelte";
    import CardSocialTraffic from "components/Cards/CardSocialTraffic.svelte";

    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";

    // Payload
    const payload = [
        {
            subtitle: "People",
            amount: 500,
            increase: 4.5,
            description: "Last Week",
            id: "People",
        },
        {
            subtitle: "Organizations",
            amount: 1235,
            increase: -523,
            description: "Never",
        },
        {
            subtitle: "People",
            amount: 500,
            increase: 4.5,
            description: "Last Week",
        },
        {
            subtitle: "Organizations",
            amount: 1235,
            increase: -523,
            description: "Never",
        },
        {
            subtitle: "People",
            amount: 500,
            increase: 4.5,
            description: "Last Week",
        },
        {
            subtitle: "Organizations",
            amount: 1235,
            increase: -523,
            description: "Never",
        },
    ];

    const navItems = ["People", "Countries", "Organizations", "Maps"];

    export let location;
</script>

<AdminNavbar {navItems} />
<HeaderStats id={"People"} {payload} title={"People"} />
<div class="px-4 md:px-10 mx-auto w-full m-24">
    <div class="flex flex-wrap ml-8">
        <div class="w-full h-500-px bg-blueGray-700 mt-24 mb-24">
            <h2
                class="text-5xl font-normal leading-normal mt-0 mb-2 text-white"
            >
                Test
            </h2>
        </div>
    </div>
</div>

<HeaderStats id={"Countries"} title={"Countries"} />
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

<HeaderStats id={"Organizations"} title={"Organizations"} />
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
