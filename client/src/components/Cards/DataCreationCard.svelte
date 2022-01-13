<script>
    import { refreshData } from "../../stores.js";
    import Flexdata from "../Plugin/Flexdata.svelte";

    // Optional Arguments
    export let title;
    export let inputs;
    export let url;
    export let refreshURL;
    export let flexdata;
    export let CollectionName;

    let flexdatalist = [];

    let formID = Math.random().toString(36).substr(2, 8); // Generate random string

    // Simplify flexdata data so looping does not
    // Have to occur in the HTML with templating engine
    for (let index in flexdata) {
        flexdatalist.push({
            Fieldname: flexdata[index].Field,
            FieldValues: [],
        });
        for (let datafield of flexdata[index].Data) {
            for (let obj of datafield) {
                for (let entry of Object.entries(obj)) {
                    for (let field of flexdata[index].DBFieldNames) {
                        if (entry[0] === field) {
                            flexdatalist[index].FieldValues.push(entry[1]);
                        }
                    }
                }
            }
        }
    }

    // Error for if form data is not valid
    let error = false;

    // If close button clicked reset error
    function closeAlert() {
        error = false;
    }

    // Setting min-width of multiple flexdatalist input,
    // otherwise its super small like 40px
    function runPreJS() {
        if (inputs.length % 2 === 1) {
            j$("div#rawArchiveTableContainer.grid div:last-child").css({
                "grid-column-start": 1,
                "grid-column-end": 3,
            });
        }
        j$("li.input-container.flexdatalist-multiple-value input").css(
            "min-width",
            "150px"
        );
    }

    function validateData() {
        // Check each input
        for (let input of inputs) {
            if (input.type !== "Submit") {
                let value = j$("#" + input.name).val();
                if (value === "" && input.required === true) {
                    error = "Please Fill All Required Fields.";
                    j$("#" + input.name).attr(
                        "placeholder",
                        `${input.placeholder} Is Required!`
                    );
                }
            }
        }
    }

    function submit(e) {
        e.preventDefault();
        let data = j$(`#${formID}`).serialize();
        // Reset error value
        error = false;
        validateData();
        // Run request if no errors
        if (error === false) {
            j$.ajax({
                type: "POST",
                url: `${location.origin}${url}`,
                // url: `${location.origin}/admin/archive-data/${CollectionName}`,
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
                    j$(`#${formID}`).trigger("reset");
                    // refreshData(refreshURL);
                    refreshData(`/admin/archive-data/${CollectionName}`);
                    // Remove flexdatalist values
                    j$("li.value").remove();
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

<div use:runPreJS />
<div class="px-4 md:px-10 mx-auto w-full">
    <div class="flex flex-wrap ml-8">
        <div class="w-full h-auto bg-blueGray-700 mb-12 p-8">
            <div class="w-full h-full bg-red-500">
                <div class="flex flex-col items-center w-full">
                    <h3
                        class="text-4xl text-center font-normal leading-normal mt-0 mb-2"
                    >
                        {title}
                    </h3>
                    {#if error !== false}
                        <div
                            class="text-white w-3/4 px-6 py-4 border-0 rounded relative mb-4 bg-blueGray-700"
                        >
                            <span
                                class="text-xl inline-block mr-5 align-middle"
                            >
                                <i class="fas fa-bell" />
                            </span>
                            <span class="inline-block align-middle mr-8">
                                <b class="capitalize">Error! </b>{error}
                            </span>
                            <button
                                on:click={closeAlert}
                                class="absolute pr-4 bg-transparent text-2xl font-semibold leading-none right-0 top-0 mt-4 mr-6 outline-none focus:outline-none"
                            >
                                <span>×</span>
                            </button>
                        </div>
                    {/if}
                </div>
                <form id={formID}>
                    <div
                        id="rawArchiveTableContainer"
                        class="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4"
                    >
                        {#if inputs !== undefined}
                            {#each inputs as input}
                                <div class="mb-3 py-0 mx-4">
                                    <!-- Flexdatalist Inputs -->
                                    {#if input.flexdatalist !== undefined}
                                        <input
                                            list={input.flexdataid !== undefined
                                                ? input.flexdataid
                                                : input.name}
                                            multiple
                                            type={input.type}
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value=""
                                            class="{input.flexdatalist === true
                                                ? 'flexdatalist'
                                                : ''} py-3 my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                                            data-min-length="0"
                                        />
                                        {#if input.flexdatalist === true && flexdata !== undefined}
                                            <datalist
                                                id={input.flexdataid !==
                                                undefined
                                                    ? input.flexdataid
                                                    : input.name}
                                            >
                                                {#each flexdatalist as datafield}
                                                    {#if datafield.Fieldname === input.name}
                                                        {#each datafield.FieldValues as value}
                                                            <option
                                                                >{value}</option
                                                            >
                                                        {/each}
                                                    {/if}
                                                {/each}
                                            </datalist>
                                        {/if}
                                        <!-- Any Input Not A Submit Or Flexdatalist -->
                                    {:else if input.type !== "Submit"}
                                        <input
                                            id={input.name}
                                            type={input.type}
                                            placeholder={input.placeholder}
                                            name={input.name}
                                            value=""
                                            class="py-3 my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                                        />
                                        <!-- Submit Inputs -->
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

<Flexdata />
