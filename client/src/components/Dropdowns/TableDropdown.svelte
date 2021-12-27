<script>
  // library for creating dropdown menu appear on click
  import { createPopper } from "@popperjs/core";

  import {
    peopleStore,
    organizationsStore,
    getDBResource,
  } from "../../stores.js";

  export let DeletionURL;
  export let RefreshURL;
  export let DeleteID;
  DeleteID = DeleteID[0].$oid;

  let dropdownPopoverShow = false;

  let btnDropdownRef;
  let popoverDropdownRef;

  const toggleDropdown = (event) => {
    event.preventDefault();
    if (dropdownPopoverShow) {
      dropdownPopoverShow = false;
    } else {
      dropdownPopoverShow = true;
      createPopper(btnDropdownRef, popoverDropdownRef, {
        placement: "bottom-start",
      });
    }
  };

  function deleteRow(e) {
    e.preventDefault();
    let data = j$("#" + DeleteID).serialize();
    j$.ajax({
      type: "POST",
      url: `${location.origin}${DeletionURL}`,
      data: data,
      success: function () {},
      error: function (e) {
        // Error Logging
        console.log(e.statusText);
        console.log(e.responseText);
      },
    });
  }
</script>

<div>
  <a
    class="text-white-500 py-1 px-3"
    href="#pablo"
    bind:this={btnDropdownRef}
    on:click={toggleDropdown}
  >
    <i class="fas fa-ellipsis-v" />
  </a>
  <div
    bind:this={popoverDropdownRef}
    class="bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48 {dropdownPopoverShow
      ? 'block'
      : 'hidden'}"
  >
    <a
      href=""
      on:click={(e) => e.preventDefault()}
      class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    >
      Update
    </a>
    <form id={DeleteID}>
      <input type="hidden" value={DeleteID} name="DeletionID" />
      <input
        type="submit"
        value="Delete"
        on:click={deleteRow}
        class="text-sm cursor-pointer text-left bg-white py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
      />
    </form>
  </div>
</div>
