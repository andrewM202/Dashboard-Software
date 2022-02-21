<script>
    import { refreshData } from "../../stores.js";
    import Flexdata from "../Plugin/Flexdata.svelte";
    import { tick } from "svelte";

    // Optional Arguments
    export let title;
    export let inputs;
    export let flexdata;
    export let CollectionName;
    export let creationColor;

    let flexdatalist = [];

    let formID = Math.random().toString(36).substring(2, 8); // Generate random string
    let submitID = Math.random().toString(36).substring(2, 8);

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
    async function runPreJS() {
        await tick();
        if (inputs.length % 2 === 0) {
            j$(`div#rawArchiveTableContainer div#${submitID}:last-child`).css({
                width: "100%",
            });
        }
        // Run interval until flexdatalist loads,
        // and then clear interval when its loaded
        let interval = setInterval(function () {
            if (j$("ul.flexdatalist-multiple").length !== 0) {
                clearInterval(interval);
                j$("li.input-container.flexdatalist-multiple-value input").css({
                    "min-width": "150px",
                    height: "100%",
                });
                j$("li.input-container.flexdatalist-multiple-value").css({
                    height: "2rem",
                });
                j$("ul.flexdatalist-multiple").css({
                    height: "3rem",
                });
                // Make the items in flexlist have cursor pointers
                j$("ul.flexdatalist-multiple").click(function () {
                    j$(".item").css({ cursor: "pointer" });
                });
            }
        }, 10);
    }
    runPreJS();

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
                // url: `${location.origin}${url}`,
                url: `${location.origin}/admin/archive-data/create`,
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

<div style={creationColor} class="w-full h-full bg-red-500">
    <div class="flex flex-col items-center w-full">
        <h3 class="text-4xl text-center font-normal leading-normal mt-0 mb-2">
            {title}
        </h3>
        {#if error !== false}
            <div
                class="text-white w-3/4 px-6 py-4 border-0 rounded relative mb-4 bg-blueGray-700"
            >
                <span class="text-xl inline-block mr-5 align-middle">
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
    <div class="flex-auto py-5 pt-0">
        <form id={formID}>
            <input type="hidden" name="CollectionName" value={CollectionName} />
            {#if inputs !== undefined}
                <div class="flex flex-wrap" id="rawArchiveTableContainer">
                    {#each inputs as input, i}
                        <div class="w-full lg:w-6/12 py-1 px-4">
                            <div class="relative w-full mb-3">
                                <label
                                    class="w-full font-semibold text-lg text-center form-check-label inline-block text-gray-800"
                                    for={input.name}>{input.placeholder}</label
                                >
                                <!-- Flexdatalist Inputs -->
                                {#if input.flexdataid !== undefined && input.flexdatalistdata !== undefined}
                                    <input
                                        id={input.name}
                                        list={input.flexdataid}
                                        multiple
                                        type={input.type}
                                        placeholder={input.placeholder}
                                        name={input.name}
                                        value=""
                                        class="flexdatalist h-12 border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                        data-min-length="0"
                                    />
                                    <datalist id={input.flexdataid}>
                                        {#each input.flexdatalistdata as datarow}
                                            {#each Object.entries(datarow) as datapoint}
                                                {#if input.flexdatafields.includes(datapoint[0])}
                                                    <option value={datapoint[1]}
                                                        >{datapoint[1]}</option
                                                    >
                                                {/if}
                                            {/each}
                                        {/each}
                                    </datalist>
                                {:else if input.type.toLowerCase() === "color"}
                                    <input
                                        id={input.name}
                                        name={input.name}
                                        type={input.type}
                                        placeholder=""
                                        class="h-12 border-0 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                        value={input.value}
                                    />
                                    <!-- Any Input Not A Flexdatalist -->
                                {:else if input.type.toLowerCase() !== "Submit"}
                                    <input
                                        id={input.name}
                                        type={input.type}
                                        placeholder={input.placeholder}
                                        name={input.name}
                                        value=""
                                        class="h-12 border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                    />
                                {/if}
                            </div>
                        </div>
                    {/each}
                    <div class="w-full lg:w-6/12 pt-6 px-4" id={submitID}>
                        <div class="relative w-full mb-3">
                            <input
                                on:click={submit}
                                type="Submit"
                                placeholder="Submit"
                                name="SubmitButton"
                                value="Submit"
                                class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                            />
                        </div>
                    </div>
                </div>
            {/if}
        </form>
    </div>
</div>

<Flexdata />
