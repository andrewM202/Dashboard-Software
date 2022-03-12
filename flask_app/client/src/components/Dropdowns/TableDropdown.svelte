<script>
  // library for creating dropdown menu appear on click
  import { createPopper } from "@popperjs/core";
  import { refreshData } from "../../stores.js";

  export let UpdateFormNames;
  export let DeleteID;
  export let CollectionName;
  export let inputs;
  $: DeleteID = DeleteID[0].$oid;
  $: UpdateID = DeleteID;

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

  // If we click anywhere, close the popper
  j$(document).click(function (e) {
    // If we don't click the cog icon
    if (!j$(e.target).is(j$("i.fas.fa-cog"))) {
      // If we don't click the anchor tag surrounding the icon
      if (!j$(e.target).is(j$("a#cogAnchor"))) {
        dropdownPopoverShow = false;
      }
    }
  });

  function deleteRow(e) {
    e.preventDefault();
    let data = j$("#" + DeleteID).serialize();
    j$.ajax({
      type: "POST",
      url: `${location.origin}/admin/archive-data/delete`,
      data: data,
      success: function () {
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
    let extendedChildren = j$(children).find("*");
    // Event listener for saving changes
    j$(modifyButtonContainer.children()[0]).click(function (e) {
      e.preventDefault();

      // Make AJAX Request
      j$(parent).wrap("<form id='saveForm'></form>");
      const data = j$("#saveForm").serializeArray();
      j$.ajax({
        type: "POST",
        url: `${location.origin}/admin/archive-data/update`,
        data: data,
        success: function () {
          // console.log("yay");
        },
        error: function () {
          // console.log("rip");
        },
      });
      j$(parent).unwrap();

      // Add original modify buttons back
      j$(modifyButtonContainer).children().remove();
      j$(modifyButtonContainer).append(modifyButtons);
      // Change the inputs back to regular text
      // with values from changed inputs
      let index = 0;
      for (let child of children) {
        let value = j$(child).children().val();
        j$(child).html(value);
        // Loop through extendedChildren x amount of times,
        // but don't use the extChild variable
        for (let extChild of extendedChildren) {
          if (child == extendedChildren.prevObject[index]) {
            j$(child).html(extendedChildren[index]);
            // If it has a span it is a color input
            if (j$(child).find("span").length > 0) {
              // Change the css of the span so the color matches new value
              j$(child).find("span").css({
                "background-color": value,
              });
            }
            j$(child).find("span").text(value);
            break;
          }
        }
        index++;
      }
      // Close the modify menu after all done
      j$(parent).find("i").click();
    });

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
      // console.log(j$(child).text());
      let type;
      for (let input of inputs) {
        if (input.name === UpdateFormNames[index]) {
          type = input.type;
          break;
        }
      }
      // Style input differently if it is a color input
      if (type.toLowerCase() === "color") {
        j$(child).html(
          `<input name='${UpdateFormNames[index]}'
        type="${type}"
        value='${j$(
          child
        ).text()}' class='childcell my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full'/>`
        );
      } else {
        j$(child).html(
          `<input name='${UpdateFormNames[index]}'
        type="${type}"
        value='${j$(
          child
        ).text()}' class='childcell p-2 my-2 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:shadow-outline w-full'/>`
        );
      }
      // j$(child).val(value);
      index++;
    }
    // Block invalid letters being pressed for number inputs
    // (no euler's e, +, or -)
    j$("input[type=number]").on("keydown", function (e) {
      let invalidChars = ["-", "+", "e", "E"]; //include "." if you only want integers
      if (invalidChars.includes(e.key)) {
        e.preventDefault();
      }
    });
    // If user copy and pastes invalid letter
    // into number input, remove it
    j$("input[type=number]").on("input", function () {
      this.value = this.value.replace(/[e\+\-]/gi, "");
    });
  }
</script>

<div class="flex w-full justify-center">
  <a
    class="text-white-500 py-1 px-3 cursor-pointer"
    id="cogAnchor"
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
