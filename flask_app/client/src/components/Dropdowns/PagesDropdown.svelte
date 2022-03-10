<script>
  import { link } from "svelte-routing";
  // library for creating dropdown menu appear on click
  import { createPopper } from "@popperjs/core";

  // core components

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
</script>

<div>
  <a
    class="lg:text-white lg:hover:text-blueGray-200 text-blueGray-700 px-3 py-4 lg:py-2 flex items-center text-xs uppercase font-bold"
    href="#pablo"
    bind:this={btnDropdownRef}
    on:click={toggleDropdown}
  >
    Navigation
  </a>
  <div
    bind:this={popoverDropdownRef}
    class="bg-white text-base z-50 float-left py-2 list-none text-left rounded shadow-lg min-w-48 {dropdownPopoverShow
      ? 'block'
      : 'hidden'}"
  >
    <a
      use:link
      href="/auth/login"
      class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    >
      Login
    </a>
    <a
      use:link
      href="/auth/register"
      class="text-sm py-2 px-4 font-normal block w-full whitespace-nowrap bg-transparent text-blueGray-700"
    >
      Register
    </a>
    <!-- <div class="h-0 mx-4 my-2 border border-solid border-blueGray-100" /> -->
  </div>
</div>
