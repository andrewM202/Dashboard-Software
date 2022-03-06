<script>
  // core components
  import TableDropdown from "components/Dropdowns/TableDropdown.svelte";
  // Popover Stuff Start
  import { createPopper } from "@popperjs/core";
  import { tick } from "svelte";

  let popoverShow = false;
  let btnRef;
  let popoverRef;

  let btnRef2;
  let popoverRef2;
  let popoverShow2 = false;

  function toggleTooltip(btnref, popref, popShow) {
    if (popShow === "popoverShow" && popoverShow === true) {
      popoverShow = false;
    } else if (popShow === "popoverShow2" && popoverShow2 === true) {
      popoverShow2 = false;
    } else {
      if (popShow === "popoverShow") {
        popoverShow = true;
        createPopper(btnRef, popoverRef, {
          placement: "left",
        });
      } else if (popShow === "popoverShow2") {
        popoverShow2 = true;
        createPopper(btnRef2, popoverRef2, {
          placement: "left",
        });
      }
    }
  }
  // Popover Stuff End

  // can be one of light or dark
  export let color = "dark";
  export let data;
  export let headers;
  export let title;
  export let DBFieldNames;
  export let RefreshURL;
  export let UpdateURL;
  export let Modification;
  export let CollectionName;
  export let tableBGColor;
  export let tableHeaderColor;
  export let tableAltColor;
  export let inputs;

  function toggleFullscreen(e) {
    j$(e.path[6]).fullScreen(true);
  }

  let tableIndexing = true;
  function toggleTableIndexing(e) {
    tableIndexing = tableIndexing === true ? false : true;
  }

  // Reactive so it recolors the rows whenever
  // data is changed
  $: if (data) {
    async function makeOddRowsRed() {
      await tick();
      if (tableAltColor !== undefined) {
        j$("table > tbody > tr").css("background-color", undefined);
        j$("table > tbody > tr:even").css("background-color", tableAltColor);
      } else {
        j$("table > tbody > tr").removeClass("bg-red-600");
        j$("table > tbody > tr:even").addClass("bg-red-600");
      }
    }
    makeOddRowsRed();
  }

  function downloadData() {
    const name = `${CollectionName}.json`;
    const saveData = JSON.stringify(data, undefined, 2);

    const a = document.createElement("a");
    const type = name.split(".").pop();
    a.href = URL.createObjectURL(
      new Blob([saveData], {
        // type: `text/${type === "txt" ? "plain" : type}`,
        type: "json",
      })
    );
    a.download = name;
    a.click();
  }
</script>

<div
  style={tableBGColor}
  class="relative flex flex-col min-w-0 break-words w-full h-full shadow-lg rounded {color ===
  'light'
    ? 'bg-white'
    : 'bg-red-500 text-white'}"
