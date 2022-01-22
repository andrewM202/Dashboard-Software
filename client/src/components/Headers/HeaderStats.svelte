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

    let id = Math.random().toString(36).substr(2, 8); // Generate random string

    async function positionSearchBar(node) {
        await tick();
        if (inputs !== undefined) {
            if (inputs.length % 2 === 0) {
                j$(node).children().last().css({
                    "grid-column-start": 1,
                    "grid-column-end": 3,
                });
            }
        }
    }
</script>

<!-- Header -->
<div class="relative bg-red-500 md:pt-24 pb-16 pt-16">
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
            {#if inputs !== undefined}
                <div
                    use:positionSearchBar
                    {id}
                    class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full"
                >
                    {#each inputs as input}
                        <div class="mb-3 py-0 mx-4">
                            <input
                                type={input.type}
                                placeholder={input.placeholder}
                                name={input.name}
                                value={input.type === "Submit"
                                    ? input.placeholder
                                    : ""}
                                class="{input.type === 'Submit'
                                    ? 'cursor-pointer'
                                    : ''} px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                    {/each}
                    <div class="mb-3 py-0 mx-4">
                        <input
                            type="Submit"
                            placeholder="Submit"
                            name="Submit"
                            value="Submit"
                            class="cursor-pointer px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                        />
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
