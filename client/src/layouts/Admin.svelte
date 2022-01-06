<script>
  import { Router, Route } from "svelte-routing";

  // components for this layout
  import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
  import Sidebar from "components/Sidebar/Sidebar.svelte";
  import HeaderStats from "components/Headers/HeaderStats.svelte";
  import FooterAdmin from "components/Footers/FooterAdmin.svelte";

  // pages for this layout
  import RawArchive from "views/admin/RawArchive.svelte";
  import Notes from "views/admin/Notes.svelte";
  import Dashboard from "views/admin/Dashboard.svelte";
  import Settings from "views/admin/Settings.svelte";
  import Tables from "views/admin/Tables.svelte";
  import Maps from "views/admin/Maps.svelte";

  export let location;
</script>

{#if ["/admin/dashboard", "/admin/tables", "/admin/maps", "/admin/notes"].includes(location.pathname)}
  <div>
    <Sidebar {location} />
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
        </Router>
        <FooterAdmin />
      </div>
    </div>
  </div>
{:else}
  <div>
    <Sidebar {location} />
    <div class="relative md:ml-64 bg-blueGray-100">
      <div id="AdminMainContentContainer" class="mx-auto w-full">
        <Router url="admin">
          <Route path="dashboard" component={Dashboard} />
          <Route path="settings" component={Settings} />
          <Route path="tables" component={Tables} />
          <Route path="maps" component={Maps} />
          <Route path="raw-archive" component={RawArchive} />
          <Route path="notes" component={Notes} />
        </Router>
        <FooterAdmin />
      </div>
    </div>
  </div>
{/if}
