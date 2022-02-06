<script>
    // core components
    import CardStats from "components/Cards/CardStats.svelte";
    import { tick } from "svelte";

    // Optional Arguments
    export let cards;
    export let title;
    export let titleColor; // Pass in class for text color
    export let titleFontSize; // Pass in class for font size
    export let inputs;
    export let CollectionName;
    export let SearchFunction; // Pass in the search function for the form
    export let submitValue; // Value of the submit button
    export let headerBGColor;

    // let id = Math.random().toString(36).substr(2, 8); // Generate random string
    let submitButtonID = Math.random().toString(36).substr(2, 8);
    let submitID = Math.random().toString(36).substring(2, 8);

    async function positionSearchBar() {
        await tick();
        if (inputs !== undefined) {
            if (inputs.length % 2 === 0) {
                j$(`#${submitID}`).css({
                    width: "100%",
                });
            }
        }
    }

    positionSearchBar();

    async function styleFlexData() {
        await tick();
        let interval = setInterval(function () {
            if (j$("ul.flexdatalist-results").length !== 0) {
                clearInterval(interval);
                j$("ul.flexdatalist-results").css({
                    "border-width": "0",
                });
                j$("#headerStatsFlexForm-flexdatalist").click(function () {
                    j$(".item").css({ cursor: "pointer" });
                });
            }
        }, 10);
    }
</script>

<!-- Header -->
<div class="relative bg-red-500 md:pt-24 pt-16" style={headerBGColor}>
    <div class="px-4 py-2 md:px-10 mx-auto w-full">
        <div>
            {#if title !== undefined}
                <h3
                    class="{titleColor} {titleFontSize} text-center font-normal leading-normal mt-0 mb-2"
                >
                    {title}
                </h3>
            {/if}
            <!-- Card stats -->
            <div class="flex flex-wrap justify-center py-4">
                {#if cards !== undefined}
                    {#each cards as card}
                        <div class="w-full lg:w-6/12 xl:w-3/12 px-4 py-2">
                            <CardStats
                                statSubtitle={card.subtitle}
                                statTitle={card.amount}
                                statArrow="up"
                                statPercent={card.increase}
                                statPercentColor={card.increase >= 0
                                    ? "text-emerald-500"
                                    : "text-red-500"}
                                statDescripiron="Since {card.description}"
                                statIconName="far fa-chart-bar"
                                statIconColor="bg-red-500"
                            />
                        </div>
                    {/each}
                {/if}
            </div>
            <!-- Inputs -->
            {#if inputs !== undefined}
                <div class="flex-auto py-10 pt-0">
                    <form>
                        <input
                            type="hidden"
                            name="CollectionName"
                            value={CollectionName}
                        />
                        <div class="flex flex-wrap">
                            {#each inputs as input}
                                <div class="w-full lg:w-6/12 py-2 px-4">
                                    <div class="relative w-full mb-3">
                                        {#if input.flexdatalistdata !== undefined}
                                            <input
                                                use:styleFlexData
                                                list={input.flexdataid}
                                                data-min-length="0"
                                                type="text"
                                                placeholder={input.placeholder}
                                                name={input.name}
                                                id="headerStatsFlexForm"
                                                class="flexdatalist border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                            />
                                            <datalist id={input.flexdataid}>
                                                {#each input.flexdatalistdata as datarow}
                                                    <option value={datarow} />
                                                {/each}
                                            </datalist>
                                        {:else}
                                            <input
                                                type={input.type}
                                                placeholder={input.placeholder}
                                                name={input.name}
                                                value={input.type === "Submit"
                                                    ? input.placeholder
                                                    : ""}
                                                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                            />
                                        {/if}
                                    </div>
                                </div>
                            {/each}
                            <div
                                class="w-full lg:w-6/12 py-2 px-4"
                                id={submitID}
                            >
                                <div class="relative w-full mb-3">
                                    <input
                                        on:click={SearchFunction}
                                        id={submitButtonID}
                                        type="Submit"
                                        placeholder="Submit"
                                        name="submit"
                                        value={submitValue !== undefined
                                            ? submitValue
                                            : "Submit"}
                                        class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                    />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            {/if}
        </div>
    </div>
</div>
