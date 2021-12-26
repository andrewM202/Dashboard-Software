<script>
    // Optional Arguments
    export let title;
    export let inputs;
    export let url;

    function submit(e) {
        e.preventDefault();
        let data = j$("form").serialize();
        j$("form").trigger("reset");
        j$.ajax({
            type: "POST",
            url: `${location.origin}${url}`,
            data: data,
            success: function () {
                // Add person to JS if successful
            },
            error: function () {
                alert("Error Creating");
            },
        });
    }
</script>

<div class="px-4 md:px-10 mx-auto w-full">
    <div class="flex flex-wrap ml-8">
        <div class="w-full h-auto bg-blueGray-700 mb-12 p-8">
            <div class="w-full h-full bg-red-500">
                <h3
                    class="text-4xl text-center font-normal leading-normal mt-0 mb-2"
                >
                    {title}
                </h3>
                <form method="POST" action="/admin/create-person">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4">
                        {#if inputs !== undefined}
                            {#each inputs as input}
                                <div class="mb-3 py-0 mx-4">
                                    {#if input.type !== "Submit"}
                                        <input
                                            type={input.type}
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value=""
                                            class="py-3 my-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                                        />
                                    {:else}
                                        <input
                                            on:click={submit}
                                            type="Submit"
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value={input.placeholder}
                                            class="py-3 mx-3 my-2 cursor-pointer placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                                        />
                                    {/if}
                                </div>
                            {/each}
                        {/if}
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