>
  <div class="rounded-t mb-0 px-4 py-3 border-0">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full max-w-full flex flex-grow flex-1">
        <!-- Icon for table indexing -->
        <div
          on:click={toggleTableIndexing}
          class="{tableIndexing === true
            ? 'bg-rose-400'
            : 'bg-black'} cursor-pointer rounded-full px-2 mr-4"
        >
          <i class="fas fa-sort-numeric-down" />
        </div>
        <h3
          class="font-semibold text-lg w-full {color === 'light'
            ? 'text-blueGray-700'
            : 'text-white'}"
        >
          <i
            on:click={toggleFullscreen}
            bind:this={btnRef}
            on:mouseenter={toggleTooltip(btnRef, popoverRef, "popoverShow")}
            on:mouseleave={toggleTooltip(btnRef, popoverRef, "popoverShow")}
            class="fas fa-arrows-alt cursor-pointer pr-4"
          />
          <!-- Tooltip Start -->
          <div
            bind:this={popoverRef}
            class="bg-orange-500 border-0 block z-50 font-normal leading-normal text-sm max-w-xs text-left no-underline break-words rounded-lg {popoverShow
              ? 'block'
              : 'hidden'}"
          >
            <div>
              <div
                class="bg-rose-400 text-white opacity-75 font-semibold p-3 uppercase rounded-t-lg"
              >
                Click For Fullscreen
              </div>
            </div>
          </div>
          <!-- Tooltip End -->
          {#if title !== undefined}
            {title}
          {:else}
            Card Tables
          {/if}
        </h3>
        <h3
          class="font-semibold text-lg text-right w-full {color === 'light'
            ? 'text-blueGray-700'
            : 'text-white'}"
        >
          <i
            on:click={downloadData}
            bind:this={btnRef2}
            on:mouseenter={toggleTooltip(btnRef2, popoverRef2, "popoverShow2")}
            on:mouseleave={toggleTooltip(btnRef2, popoverRef2, "popoverShow2")}
            class="fas fa-download self-end cursor-pointer "
          />
          <!-- Tooltip Start -->
          <div
            bind:this={popoverRef2}
            class="bg-orange-500 border-0 block z-50 font-normal leading-normal text-sm max-w-xs text-left no-underline break-words rounded-lg {popoverShow2
              ? 'block'
              : 'hidden'}"
          >
            <div>
              <div
                class="bg-rose-400 text-white opacity-75 font-semibold p-3 uppercase rounded-t-lg"
              >
                Click To Download Data (JSON)
              </div>
            </div>
          </div>
        </h3>
      </div>
    </div>
  </div>
  <div class="block w-full overflow-x-auto">
    <!-- Projects table -->
    <table class="items-center w-full bg-transparent border-collapse">
      <thead>
        <tr>
          {#if headers !== undefined}
            {#if tableIndexing === true}
              <th
                style={tableHeaderColor}
                class="w-16 text-center sticky top-0 px-6 align-middle border-solid py-3 text-s uppercase border-l border-r font-semibold text-left {color ===
                'light'
                  ? 'bg-blueGray-50 text-blueGray-500 border-blueGray-100'
                  : 'bg-rose-700 text-red-200 border-red-600'}"
              >
                Index
              </th>
            {/if}
            {#each headers as header}
              <!-- top-0 required for sticky table headers -->
              <th
                style={tableHeaderColor}
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
                style={tableHeaderColor}
                class="w-28 sticky top-0 px-6 align-middle order-solid py-3 text-s uppercase border-l border-r font-semibold text-center {color ===
                'light'
                  ? 'bg-blueGray-50 text-blueGray-500 border-blueGray-100'
                  : 'bg-rose-700 text-red-200 border-red-600'}">Modify</th
              >
            {/if}
          {/if}
        </tr>
      </thead>
      <tbody>
        {#if data !== undefined}
          {#each data as row, rowNum}
            <tr>
              {#if tableIndexing === true}
                <!-- <td
                  class="w-full flex text-center justify-center border-t-0 align-middle border-l-0 border-r-0 text-s p-4"
                > -->
                <td
                  class="break-words w-16 text-center border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                >
                  {rowNum + 1}
                </td>
              {/if}
              {#each Object.entries(row) as entry, i}
                {#if DBFieldNames.includes(entry[0])}
                  <!-- If this is a color input style it differently -->
                  {#if headers[i - 1] === "Color"}
                    <td
                      class="datacell break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                    >
                      <span
                        class="p-3 px-12"
                        style="background-color: {entry[1]}; border-radius: 16px;"
                        >{entry[1]}</span
                      >
                    </td>
                  {:else}
                    <td
                      class="datacell break-words w-56 border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                    >
                      {entry[1]}
                    </td>
                  {/if}
                {/if}
              {/each}
              {#if Modification !== false}
                <!-- <td
                  class="w-full flex text-center justify-center border-t-0 align-middle border-l-0 border-r-0 text-xs p-4"
                > -->
                <td
                  class="break-words w-16 text-center border-t-0 px-6 align-middle border-l-0 border-r-0 text-s p-4"
                >
                  <TableDropdown
                    {RefreshURL}
                    {UpdateURL}
                    UpdateFormNames={DBFieldNames}
                    {CollectionName}
                    DeleteID={Object.values(row)}
                    {inputs}
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
