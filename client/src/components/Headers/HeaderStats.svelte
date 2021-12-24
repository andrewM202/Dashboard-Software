<script>
    // core components
    import CardStats from "components/Cards/CardStats.svelte";

    // Optional Arguments
    export let payload;
    export let id = "";
    export let title;
</script>

<!-- Header -->
<div class="relative bg-red-500 md:pt-32 pb-32 pt-12" {id}>
    <div class="px-4 md:px-10 mx-auto w-full">
        <div>
            {#if title !== undefined}
                <h3
                    class="text-4xl text-center font-normal leading-normal mt-0 mb-2 text-orange-800"
                >
                    {title}
                </h3>
            {/if}
            <!-- Card stats -->
            <div class="flex flex-wrap">
                {#if payload !== undefined}
                    {#each payload as pkg}
                        <div class="w-full lg:w-6/12 xl:w-3/12 p-4">
                            <CardStats
                                statSubtitle={pkg.subtitle}
                                statTitle={pkg.amount}
                                statArrow="up"
                                statPercent={pkg.increase}
                                statPercentColor={pkg.increase >= 0
                                    ? "text-emerald-500"
                                    : "text-red-500"}
                                statDescripiron="Since {pkg.description}"
                                statIconName="far fa-chart-bar"
                                statIconColor="bg-red-500"
                            />
                        </div>
                    {/each}
                {:else}
                    <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
                        <CardStats
                            statSubtitle="TRAFFIC"
                            statTitle="350,897"
                            statArrow="up"
                            statPercent="3.48"
                            statPercentColor="text-emerald-500"
                            statDescripiron="Since last month"
                            statIconName="far fa-chart-bar"
                            statIconColor="bg-red-500"
                        />
                    </div>
                    <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
                        <CardStats
                            statSubtitle="NEW USERS"
                            statTitle="2,356"
                            statArrow="down"
                            statPercent="3.48"
                            statPercentColor="text-red-500"
                            statDescripiron="Since last week"
                            statIconName="fas fa-chart-pie"
                            statIconColor="bg-orange-500"
                        />
                    </div>
                    <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
                        <CardStats
                            statSubtitle="SALES"
                            statTitle="924"
                            statArrow="down"
                            statPercent="1.10"
                            statPercentColor="text-orange-500"
                            statDescripiron="Since yesterday"
                            statIconName="fas fa-users"
                            statIconColor="bg-pink-500"
                        />
                    </div>
                    <div class="w-full lg:w-6/12 xl:w-3/12 px-4">
                        <CardStats
                            statSubtitle="PERFORMANCE"
                            statTitle="49,65%"
                            statArrow="up"
                            statPercent="12"
                            statPercentColor="text-emerald-500"
                            statDescripiron="Since last month"
                            statIconName="fas fa-percent"
                            statIconColor="bg-emerald-500"
                        />
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>
