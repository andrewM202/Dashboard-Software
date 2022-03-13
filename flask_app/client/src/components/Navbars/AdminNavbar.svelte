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
  class="bg-red-500 block w-full z-10 bg-transparent md:flex-row md:flex-nowrap md:justify-start items-center"
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
    class="w-full mx-auto items-center flex justify-center flex-wrap md:flex-wrap py-4"
  >
    <!-- Brand -->

    {#if navItems !== undefined}
      {#each navItems as navItem, i}
        <!-- <a href="#{navItem}" class="pl-4 text-white text-sm uppercase"
          >{navItem}</a>
        > -->
        <p
          on:click={() => (openTab = i)}
          style="margin: 5px; background-color: white; color: black; padding: 10px; border-radius: 5px;"
          class="truncate nav-item cursor-pointer text-sm uppercase text-center"
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

{#if navItems.length === 1}
  <style>
  </style>
{:else if navItems.length === 2}
  <style>
    @media (min-width: 1024px) {
      p.nav-item {
        width: calc(50% - 30px) !important;
      }
    }
  </style>
{:else if navItems.length === 3}
  <style>
    @media (min-width: 1024px) {
      p.nav-item {
        width: calc(33% - 30px) !important;
      }
    }
  </style>
{:else}
  <style>
    @media (min-width: 1024px) {
      p.nav-item {
        width: calc(25% - 30px) !important;
      }
    }
  </style>
{/if}

<!-- End Navbar -->
<style>
  p.nav-item {
    width: calc(100% - 30px);
  }
</style>
