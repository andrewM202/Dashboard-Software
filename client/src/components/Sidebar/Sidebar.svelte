<script>
  import { link } from "svelte-routing";

  // core components
  import NotificationDropdown from "components/Dropdowns/NotificationDropdown.svelte";
  import UserDropdown from "components/Dropdowns/UserDropdown.svelte";

  let collapseShow = "hidden";

  function toggleCollapseShow(classes) {
    collapseShow = classes;
  }

  let navBarCollapseShow = true;
  function closeSideBar(e) {
    if (navBarCollapseShow) {
      // Hide side bar
      j$("#SideBarNav").toggle();
      // Make main content whole width
      j$("#AdminMainContentContainer").css({
        position: "absolute",
        right: "0",
        width: "100vw",
      });
      j$("#AdminMainContentContainer").addClass("bg-blueGray-100");
      j$("#AdminMainContentContainer").prepend(j$("#ReOpenSideBarIcon"));
      j$("#ReOpenSideBarIcon").toggle();
      // Make second button visible
      j$("#ReOpenSideBarIcon").css({
        "z-index": 500000,
        top: "10px",
        position: "-webkit-sticky",
      });
      navBarCollapseShow = false;
    } else {
      j$("#SideBarNav").toggle();
      j$("#AdminMainContentContainer").css({
        position: "inherit",
        right: "0",
        width: "auto",
      });
      j$("#AdminMainContentContainer").removeClass("bg-blueGray-100");
      j$("#ReOpenSideBarIcon").css({
        "z-index": 0,
      });
      j$("#ReOpenSideBarIcon").toggle();
      j$("#app > div").append(j$("#ReOpenSideBarIcon"));
      navBarCollapseShow = true;
    }
  }
</script>

<i
  id="ReOpenSideBarIcon"
  on:click={closeSideBar}
  class="fas fa-plus-square hidden sticky left-10 cursor-pointer"
/>
<nav
  id="SideBarNav"
  class="z-50 md:left-0 md:block md:fixed md:top-0 md:bottom-0 md:overflow-y-auto md:flex-row md:flex-nowrap md:overflow-hidden shadow-xl bg-white flex flex-wrap items-center justify-between relative md:w-64 z-10 py-4 px-6"
