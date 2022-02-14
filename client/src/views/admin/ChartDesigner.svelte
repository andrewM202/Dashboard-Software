<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import { tick } from "svelte";
    import { collectionPairsStore } from "../../stores.js";
    // D3 Imports
    import * as d3 from "d3";
    import { Histogram } from "@d3/histogram";

    $: collectionPairs = $collectionPairsStore;

    let tableData = [];
    $: tableData = [collectionPairs];

    let titleSearchInputs;
    $: titleSearchInputs = [
        {
            type: "Text",
            placeholder: "Chart To Edit",
            name: "ChartType",
            flexdatalistdata: ["Bar Chart", "Pie Chart", "Line Chart", "Table"],
            flexdataid: Math.random().toString(36).substring(2, 8),
        },
    ];

    let cardSettings;
    $: cardSettings = [
        {
            Subtitle: "Chart Creation",
            Inputs: [
                {
                    type: "Text",
                    placeholder: "Chart Name",
                    name: "chart_name",
                    value: "",
                    popoverMessage: "Name of the chart",
                    flexdatalistdisabled: true,
                },
                {
                    type: "Text",
                    placeholder: "Chart Type",
                    name: "chart_type",
                    value: "",
                    popoverMessage: "Type of the chart",
                    flexdatalistdata: [
                        "Bar Chart",
                        "Pie Chart",
                        "Line Chart",
                        "Table",
                    ],
                    flexdataid: Math.random().toString(36).substring(2, 8),
                    flexdatalistsingle: true, // Makes it so can only pick one value in flexdatalist
                },
                {
                    type: "Text",
                    placeholder: "Data Pull",
                    name: "chart_type",
                    value: "",
                    popoverMessage:
                        "Which collection and field should you pull the data from? Enter as many fields as needed",
                    flexdatalistdata: collectionPairs,
                    flexdataid: Math.random().toString(36).substring(2, 8),
                    flexdatanone: true,
                },
            ],
        },
        {
            Subtitle: "Create Chart",
            Inputs: [
                {
                    type: "submit",
                    placeholder: "Chart Creation",
                    name: "chart_creation",
                    value: "Start Chart Creation",
                    popoverMessage: "Press this button to create the chart",
                    postURL: "/admin/dashboard/create-chart",
                },
            ],
        },
    ];

    async function createBarChart() {
        await tick();
        let data = [4, 8, 15, 16, 23, 42];
        const div = d3
            .create("div")
            .style("font", "20px sans-serif")
            .style("text-align", "right")
            .style("color", "white")
            .style("height", "100%");

        div.selectAll("div")
            .data(data)
            .join("div")
            .style("background", "steelblue")
            .style("padding", "3px")
            .style("margin", "1px")
            .style("width", (d) => `${d * 20}px`)
            .style(
                "height",
                (d) =>
                    `calc(${(100 * 1) / data.length}% - ${8 / data.length}px)`
            )
            .text((d) => d);

        j$("#ChartCreationContainer").append(div.node());
    }
    createBarChart();

    function HeaderSearchFunction(e) {
        e.preventDefault();
    }
</script>

<AdminNavbar />

<HeaderStats
    title={"Chart Designer"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
    submitValue={"Edit Chart"}
    SearchFunction={HeaderSearchFunction}
/>

{#if tableData.includes(undefined) !== true}
    <div class="mt-4 w-full md:w-11/12 h-auto px-4">
        <CardSettings
            title={"Chart Creation"}
            descButtonTitle={"Creation Mode"}
            settings={cardSettings}
        />
    </div>
{:else}
    <div class="mt-4 w-full md:w-11/12 h-auto px-4">
        <CardSettings
            title={"Chart Creation"}
            descButtonTitle={"Creation Mode"}
            settings={cardSettings}
        />
    </div>
{/if}

<div class="mt-4 w-full md:w-11/12 h-auto px-4">
    <div
        id="ChartCreationContainer"
        class="w-full border-8 border-blueGray-200"
        style="height: 500px; border-radius: 8px; "
    >
        <!-- <svg width="100%" height="100%" /> -->
    </div>
</div>
