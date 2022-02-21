<script>
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";
    import { collectionPairsStore } from "../../stores.js";
    import { tick } from "svelte";
    // D3 Imports
    import { createBarChart } from "components/DesignerCharts/BarChart.svelte";

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

    // async function createBarChart(connectionNodeID, settings) {
    //     await tick();
    //     let data = [4, 8, 15, 16, 23, 42, 12];
    //     const div = d3
    //         .create("div")
    //         .style("font", "20px sans-serif")
    //         .style("text-align", "right")
    //         .style("color", "white")
    //         .style("height", "100%")
    //         .style("overflow", "auto");

    //     div.selectAll("div")
    //         .data(data)
    //         .join("div")
    //         .style("background", "steelblue")
    //         .style("padding", "3px")
    //         .style("margin", "1px")
    //         .style("width", (d) => `${d * 20}px`)
    //         .style("height", (d) => `50px`)
    //         .text((d) => d);

    //     j$(`#${connectionNodeID}`).append(div.node());
    // }
    async function createCharts() {
        await tick();
        createBarChart(j$("#ChartCreationContainer"), "test");
    }
    createCharts();

    function HeaderSearchFunction(e) {
        e.preventDefault();
    }
</script>

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

<div class="mt-4 w-full overflow-x-auto md:w-11/12 h-auto px-4">
    <div
        id="ChartCreationContainer"
        class="w-full overflow-x-auto border-8 border-blueGray-200"
        style="border-radius: 8px; "
    />
</div>