>
  <div
    class="md:flex-col md:items-stretch md:min-h-full md:flex-nowrap px-0 flex flex-wrap items-center justify-between w-full mx-auto"
  >
    <i
      on:click={closeSideBar}
      class="fas fa-times hidden md:block absolute top-10 right-10 cursor-pointer"
    />
    <!-- Toggler -->
    <button
      class="cursor-pointer text-black opacity-50 md:hidden px-3 py-1 text-xl leading-none bg-transparent rounded border border-solid border-transparent"
      type="button"
      on:click={() => toggleCollapseShow("bg-white m-2 py-3 px-6")}
    >
      <i class="fas fa-bars" />
    </button>
    <!-- Brand -->
    <p
      use:link
      class="md:block text-left md:pb-2 text-blueGray-600 mr-0 inline-block whitespace-nowrap text-sm uppercase font-bold p-4 px-0"
      href="/"
    >
      Scientia Est Potentia
    </p>
    <!-- User -->
    <ul class="md:hidden sidebar-list items-center flex flex-wrap list-none">
      <li class="inline-block relative">
        <NotificationDropdown />
      </li>
      <li class="inline-block relative">
        <UserDropdown />
      </li>
    </ul>
    <!-- Collapse -->
    <div
      class="md:flex md:flex-col md:items-stretch md:opacity-100 md:relative md:mt-4 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1 rounded {collapseShow}"
    >
      <!-- Collapse header -->
      <div
        class="md:min-w-full md:hidden block pb-4 mb-4 border-b border-solid border-blueGray-200"
      >
        <div class="flex flex-wrap">
          <div class="w-6/12">
            <a
              use:link
              class="md:block text-left md:pb-2 text-blueGray-600 mr-0 inline-block whitespace-nowrap text-sm uppercase font-bold p-4 px-0"
              href="/"
            >
              Scientia Est Potentia
            </a>
          </div>
          <div class="w-6/12 flex justify-end">
            <button
              type="button"
              class="cursor-pointer text-black opacity-50 md:hidden px-3 py-1 text-xl leading-none bg-transparent rounded border border-solid border-transparent"
              on:click={() => toggleCollapseShow("hidden")}
            >
              <i class="fas fa-times" />
            </button>
          </div>
        </div>
      </div>
      <!-- Form -->
      <form class="mt-6 mb-4 md:hidden">
        <div class="mb-3 pt-0">
          <input
            type="text"
            placeholder="Search"
            class="border-0 px-3 py-2 h-12 border border-solid border-blueGray-500 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-base leading-snug shadow-none outline-none focus:outline-none w-full font-normal"
          />
        </div>
      </form>

      <!-- Divider -->
      <hr class="my-4 md:min-w-full" />
      <!-- Heading -->
      <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        Dashboards
      </h6>
      <!-- Navigation -->

      <ul
        class="sidebar-list md:flex-col md:min-w-full flex flex-col list-none"
      >
        <li class="items-center">
          <a
            use:link
            href="/admin/dashboard"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/dashboard'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-chart-line mr-2 text-sm {location.href.indexOf(
                '/admin/dashboard'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Arch Dashboard
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/people"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/people'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-user-tie mr-2 text-sm {location.href.indexOf(
                '/admin/people'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            People
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/countries"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/countries'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-globe mr-2 text-sm {location.href.indexOf(
                '/admin/countries'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Countries
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/organizations"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/organizations'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-sitemap mr-2 text-sm {location.href.indexOf(
                '/admin/organizations'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Organizations
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/resources"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/resources'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-gem mr-2 text-sm {location.href.indexOf(
                '/admin/resources'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Resources
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/tables"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/tables'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-table mr-2 text-sm {location.href.indexOf(
                '/admin/tables'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Tables
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/maps"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/maps'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-map mr-2 text-sm {location.href.indexOf(
                '/admin/maps'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Maps, Charts, Graphs
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/timeline"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/timeline'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-arrows-alt-h mr-2 text-sm {location.href.indexOf(
                '/admin/timeline'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Timeline
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/networks"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/networks'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-cloud mr-2 text-sm {location.href.indexOf(
                '/admin/networks'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Networks
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/dictionary"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/dictionary'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-book-open mr-2 text-sm {location.href.indexOf(
                '/admin/dictionary'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Dictionary
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/dashboard-designer"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/dashboard-designer'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-book-open mr-2 text-sm {location.href.indexOf(
                '/admin/dashboard-designer'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Dashboard Designer
          </a>
        </li>
      </ul>

      <!-- Divider -->
      <hr class="my-4 md:min-w-full" />
      <!-- Heading -->
      <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        Archive
      </h6>
      <!-- Navigation -->
      <ul
        class="sidebar-list md:flex-col md:min-w-full flex flex-col list-none md:mb-4"
      >
        <li class="items-center">
          <a
            use:link
            href="/admin/refresh-archive"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/refresh-archive'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-database mr-2 text-sm {location.href.indexOf(
                '/admin/refresh-archive'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Refresh Data
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/raw-archive"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/raw-archive'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-file-archive mr-2 text-sm {location.href.indexOf(
                '/admin/raw-archive'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Raw Archive
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/archive-designer"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/archive-designer'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-file-archive mr-2 text-sm {location.href.indexOf(
                '/admin/archive-designer'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Archive Designer
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            href="/admin/notes"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/notes'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-sticky-note mr-2 text-sm {location.href.indexOf(
                '/admin/notes'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Notes
          </a>
        </li>
      </ul>

      <!-- Divider -->
      <hr class="my-4 md:min-w-full" />
      <!-- Heading -->
      <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        Authentication
      </h6>
      <!-- Navigation -->

      <ul
        class="sidebar-list md:flex-col md:min-w-full flex flex-col list-none md:mb-4"
      >
        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/auth/login"
          >
            <i class="fas fa-fingerprint text-blueGray-300 mr-2 text-sm" />
            Login
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/auth/register"
          >
            <i class="fas fa-clipboard-list text-blueGray-300 mr-2 text-sm" />
            Register
          </a>
        </li>
      </ul>

      <!-- Divider -->
      <hr class="my-4 md:min-w-full" />
      <!-- Heading -->
      <h6
        class="md:min-w-full text-blueGray-500 text-xs uppercase font-bold block pt-1 pb-4 no-underline"
      >
        No Layout Pages
      </h6>
      <!-- Navigation -->

      <ul
        class="sidebar-list md:flex-col md:min-w-full flex flex-col list-none md:mb-4"
      >
        <li class="items-center">
          <a
            use:link
            href="/admin/settings"
            class="text-xs uppercase py-3 font-bold block {location.href.indexOf(
              '/admin/settings'
            ) !== -1
              ? 'text-red-500 hover:text-red-600'
              : 'text-blueGray-700 hover:text-blueGray-500'}"
          >
            <i
              class="fas fa-tv mr-2 text-sm {location.href.indexOf(
                '/admin/settings'
              ) !== -1
                ? 'opacity-75'
                : 'text-blueGray-300'}"
            />
            Settings
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/landing"
          >
            <i class="fas fa-newspaper text-blueGray-300 mr-2 text-sm" />
            Landing Page
          </a>
        </li>

        <li class="items-center">
          <a
            use:link
            class="text-blueGray-700 hover:text-blueGray-500 text-xs uppercase py-3 font-bold block"
            href="/profile"
          >
            <i class="fas fa-user-circle text-blueGray-300 mr-2 text-sm" />
            Profile Page
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>
