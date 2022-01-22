<script>
  // library for creating dropdown menu appear on click
  import { createPopper } from "@popperjs/core";
  import { refreshData } from "../../stores.js";

  export let UpdateFormNames;
  export let DeleteID;
  export let CollectionName;
  $: DeleteID = DeleteID[0].$oid;
  $: UpdateID = DeleteID[0].$oid;

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
    console.log(DeleteID);
    let data = j$("#" + DeleteID).serialize();
    j$.ajax({
      type: "POST",
      // url: `${location.origin}${DeletionURL}`,
      url: `${location.origin}/admin/archive-data/delete`,
      data: data,
      success: function () {
        // refreshData(RefreshURL);
        refreshData(`/admin/archive-data/${CollectionName}`);
      },
      error: function (e) {
        // Error Logging
        console.log(e.statusText);
        console.log(e.responseText);
      },
    });
  }

  function updateRow(e) {
    e.preventDefault();
    let modifyButtonContainer = j$(e.path[1]);
    const modifyButtons = j$(e.path[1]).children().remove();
    // Change the buttons from delete and update to save changes
    j$(e.path[1]).append(
      "<a href='' id='saveRow' class='text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700'>Save Changes</a>"
    );

    let parent = j$(e.path[4]);
    let children = j$(e.path[4]).children(".datacell");
    // let closeButton = j$(`${e.path[4]}:last-child i`);
    // Event listener for saving changes
    j$(modifyButtonContainer.children()[0]).click(function (e) {
      e.preventDefault();

      // Make AJAX Request
      j$(parent).wrap("<form id='saveForm'></form>");
      const data = j$("#saveForm").serializeArray();
      j$.ajax({
        type: "POST",
        // url: `${location.origin}${UpdateURL}`,
        url: `${location.origin}/admin/archive-data/update`,
        data: data,
        success: function () {
          console.log("yay");
        },
        error: function () {
          console.log("rip");
        },
      });
      j$(parent).unwrap();

      // Add original modify buttons back
      j$(modifyButtonContainer).children().remove();
      j$(modifyButtonContainer).append(modifyButtons);
      // Change the inputs back to regular text
      // with values from changed inputs
      for (let child of children) {
        let value = j$(child).children().val();
        j$(child).html(value);
      }
      // Close the modify menu after all done
      j$(parent).find("i").click();
    });

    // Hopefully can serialize without form element...
    // j$(e.path[4]).wrap("<form></form>");

    // Change the text to input fields
    // Append hidden input with the update id for the DB
    j$(parent).append(
      `<input type='hidden' name='UpdateID' value='${UpdateID}' />`
    );
    j$(parent).append(
      `<input type='hidden' name='CollectionName' value='${CollectionName}' />`
    );
    // Index for setting the form names from settings JSON
    let index = 0;
    for (let child of children) {
      j$(child).html(
        `<input name='${UpdateFormNames[index]}'
        value='${j$(
          child
        ).text()}' class='childcell p-2 my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full'/>`
      );
      index++;
    }
  }
</script>

<div class="flex w-full justify-center">
  <a
    class="text-white-500 py-1 px-3"
    href="#pablo"
    bind:this={btnDropdownRef}
    on:click={toggleDropdown}
  >
    <i class="fas fa-cog" />
  </a>
  <div
    id="modifyContainer"
    bind:this={popoverDropdownRef}
    class="bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48 {dropdownPopoverShow
      ? 'block'
      : 'hidden'}"
  >
    <a
      href=""
      on:click={updateRow}
      class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    >
      Update
    </a>
    <form id={DeleteID}>
      <input type="hidden" value={DeleteID} name="DeletionID" />
      <input type="hidden" value={CollectionName} name="CollectionName" />
      <input
        type="submit"
        value="Delete"
        on:click={deleteRow}
        class="text-sm cursor-pointer text-left bg-white py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
      />
    </form>
  </div>
</div>
