<script>
    import { refreshData } from "../../stores.js";

    // Optional Arguments
    export let title;
    export let inputs;
    export let url;
    export let refreshURL;
    // Error for if form data is not valid
    let error = false;

    function validateData() {
        // Check each input
        for (let input of inputs) {
            if (input.type !== "Submit") {
                let value = j$("#" + input.name).val();
                if (value === "" && input.required === true) {
                    error = "Please Fill All Required Fields.";
                    j$("#" + input.name).attr(
                        "placeholder",
                        `${input.name} Is Required!`
                    );
                }
            }
        }
    }

    function submit(e) {
        e.preventDefault();
        let data = j$("form").serialize();
        // Reset error value
        error = false;
        validateData();
        // Run request if no errors
        if (error === false) {
            j$.ajax({
                type: "POST",
                url: `${location.origin}${url}`,
                data: data,
                success: function () {
                    // Reset placeholder values on success
                    for (let input of inputs) {
                        if (input.type !== "Submit") {
                            j$("#" + input.name).attr(
                                "placeholder",
                                `${input.name}`
                            );
                        }
                    }
                    j$("form").trigger("reset");
                    refreshData(refreshURL);
                },
                error: function (e) {
                    error = "Server Error During Creation.";
                    // Error logging
                    console.log(e.statusText);
                    console.log(e.responseText);
                },
            });
        }
    }
</script>

<div class="px-4 md:px-10 mx-auto w-full">
    <div class="flex flex-wrap ml-8">
        <div class="w-full h-auto bg-blueGray-700 mb-12 p-8">
            <div class="w-full h-full bg-red-500">
                <div class="flex flex-col">
                    <h3
                        class="text-4xl text-center font-normal leading-normal mt-0 mb-2"
                    >
                        {title}
                    </h3>
                    {#if error !== false}
                        <h4
                            class="text-3xl text-center font-normal leading-normal mt-0 mb-2"
                        >
                            {error}
                        </h4>
                    {/if}
                </div>
                <form>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4">
                        {#if inputs !== undefined}
                            {#each inputs as input}
                                <div class="mb-3 py-0 mx-4">
                                    {#if input.type !== "Submit"}
                                        <input
                                            id={input.name}
                                            type={input.type}
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value=""
                                            class="py-3 my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                                        />
                                    {:else}
                                        <input
                                            on:click={submit}
                                            type="Submit"
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value={input.placeholder}
                                            class="py-3 mx-3 my-2 cursor-pointer text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
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
