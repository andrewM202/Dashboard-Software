<script>
    // Optional Arguments
    export let cards;
    export let id = "";
    export let title;
    export let inputs;

    function submit(e) {
        e.preventDefault();
        let data = j$("form").serialize();
        j$("form").trigger("reset");
        j$.ajax({
            type: "POST",
            url: `${location.origin}/admin/create-person`,
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
                    Create Person
                </h3>
                <form method="POST" action="/admin/create-person">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 md:gap-4">
                        <div class="mb-3 py-0 mx-4">
                            <input
                                type="text"
                                placeholder="First Name"
                                name="first_name"
                                value=""
                                class="py-3 my-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                        <div class="mb-3 py-0 mx-4">
                            <input
                                type="text"
                                placeholder="Last Name"
                                name="last_name"
                                value=""
                                class="py-3 my-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                        <div class="mb-3 py-0 mx-4">
                            <input
                                type="text"
                                placeholder="Organization"
                                name="organization"
                                value=""
                                class="py-3 my-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                        <div class="mb-3 py-0 mx-4">
                            <input
                                type="text"
                                placeholder="Title"
                                name="title"
                                value=""
                                class="py-3 my-2 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                        <div class="mb-3 py-0 mx-4">
                            <input
                                on:click={submit}
                                type="submit"
                                placeholder="test"
                                name="test"
                                value="Submit"
                                class="py-3 mx-3 my-2 cursor-pointer placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
                            />
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
