<script>
  // core components
  import TableDropdown from "components/Dropdowns/TableDropdown.svelte";
  // Popover Stuff Start
  import { createPopper } from "@popperjs/core";
  import { onMount, tick } from "svelte";

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

  class popover {
    constructor(btnRef, popoverRef) {
      this.popoverShow = false;
      this.btnRef = btnRef;
      this.popoverRef = popoverRef;
    }
    toggleTooltip() {
      if (this.popoverShow) {
        this.popoverShow = false;
      } else {
        this.popoverShow = true;
        createPopper(this.btnRef, this.popoverRef, {
          placement: "top",
          // Modifer to give padding to popover
          modifiers: [
            {
              name: "preventOverflow",
              options: {
                padding: 50,
              },
            },
          ],
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

  // On page load, svelte loads all elements for all tables
  // but they are not visible. This makes it so scrollWidth is 0
  // but innerWidth() is > 0. We need to wait until the scrollWidth is
  // not zero (when the table is clicked on and displayed) to check if it
  // should have the overflow popper applied to it
  let detectOverflowLater = [];
  onMount(() => {
    j$("nav").click(function () {
      for (let i = 0; i < detectOverflowLater.length; i++) {
        let e = j$(detectOverflowLater[i].event)[0];
        if (j$(e)[0].scrollWidth > Math.ceil(j$(e).innerWidth())) {
          // This element is now found to be overflown, remove it from
          // detectOverflowLater
          detectOverflowLater[i].remove = true;
          j$(e).append(`<div
                      style="white-space: normal; max-width: 500px; height: auto;"
                      class="bg-rose-400 hidden z-50 text-white font-semibold p-3 uppercase rounded-t-lg"
                    >
                      <span>${j$(e).text()}</span>
                    </div>`);
          let pop = new popover(e, j$(e).children("div")[0]);
          j$(e).mouseenter(function () {
            pop.toggleTooltip();
            j$(e).find("div").removeClass("hidden");
            j$(e).find("div").addClass("block");
          });
          j$(e).mouseleave(function () {
            pop.toggleTooltip();
            j$(e).find("div").addClass("hidden");
            j$(e).find("div").removeClass("block");
          });
        } else if (
          j$(e)[0].scrollWidth !== 0 &&
          j$(e)[0].scrollWidth === Math.ceil(j$(e).innerWidth())
        ) {
          // This element is not found to be overflown, remove it from
          // detectOverflowLater
          detectOverflowLater[i].remove = true;
        }
      }
      let overflowCopy = [];
      for (let i = 0; i < detectOverflowLater.length; i++) {
        if (!detectOverflowLater[i].remove) {
          overflowCopy.push(detectOverflowLater[i]);
        }
      }
      detectOverflowLater = overflowCopy;
    });
  });
  async function detectCellOverflow(e) {
    await tick();
    // Detect if a <td> is overflowing in the card table.
    // If it is, add a hover to see the entire text
    setTimeout(function () {
      if (j$(e)[0].scrollWidth === 0) {
        detectOverflowLater.push({
          event: j$(e),
          remove: false,
        });
      } else if (j$(e)[0].scrollWidth > Math.ceil(j$(e).innerWidth())) {
        j$(e).append(`<div
                      style="white-space: normal; max-width: 500px; height: auto;"
                      class="bg-rose-400 hidden z-50 text-white font-semibold p-3 uppercase rounded-t-lg"
                    >
                      <span>${j$(e).text()}</span>
                    </div>`);
        let pop = new popover(e, j$(e).children("div")[0]);
        j$(e).mouseenter(function () {
          pop.toggleTooltip();
          j$(e).find("*").removeClass("hidden");
          j$(e).find("*").addClass("block");
        });
        j$(e).mouseleave(function () {
          pop.toggleTooltip();
          j$(e).find("*").addClass("hidden");
          j$(e).find("*").removeClass("block");
        });
      }
    }, 300);
  }

  function archiveTableScrollerRight() {
    if (rangeEnd + totalRange > data.length) {
      rangeEnd = data.length;
      if (rangeEnd - totalRange < 1) {
        rangeStart = 1;
      } else {
        rangeStart = rangeEnd - totalRange + 1;
      }
    } else {
      rangeStart += totalRange;
      rangeEnd += totalRange;
    }
  }

  function archiveTableScrollerLeft() {
    if (rangeStart - totalRange < 1) {
      rangeStart = 1;
      if (rangeStart + totalRange > data.length) {
        rangeEnd = data.length;
      } else {
        rangeEnd = totalRange;
      }
    } else {
      rangeStart -= totalRange;
      rangeEnd -= totalRange;
    }
  }

  // Variable for controlling which range of documents to draw up in DOM
  let totalRange = 25;
  let rangeStart = 1;
  let rangeEnd;
  $: rangeEnd = data.length < totalRange ? data.length : totalRange; // Make reactive so it updates if we do a search
</script>

<div
  style={(tableBGColor, "height: 90%;")}
  class="flex flex-col min-w-0 break-words w-full shadow-lg rounded {color ===
  'light'
    ? 'bg-white'
    : 'bg-red-500 text-white'}"
>
  <div class="rounded-t mb-0 px-4 py-3 border-0">
    <div class="flex flex-wrap items-center">
      <div class="relative w-full max-w-full flex flex-grow flex-1">
        <!-- Icon for table indexing -->
        <div
          style="height: 1.8rem; width: 1.8rem;"
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
            {#if rowNum + 1 >= rangeStart && rowNum < rangeEnd}
              <tr
                class={rowNum % 2 === 0
                  ? tableAltColor === undefined
                    ? "bg-red-600"
                    : tableAltColor
                  : ""}
              >
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
                        use:detectCellOverflow
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
            {/if}
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>
<div
  style="height: 10%; max-height: 80px;"
  class="relative flex justify-center items-center min-w-0 break-words w-full shadow-lg bg-blueGray-600 text-white"
>
  <div
    on:click={archiveTableScrollerLeft}
    style="left: 0px; bottom: 0px;"
    class="archiveTableScroller bg-gray-600 cursor-pointer w-1/2 h-full absolute shadow"
  />
  <div
    on:click={archiveTableScrollerRight}
    style="right: 0px; bottom: 0px;"
    class="archiveTableScroller bg-gray-600 cursor-pointer w-1/2 h-full absolute shadow"
  />
  <h3>
    Results {rangeStart}-{rangeEnd} of {data.length}
  </h3>
</div>

<style>
  .archiveTableScroller:hover {
    background-color: rgb(100 116 139);
    opacity: 0.3;
  }
  td {
    max-width: 14rem;
    /* max-width: 50ch; */
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }
</style>
