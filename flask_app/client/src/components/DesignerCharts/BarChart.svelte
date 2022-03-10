<script context="module">
    import { tick } from "svelte";
    import * as d3 from "d3";

    async function barChart(connectionNode, settings) {
        await tick();
        let data = [4, 8, 15, 16, 23, 42, 12];
        const div = d3
            .create("div")
            .style("font", "20px sans-serif")
            .style("text-align", "right")
            .style("color", "white")
            .style("height", "100%")
            .style("overflow", "auto");

        div.selectAll("div")
            .data(data)
            .join("div")
            .style("background", "steelblue")
            .style("padding", "3px")
            .style("margin", "1px")
            .style("width", (d) => `${d * 20}px`)
            .style("height", (d) => `50px`)
            .text((d) => d);

        j$(connectionNode).append(div.node());
    }

    export let createBarChart = barChart;
</script>
