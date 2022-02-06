<script>
  // core components
  export let navItems;
  export let openTab;
  export let title;
  export let navBarBGColor;
</script>

<!-- Navbar -->
<nav
  style={navBarBGColor}
  class="absolute bg-red-500 top-0 left-0 w-full z-10 bg-transparent md:flex-row md:flex-nowrap md:justify-start flex items-center p-4"
>
  {#if title !== undefined}
    <div class="md:block hidden md:pr-10 px-4 w-40">
      <a
        class="text-white min-w-full text-sm uppercase align-self-start hidden lg:inline-block font-semibold"
        href="#pablo"
        on:click={(e) => e.preventDefault()}
      >
        {title}
      </a>
    </div>
  {/if}
  <div
    class="w-full mx-autp items-center flex justify-around flex-wrap md:flex-wrap md:px-10 px-4"
  >
    <!-- Brand -->

    {#if navItems !== undefined}
      {#each navItems as navItem, i}
        <!-- <a href="#{navItem}" class="pl-4 text-white text-sm uppercase"
          >{navItem}</a>
        > -->
        <p
          on:click={() => (openTab = i)}
          class="cursor-pointer pl-4 text-white text-sm uppercase"
        >
          {navItem}
        </p>
      {/each}
    {/if}
    <!-- Form -->
    <!-- <form
      class="md:flex hidden flex-row flex-wrap items-center lg:ml-auto mr-3"
    >
      <div class="relative flex w-full flex-wrap items-stretch">
        <span
          class="z-10 h-full leading-snug font-normal absolute text-center text-blueGray-300 absolute bg-transparent rounded text-base items-center justify-center w-8 pl-3 py-3"
        >
          <i class="fas fa-search" />
        </span>
        <input
          type="text"
          placeholder="Search here..."
          class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm shadow outline-none focus:outline-none focus:ring w-full pl-10"
        />
      </div>
    </form> -->
  </div>
</nav>
<!-- End Navbar -->
