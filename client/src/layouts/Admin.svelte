<script>
  import { Router, Route } from "svelte-routing";
  import { userSettingsStore } from "../stores.js";

  // Users Settings
  let UserSettings;
  $: UserSettings = $userSettingsStore;

  // components for this layout
  import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
  import Sidebar from "components/Sidebar/Sidebar.svelte";
  import HeaderStats from "components/Headers/HeaderStats.svelte";
  import FooterAdmin from "components/Footers/FooterAdmin.svelte";

  // pages for this layout
  import RawArchive from "views/admin/RawArchive.svelte";
  import ArchiveDesigner from "views/admin/ArchiveDesigner.svelte";
  import ArchiveUpload from "views/admin/ArchiveUpload.svelte";
  import DashboardDesigner from "views/admin/DashboardDesigner.svelte";
  import Notes from "views/admin/Notes.svelte";
  import Dashboard from "views/admin/Dashboard.svelte";
  import Settings from "views/admin/Settings.svelte";
  import Tables from "views/admin/Tables.svelte";
  import Maps from "views/admin/Maps.svelte";

  export let location;
</script>

{#if ["/admin/dashboard", "/admin/tables", "/admin/maps"].includes(location.pathname)}
  <div>
    {#if UserSettings !== undefined}
      <Sidebar
        {location}
        sidebarBackgroundColor={UserSettings[0].sidebar_color !== undefined &&
        UserSettings[0].sidebar_color !== null
          ? `Background-color: ${UserSettings[0].sidebar_color}`
          : undefined}
        sidebarDefaultToggled={UserSettings[0].sidebar_state !== undefined &&
        UserSettings[0].sidebar_state !== null
          ? UserSettings[0].sidebar_state
          : true}
      />
    {:else}
      <Sidebar {location} />
    {/if}
    <div class="relative md:ml-64 bg-blueGray-100">
      <AdminNavbar />
      <HeaderStats />
      <div class="px-4 md:px-10 mx-auto w-full m-24">
        <Router url="admin">
          <Route path="dashboard" component={Dashboard} />
          <Route path="settings" component={Settings} />
          <Route path="tables" component={Tables} />
          <Route path="maps" component={Maps} />
          <Route path="raw-archive" component={RawArchive} />
          <Route path="notes" component={Notes} />
          <Route path="archive-designer" component={ArchiveDesigner} />
          <Route path="archive-upload" component={ArchiveUpload} />
          <Route path="dashboard-designer" component={DashboardDesigner} />
        </Router>
        {#if UserSettings !== undefined}
          <FooterAdmin
            footerBGColor={UserSettings[0].footer_color !== undefined &&
            UserSettings[0].footer_color !== null
              ? `Background-color: ${UserSettings[0].footer_color}`
              : undefined}
          />
        {:else}
          <FooterAdmin />
        {/if}
      </div>
    </div>
  </div>
{:else}
  <div>
    {#if UserSettings !== undefined}
      <Sidebar
        {location}
        sidebarBackgroundColor={UserSettings[0].sidebar_color !== undefined &&
        UserSettings[0].sidebar_color !== null
          ? `Background-color: ${UserSettings[0].sidebar_color}`
          : undefined}
        sidebarDefaultToggled={UserSettings[0].sidebar_state !== undefined &&
        UserSettings[0].sidebar_state !== null
          ? UserSettings[0].sidebar_state
          : true}
      />
    {:else}
      <Sidebar {location} />
    {/if}
    <div class="relative md:ml-64 bg-blueGray-100">
      <div id="AdminMainContentContainer" class="mx-auto w-full">
        <Router url="admin">
          <Route path="dashboard" component={Dashboard} />
          <Route path="settings" component={Settings} />
          <Route path="tables" component={Tables} />
          <Route path="maps" component={Maps} />
          <Route path="raw-archive" component={RawArchive} />
          <Route path="notes" component={Notes} />
          <Route path="archive-designer" component={ArchiveDesigner} />
          <Route path="archive-upload" component={ArchiveUpload} />
          <Route path="dashboard-designer" component={DashboardDesigner} />
        </Router>
        {#if UserSettings !== undefined}
          <FooterAdmin
            footerBGColor={UserSettings[0].footer_color !== undefined &&
            UserSettings[0].footer_color !== null
              ? `Background-color: ${UserSettings[0].footer_color}`
              : undefined}
          />
        {:else}
          <FooterAdmin />
        {/if}
      </div>
    </div>
  </div>
{/if}
