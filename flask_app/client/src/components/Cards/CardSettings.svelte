<script>
  import { createPopper } from "@popperjs/core";
  import { tick } from "svelte";
  import Flexdata from "../Plugin/Flexdata.svelte";
  import { refreshData } from "../../stores.js";

  export let settings;
  export let title;
  export let descButtonTitle;
  export let clearForm = true; // Should the form be cleared after post

  let formID = "archCreateForm"; // Math.random().toString(36).substring(2, 8); // Generate random string
  let error = false; // Error for if field is required

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

  async function registerToolTips() {
    await tick();
    let infos = j$(".archive-creation-info-i");
    let divs = j$(".archive-creation-info-div");
    for (let i = 0; i < infos.length; i++) {
      let pop = new popover(infos[i], divs[i]);
      j$(infos[i]).mouseenter(function () {
        pop.toggleTooltip();
        j$(divs[i]).removeClass("hidden");
        j$(divs[i]).addClass("block");
      });
      j$(infos[i]).mouseleave(function () {
        pop.toggleTooltip();
        j$(divs[i]).removeClass("block");
        j$(divs[i]).addClass("hidden");
      });
    }
  }

  $: if (settings) {
    registerToolTips();
  }

  async function styleFlexData(e) {
    // Allow duplicate values
    j$(e).flexdatalist({
      allowDuplicateValues: true,
      multiple: true,
      searchContain: true,
    });

    await tick();
    let interval = setInterval(function () {
      if (
        j$("#CardSettingsOriginParent ul.flexdatalist-multiple").length !== 0
      ) {
        clearInterval(interval);
        j$("#CardSettingsOriginParent ul.flexdatalist-multiple").css({
          "border-width": "0",
        });
        j$("#CardSettingsOriginParent ul.flexdatalist-multiple").click(
          function () {
            j$(".item").css({ cursor: "pointer" });
          }
        );
        j$("li.input-container.flexdatalist-multiple-value").focus(function () {
          j$(".item").css({ cursor: "pointer" });
        });
        j$("li.input-container.flexdatalist-multiple-value").css({
          "min-height": "2rem",
        });
        j$("li.input-container.flexdatalist-multiple-value input").css({
          "min-height": "2.2rem",
        });
        j$("ul.flexdatalist-multiple").css({
          "min-height": "3rem",
        });
        // If we tab into a flex input make the items have a cursor pointer
        j$(document).keydown(function (event) {
          if (event.keyCode === 9) {
            // We just tabbed. Set a timeout for 250 milliseconds
            // and then add the cursor property
            setTimeout(function () {
              j$(".item").css({ cursor: "pointer" });
            }, 250);
          }
        });
      }
    }, 10);
  }

  // Have it recalculate numbers on any document change, so if you
  // press enter when focused on form it still runs
  let currentDraggedElem;
  j$(document).on("change", function () {
    let lists = j$("ul.flexdatalist-multiple");
    for (let list of lists) {
      let count = 0;
      j$(list)
        .find("li.value span.text")
        .each(function () {
          let currentText = j$(this).text();
          count++;
          if (j$(this).attr("Numbered") !== "true") {
            j$(this).text(`${count}. ${currentText}`);
            j$(this).attr("Numbered", "true");
          } else {
            // Renumber if it its already numbered, without duplications
            let baseText = j$(this)
              .text()
              .substring(
                j$(this).text().indexOf(" ") + 1,
                j$(this).text().length
              );
            j$(this).text(`${count}. ${baseText}`);
          }
        });

      j$(list)
        .find("li.value")
        .each(function () {
          let currElemEvents = j$._data(this, "events");
          // console.log(currElemEvents);
          // Make each of the values in the inputs draggable
          j$(this).attr("draggable", true);
          // Give the inputs a grab css
          j$(this).css("cursor", "grab");
          // Create event listeners
          // If this element does not already have the events
          if (currElemEvents.drag === undefined) {
            j$(this).on("drag", function (e) {
              if (j$(this) !== undefined) currentDraggedElem = j$(this);
            });
          }
          if (currElemEvents.dragover === undefined) {
            j$(this).on("dragover", function (e) {
              e.preventDefault();
              // If we are dragging over li.value
              if (
                j$(e.currentTarget).attr("class") === "value" &&
                j$(e.currentTarget).is("li")
              ) {
                // If that li.value is a different element from the
                // one being dragged
                if (!j$(e.currentTarget).is(j$(this))) {
                  e.dataTransfer.dropEffect = "copy";
                }
              }
            });
          }

          if (currElemEvents.drop === undefined) {
            j$(this).on("drop", function (e) {
              e.preventDefault();
              e.stopPropagation();
              console.log("Dropped");
              // console.log(e.originalEvent.path); // The path of the element that was dropped on
              // console.log(j$(e.currentTarget)); // The element the draggable was dropped on
              // console.log(currentDraggedElem); // The element that was dragged
              // Get the parent UL element
              let ulContainer;
              let parent;
              for (let elem of e.originalEvent.path) {
                let attr = j$(elem).attr("class");
                if (attr !== undefined) {
                  if (
                    attr.indexOf("flexdatalist-multiple") !== -1 &&
                    j$(elem).is("ul")
                  ) {
                    parent = elem;
                  }
                }
              }
              // Only if the LIs are the same should we switch. Basically,
              // both values have to be from the same flexdatalist input
              if (j$(parent).is(j$(currentDraggedElem.parent("ul")))) {
                let pc = parent.children;
                // Find the index of the currentDraggedElem
                // to see if its before or after the element dropped on
                let draggedIndex;
                for (let j = 0; j < parent.children.length; j++) {
                  if (j$(pc[j]).is(j$(currentDraggedElem))) {
                    draggedIndex = j;
                    break;
                  }
                }
                for (let i = 0; i < parent.children.length; i++) {
                  if (j$(pc[i]).is(j$(e.currentTarget))) {
                    // Put the dragged element right in front of it
                    // or behind it depending on the draggedIndex
                    if (i > draggedIndex) {
                      j$(currentDraggedElem).insertAfter(parent.children[i]);
                    } else {
                      j$(currentDraggedElem).insertBefore(parent.children[i]);
                    }

                    // Set the value of the input again now that it is re-ordered
                    let stringValues = "";
                    for (let child of parent.children) {
                      if (j$(child).is("li")) {
                        let nodeClass = j$(child).attr("class");
                        if (nodeClass === "value") {
                          // console.log(j$(child).text());
                          let baseText = j$(child)
                            .text()
                            .substring(
                              j$(child).text().indexOf(" ") + 1,
                              j$(child).text().length
                            );
                          baseText = baseText.substring(0, baseText.length - 1);
                          stringValues += "," + baseText;
                        }
                      }
                    }
                    // This gets rid of initial ,
                    stringValues = stringValues.substring(
                      1,
                      stringValues.length
                    );

                    // We have to find the input now
                    // and set it's value to stringValues
                    j$(parent).siblings("input").val(stringValues);

                    // Renumber all of the elements start
                    let count = 0;
                    j$(list)
                      .find("li.value span.text")
                      .each(function () {
                        let currentText = j$(this).text();
                        count++;
                        if (j$(this).attr("Numbered") !== "true") {
                          j$(this).text(`${count}. ${currentText}`);
                          j$(this).attr("Numbered", "true");
                        } else {
                          // Renumber if it its already numbered, without duplications
                          let baseText = j$(this)
                            .text()
                            .substring(
                              j$(this).text().indexOf(" ") + 1,
                              j$(this).text().length
                            );
                          j$(this).text(`${count}. ${baseText}`);
                        }
                      });
                    // Renumber all of the elements end
                    break; // End the for loop early since work is done
                  }
                }
              }
            });
          }
        });
    }
  });

  async function styleFlexDataRegular(e) {
    j$(e).flexdatalist({ noResultsText: "" });

    await tick();
    let interval = setInterval(function () {
      if (
        j$("#CardSettingsOriginParent ul.flexdatalist-multiple").length !== 0
      ) {
        clearInterval(interval);
        j$("#CardSettingsOriginParent ul.flexdatalist-multiple").css({
          "border-width": "0",
        });
        j$("li.input-container.flexdatalist-multiple-value").css({
          "min-height": "2rem",
        });
        j$("li.input-container.flexdatalist-multiple-value input").css({
          "min-height": "2.2rem",
        });
        j$("ul.flexdatalist-multiple").css({
          "min-height": "3rem",
        });
      }
      j$(".flexDataRegular").click(function () {
        j$(".item").css({ cursor: "pointer" });
      });
      // If we tab into a flex input make the items have a cursor pointer
      j$(document).keydown(function (event) {
        if (event.keyCode === 9) {
          // We just tabbed. Set a timeout for 250 milliseconds
          // and then add the cursor property
          setTimeout(function () {
            j$(".item").css({ cursor: "pointer" });
          }, 250);
        }
      });
    }, 10);
  }

  function submit(e) {
    e.preventDefault();
    let postURL = e.srcElement.attributes.posturl.nodeValue;
    let data = new FormData(j$(`#${formID}`)[0]);
    j$.ajax({
      type: "POST",
      url: `${location.origin}${postURL}`,
      data: data,
      mimeType: "multipart/form-data",
      contentType: false,
      processData: false,
      success: function () {
        // Reset form
        if (clearForm) j$(`#${formID}`).trigger("reset");
        // Scroll to top of window
        j$("html, body").animate({ scrollTop: "0px" }, 500);
        // Remove flexdatalist values
        j$("li.value").remove();
        refreshData();
      },
      error: function (e) {
        // Error logging
        console.log(e.statusText);
        console.log(e.responseText);
        // Scroll to top of window
        j$("html, body").animate({ scrollTop: "0px" }, 500);
      },
    });
  }

  // A function to change the value of
  // a checkbox when it is clicked,
  // from on or off
  function changeCheckboxValue(e) {
    let checkboxValue = j$(e.path[0]).val();
    // Toggle value from on or off
    checkboxValue === "off"
      ? j$(e.path[0]).val("on")
      : j$(e.path[0]).val("off");
    // Update checkboxValue since we just changed it
    checkboxValue = j$(e.path[0]).val();
    // Add the "checked" attribute if its value is on
    checkboxValue === "off"
      ? j$(e.path[0]).removeAttr("checked")
      : j$(e.path[0]).attr("checked", "");
  }

  function setCheckboxState(e) {
    let checkboxValue = j$(e).val();
    // If checkboxValue is is on add checked attribute
    checkboxValue === "on" ? j$(e).attr("checked", "") : "";
  }

  let showModal = false;

  function toggleModal(e) {
    e.preventDefault();
    showModal = !showModal;
  }
