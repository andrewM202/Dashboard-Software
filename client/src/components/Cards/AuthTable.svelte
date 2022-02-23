<script>
    import { each } from "svelte/internal";

    export let data;
    export let tableHeaders = [];
    export let approveFunction;
    export let denyFunction;
    export let DBFieldNames;
    export let roles;
    export let use;
    export let title;
</script>

<div
    class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
>
    <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
        <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
            {title}
        </h6>
        <div class="flex flex-wrap">
            <div class="w-full px-4">
                <div class="relative w-full mb-3">
                    <table
                        class="table-fixed items-center w-full bg-transparent border-collapse"
                    >
                        <thead>
                            <tr>
                                {#each tableHeaders as tableHead}
                                    <th
                                        class="w-1/3 sticky top-0 px-6 align-middle border-solid py-3 text-s uppercase border-l border-r font-semibold text-left bg-white text-blueGray-500 border-blueGray-100"
                                        >{tableHead}</th
                                    >
                                {/each}
                            </tr>
                        </thead>
                        <tbody>
                            {#if use === "approval"}
                                {#each data as row}
                                    <tr>
                                        {#each Object.entries(row) as entry}
                                            {#if DBFieldNames.includes(entry[0])}
                                                <td
                                                    class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                                    >{entry[1]}</td
                                                >
                                                <input
                                                    type="hidden"
                                                    name="username"
                                                    value={entry[1]}
                                                />
                                            {/if}
                                        {/each}
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <select class="w-full" name="role">
                                                {#each roles as role}
                                                    <option value={role}
                                                        >{role}</option
                                                    >
                                                {/each}
                                            </select>
                                        </td>
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <input
                                                class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                                type="submit"
                                                value="Approve"
                                                on:click={approveFunction}
                                            />
                                        </td>
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <input
                                                class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                                type="submit"
                                                value="Deny"
                                                on:click={denyFunction}
                                            />
                                        </td>
                                    </tr>
                                {/each}
                            {:else if use === "user-updating"}
                                {#each data as row}
                                    <tr>
                                        <input
                                            type="hidden"
                                            name="id"
                                            value={row.id}
                                        />
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <input
                                                type="text"
                                                placeholder="Username"
                                                name="username"
                                                value={row.username}
                                                class="h-12 border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                            />
                                        </td>
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <select class="w-full" name="role">
                                                {#each row.roles as role}
                                                    <option value={role}
                                                        >{role}</option
                                                    >
                                                {/each}
                                                {#each roles as role}
                                                    {#if row.roles.includes(role) !== true}
                                                        <option value={role}
                                                            >{role}</option
                                                        >
                                                    {/if}
                                                {/each}
                                            </select>
                                        </td>
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <input
                                                class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                                type="submit"
                                                value="Delete Account"
                                                on:click={denyFunction}
                                            />
                                        </td>
                                        <td
                                            class="break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                                        >
                                            <input
                                                class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                                                type="submit"
                                                value="Save User Changes"
                                                on:click={approveFunction}
                                            />
                                        </td>
                                    </tr>
                                {/each}
                            {/if}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
