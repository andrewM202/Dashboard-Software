<script>
  // core components
  import TableDropdown from "components/Dropdowns/TableDropdown.svelte";

  const bootstrap = "../assets/img/bootstrap.jpg";
  const angular = "../assets/img/angular.jpg";
  const sketch = "../assets/img/sketch.jpg";
  const react = "../assets/img/react.jpg";
  const vue = "../assets/img/react.jpg";

  const team1 = "../assets/img/team-1-800x800.jpg";
  const team2 = "../assets/img/team-2-800x800.jpg";
  const team3 = "../assets/img/team-3-800x800.jpg";
  const team4 = "../assets/img/team-4-470x470.png";

  // can be one of light or dark
  export let color = "light";
  export let data;
  export let headers;
  export let title;
  export let DBFieldNames;
  export let DeletionURL;
  export let RefreshURL;
  export let UpdateURL;
  export let UpdateFormNames;
  export let Modification;

  function toggleFullscreen(e) {
    j$(e.path[6]).fullScreen(true);
  }

  setInterval(function () {
    j$("table > tbody > tr:odd").addClass("bg-red-600");
  }, 100);
</script>

<div
  class="relative flex flex-col min-w-0 break-words w-full h-full shadow-lg rounded {color ===
  'light'
    ? 'bg-white'
    : 'bg-red-500 text-white'}"
>
  <div class="rounded-t mb-0 px-4 py-3 border-0">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full px-4 max-w-full flex-grow flex-1">
        <h3
          class="font-semibold text-lg {color === 'light'
            ? 'text-blueGray-700'
            : 'text-white'}"
        >
          <i
            on:click={toggleFullscreen}
            class="fas fa-arrows-alt cursor-pointer pr-4"
          />
          {#if title !== undefined}
            {title}
          {:else}
            Card Tables
          {/if}
        </h3>
      </div>
    </div>
  </div>
  <div class="block w-full overflow-x-auto">
    <!-- Projects table -->
    <table
      class="table-fixed items-center w-full bg-transparent border-collapse"
    >
      <thead>
        <tr>
          {#if headers !== undefined}
            {#each headers as header}
              <!-- top-0 required for sticky table headers -->
              <th
                class="w-56 sticky top-0 px-6 align-middle border-solid py-3 text-s uppercase border-l border-r font-semibold text-left {color ===
                'light'
                  ? 'bg-blueGray-50 text-blueGray-500 border-blueGray-100'
                  : 'bg-rose-700 text-red-200 border-red-600'}"
              >
                {header}
              </th>
            {/each}
            {#if Modification !== false}
              <th
                class="w-28 px-6 align-middle border border-solid py-3 text-s uppercase border-l-0 border-r-0 font-semibold text-center {color ===
                'light'
                  ? 'bg-blueGray-50 text-blueGray-500 border-blueGray-100'
                  : 'bg-red-500 text-red-200 border-red-600'}">Modify</th
              >
            {/if}
          {/if}
        </tr>
      </thead>
      <tbody>
        {#if data !== undefined}
          {#each data as row}
            <tr>
              {#each Object.entries(row) as entry}
                {#if DBFieldNames.includes(entry[0])}
                  <td
                    class="datacell break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                  >
                    {entry[1]}
                  </td>
                {/if}
              {/each}
              {#if Modification !== false}
                <td
                  class="w-28 flex text-center justify-center border-t-0 align-middle border-l-0 border-r-0 text-xs p-4"
                >
                  <TableDropdown
                    {RefreshURL}
                    {DeletionURL}
                    {UpdateURL}
                    {UpdateFormNames}
                    DeleteID={Object.values(row)}
                  />
                </td>
              {/if}
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>