</script>

{#if settings !== undefined}
  <!-- Header Start -->
  <div
    id="CardSettingsOriginParent"
    class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
  >
    <div class="rounded-t bg-white mb-0 px-6 py-6">
      <div class="text-center flex justify-between">
        <h6 class="text-blueGray-700 text-xl font-bold">
          {title !== undefined ? title : "My Account"}
        </h6>
        {#if descButtonTitle !== undefined}
          <button
            class="bg-red-400 text-white active:bg-red-500 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
            type="button"
          >
            {descButtonTitle}
          </button>
        {/if}
      </div>
    </div>
    <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
      <form method="POST" id={formID}>
        {#each settings as inputSection, i}
          <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
            <!-- Tooltip Start -->
            {#if inputSection.SubtitlePopoverMessage !== undefined}
              <i
                class="archive-creation-info-i fas fa-info-circle cursor-pointer pl-12"
              />
              <div
                class="hidden archive-creation-info-div bg-orange-500 border-0 block z-50 font-normal leading-normal text-sm max-w-xs text-left no-underline break-words rounded-lg"
              >
                <div>
                  <div
                    class="bg-rose-400 text-white opacity-75 font-semibold p-3 uppercase rounded-t-lg"
                  >
                    {inputSection.SubtitlePopoverMessage}
                  </div>
                </div>
              </div>
            {/if}
            <!-- Tooltip End -->
            {inputSection.Subtitle}
          </h6>
          <div class="flex flex-wrap">
            {#each inputSection.Inputs as input}
              <!-- If input is a submit or textarea make it full 
                width else only partial width -->
              <div
                class="{input.type !== 'submit' && input.type !== 'textarea'
                  ? 'lg:w-6/12 px-4'
                  : ''} {input.type === 'textarea' ? 'px-4' : ''} w-full"
              >
                <div class="relative w-full mb-3">
                  <label
                    class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    for=""
                  >
                    <!-- Tooltip Start -->
                    {#if input.popoverMessage !== undefined}
                      <i
                        class="archive-creation-info-i fas fa-info-circle cursor-pointer pl-12"
                      />
                      <div
                        class="hidden archive-creation-info-div bg-orange-500 border-0 block z-50 font-normal leading-normal text-sm max-w-xs text-left no-underline break-words rounded-lg"
                      >
                        <div>
                          <div
                            class="bg-rose-400 text-white opacity-75 font-semibold p-3 uppercase rounded-t-lg"
                          >
                            {input.popoverMessage}
                          </div>
                        </div>
                      </div>
                    {/if}
                    <!-- Tooltip End -->
                    {input.placeholder}
                  </label>

                  {#if input.type === "color"}
                    <input
                      id="grid-username"
                      name={input.name}
                      type={input.type}
                      placeholder=""
                      class="border-0 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      value={input.value}
                    />
                  {:else if input.type === "checkbox"}
                    <input
                      class="form-check-input appearance-none w-9 -ml-10 rounded-full float-left h-5 align-top bg-white bg-no-repeat bg-contain bg-gray-300 focus:outline-none cursor-pointer shadow-sm"
                      type="checkbox"
                      role="switch"
                      name={input.name}
                      id="flexSwitchCheckDefault"
                      value={input.value}
                      on:click={changeCheckboxValue}
                      use:setCheckboxState
                    />
                    <label
                      class="form-check-label inline-block text-gray-800"
                      for="flexSwitchCheckDefault">{input.placeholder}</label
                    >
                    <!-- Any regular input with the flexdatalist disabled -->
                  {:else if input.type === "textarea"}
                    {#if input.readonly === true}
                      <textarea
                        class="border-0 min-h-250 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        name={input.name}
                        value={input.value}
                        placeholder={input.placeholder}
                        readonly
                      />
                    {:else}
                      <textarea
                        class="border-0 min-h-250 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        name={input.name}
                        value={input.value}
                        placeholder={input.placeholder}
                      />
                    {/if}
                  {:else if input.type === "button"}
                    <input
                      id="grid-username"
                      name={input.name}
                      type={input.type}
                      placeholder={input.placeholder}
                      class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      value={input.value}
                      on:click={input.submitFunction !== undefined
                        ? input.submitFunction
                        : submit}
                    />
                  {:else if input.flexdatalistdisabled === true}
                    <input
                      id="grid-username"
                      name={input.name}
                      type={input.type}
                      placeholder={input.placeholder}
                      class="border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      value={input.value}
                    />
                    <!-- Any submit input -->
                  {:else if input.type === "submit"}
                    {#if input.confirmationRequired === true}
                      <!-- If this button should have a modal -->
                      <button
                        class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        on:click={toggleModal}>{input.value}</button
                      >
                      {#if showModal}
                        <div
                          style="margin: 0;
                          left: 50%;
                          bottom: 25%;
                          -ms-transform: translate(-50%, -50%);
                          transform: translate(-50%, -50%);"
                          class="overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex"
                        >
                          <div class="relative w-auto my-6  max-w-sm">
                            <!--content-->
                            <div
                              class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none"
                            >
                              <!--header-->
                              <div
                                class="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t"
                              >
                                <h3 class="text-3xl font-semibold">Deletion</h3>
                                <button
                                  class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                                  on:click={toggleModal}
                                >
                                  <span
                                    class="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none"
                                  >
                                    ×
                                  </span>
                                </button>
                              </div>
                              <!--footer-->
                              <div
                                class="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b"
                              >
                                <button
                                  class="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                                  type="button"
                                  on:click={toggleModal}
                                >
                                  Close
                                </button>
                                <button
                                  class="bg-emerald-500 text-white active:bg-emerald-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                                  type="button"
                                  on:click={submit}
                                  on:click={toggleModal}
                                  postURL={input.postURL}
                                >
                                  Confirm delete
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="opacity-25 fixed inset-0 z-40 bg-black" />
                      {/if}
                    {:else}
                      <input
                        id="grid-username"
                        postURL={input.postURL}
                        on:click={input.submitFunction !== undefined
                          ? input.submitFunction
                          : submit}
                        name={input.name}
                        type={input.type}
                        placeholder={input.placeholder}
                        class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                        value={input.value}
                      />
                    {/if}
                    <!-- Generic flexlist with no predefined values -->
                  {:else if input.flexdatalistdata === undefined}
                    <input
                      use:styleFlexDataRegular
                      id="grid-username"
                      placeholder="....."
                      name={input.name}
                      type={input.type}
                      class="flexdatalist border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      value={input.value}
                      list="flexList"
                      data-min-length="0"
                      multiple="multiple"
                    />
                    <datalist id="flexList" />
                  {:else if input.flexdatalistdata[0] !== undefined && input.flexdatalistsingle && typeof input.flexdatalistdata[0] === "string"}
                    <input
                      use:styleFlexDataRegular
                      type="text"
                      placeholder=""
                      class="flexdatalist flexDataRegular border-0 py-3 px-3 text-blueGray-600 relative bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150 w-full"
                      data-min-length="0"
                      list={input.flexdataid}
                      name={input.name}
                    />
                    <datalist id={input.flexdataid}>
                      {#if input.flexdatanonedata}
                        <option value="None">None</option>
                      {/if}
                      {#each input.flexdatalistdata as data}
                        <option value={data} />
                      {/each}
                    </datalist>
                    <!-- Data imported from store -->
                  {:else if input.flexdatalistdata[0] !== undefined && typeof input.flexdatalistdata[0] !== "string"}
                    <input
                      use:styleFlexData
                      type="text"
                      placeholder=""
                      class="flexdatalist border-0 py-3 px-3 text-blueGray-600 relative bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150 w-full"
                      data-min-length="0"
                      multiple="multiple"
                      list={input.flexdataid}
                      name={input.name}
                    />
                    <datalist id={input.flexdataid}>
                      {#if input.flexdatanonedata}
                        <option value="None">None</option>
                      {/if}
                      {#each input.flexdatalistdata as datarow}
                        {#each Object.entries(datarow) as datapoint}
                          {#if datapoint[0] !== "_id"}
                            <option value={datapoint[1]}>{datapoint[1]}</option>
                          {/if}
                        {/each}
                      {/each}
                    </datalist>
                    <!-- Values loaded for flexlist from array of strings -->
                  {:else}
                    <input
                      use:styleFlexData
                      type="text"
                      placeholder=""
                      class="flexdatalist border-0 py-3 px-3 text-blueGray-600 relative bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150 w-full"
                      data-min-length="0"
                      multiple="multiple"
                      list={input.flexdataid}
                      name={input.name}
                    />
                    <datalist id={input.flexdataid}>
                      {#if input.flexdatanonedata}
                        <option value="None">None</option>
                      {/if}
                      {#each input.flexdatalistdata as data}
                        <!-- <option value="{z}. {data}"> -->
                        <option value={data}>
                          <!-- {data}</option> -->
                        </option>{/each}
                    </datalist>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
          <!-- Add hr if this is not last input section -->
          {#if i !== settings.length - 1}
            <hr class="mt-6 border-b-1 border-blueGray-300" />
          {/if}
        {/each}
      </form>
    </div>
  </div>
  <!-- Inputs End -->
{:else}
  <div
    class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-100 border-0"
  >
    <div class="rounded-t bg-white mb-0 px-6 py-6">
      <div class="text-center flex justify-between">
        <h6 class="text-blueGray-700 text-xl font-bold">My account</h6>
        <button
          class="bg-red-400 text-white active:bg-red-500 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
          type="button"
        >
          Settings
        </button>
      </div>
    </div>
    <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
      <form>
        <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
          User Information
        </h6>
        <div class="flex flex-wrap">
          <div class="w-full lg:w-6/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-username"
              >
                Username
              </label>
              <input
                id="grid-username"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="lucky.jesse"
              />
            </div>
          </div>
          <div class="w-full lg:w-6/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-email"
              >
                Email address
              </label>
              <input
                id="grid-email"
                type="email"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="jesse@example.com"
              />
            </div>
          </div>
          <div class="w-full lg:w-6/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-first-name"
              >
                First Name
              </label>
              <input
                id="grid-first-name"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="Lucky"
              />
            </div>
          </div>
          <div class="w-full lg:w-6/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-last-name"
              >
                Last Name
              </label>
              <input
                id="grid-last-name"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="Jesse"
              />
            </div>
          </div>
        </div>

        <hr class="mt-6 border-b-1 border-blueGray-300" />

        <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
          Contact Information
        </h6>
        <div class="flex flex-wrap">
          <div class="w-full lg:w-12/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-address"
              >
                Address
              </label>
              <input
                id="grid-address"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09"
              />
            </div>
          </div>
          <div class="w-full lg:w-4/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-city"
              >
                City
              </label>
              <input
                id="grid-city"
                type="email"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="New York"
              />
            </div>
          </div>
          <div class="w-full lg:w-4/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-country"
              >
                Country
              </label>
              <input
                id="grid-country"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="United States"
              />
            </div>
          </div>
          <div class="w-full lg:w-4/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-postal-code"
              >
                Postal Code
              </label>
              <input
                id="grid-postal-code"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                value="Postal Code"
              />
            </div>
          </div>
        </div>

        <hr class="mt-6 border-b-1 border-blueGray-300" />

        <h6 class="text-blueGray-400 text-sm mt-3 mb-6 font-bold uppercase">
          About Me
        </h6>
        <div class="flex flex-wrap">
          <div class="w-full lg:w-12/12 px-4">
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                for="grid-about-me"
              >
                About me
              </label>
              <textarea
                id="grid-about-me"
                type="text"
                class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                rows="4"
                value="A beautiful UI Kit and Admin for Svelte & Tailwind CSS. It is Free
                and Open Source."
              />
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
{/if}

<Flexdata />
