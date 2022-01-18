<script>
  import { createPopper } from "@popperjs/core";
  import { tick } from "svelte";
  import Flexdata from "../Plugin/Flexdata.svelte";

  export let settings;
  export let title;
  export let postURL;

  let formID = Math.random().toString(36).substring(2, 8); // Generate random string
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
  registerToolTips();

  let z = 1;
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
            j$("ul.flexdatalist-results > li").click(function (e) {
              z++;
            });
          }
        );
      }
    }, 10);
  }

  async function styleFlexDataRegular(e) {
    // Allow duplicate values
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
      }
    }, 10);
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
    j$.ajax({
      type: "POST",
      url: `${location.origin}${postURL}`,
      data: data,
      success: function () {
        // Reset form
        j$(`#${formID}`).trigger("reset");
        // Scroll to top of window
        j$("html, body").animate({ scrollTop: "0px" }, 500);
        // Remove flexdatalist values
        j$("li.value").remove();
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
        <button
          class="bg-red-400 text-white active:bg-red-500 font-bold uppercase text-xs px-4 py-2 rounded shadow hover:shadow-md outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
          type="button"
        >
          Settings
        </button>
      </div>
    </div>
    <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
      <form method="POST" id={formID}>
        {#each settings as inputSection}
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
              <div class="w-full lg:w-6/12 px-4">
                <div class="relative w-full mb-3">
                  <label
                    class="block uppercase text-blueGray-600 text-xs font-bold mb-2"
                    for="grid-username"
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
                  {#if input.flexdatalistdisabled === true}
                    <input
                      id="grid-username"
                      name={input.name}
                      type={input.type}
                      placeholder={input.placeholder}
                      class="border-0 px-3 py-3 placeholder-blueGray-400 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
                      value={input.value}
                    />
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
                    <!-- Data imported from store -->
                  {:else if input.flexdatalistdata[0] !== undefined && typeof input.flexdatalistdata[0] !== "string"}
                    <input
                      use:styleFlexData
                      type="text"
                      placeholder=""
                      class="flexdatalist border-0 py-3 px-3 my-2 text-blueGray-600 relative bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150 w-full"
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
                      class="flexdatalist border-0 py-3 px-3 my-2 text-blueGray-600 relative bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150 w-full"
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
                        <option value="{z}. {data}">
                          <!-- {data}</option> -->
                        </option>{/each}
                    </datalist>
                  {/if}
                </div>
              </div>
            {/each}
          </div>

          <hr class="mt-6 border-b-1 border-blueGray-300" />
        {/each}
        <input
          on:click={submit}
          type="submit"
          value="Submit"
          class="py-3 mx-3 my-6 cursor-pointer text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full"
        />
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
