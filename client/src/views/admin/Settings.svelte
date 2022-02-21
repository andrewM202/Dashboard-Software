<script>
  // core components
  import CardSettings from "components/Cards/CardSettings.svelte";
  export let location;
  import { userSettingsStore } from "../../stores.js";

  let settingsConfig;
  $: settingsConfig = $userSettingsStore;

  let tableData = [];
  $: tableData = [$userSettingsStore];

  let adminSettings;
  $: adminSettings = [
    {
      Subtitle: "Color Customization",
      Inputs: [
        {
          type: "color",
          placeholder: "Sidebar Color",
          name: "sidebar-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].sidebar_color === null
                ? "#FFFFFF"
                : settingsConfig[0].sidebar_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Header Color",
          name: "archive-header-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].archive_header_color === null
                ? "#EF4444"
                : settingsConfig[0].archive_header_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Table Background Color",
          name: "archive-table-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].archive_table_color === null
                ? "#EF4444"
                : settingsConfig[0].archive_table_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Table Headers Color",
          name: "archive-table-header-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].archive_table_header_color === null
                ? "#BE123C"
                : settingsConfig[0].archive_table_header_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Table Alt Row Color",
          name: "archive-table-alt-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].archive_table_alt_color === null
                ? "#DC2626"
                : settingsConfig[0].archive_table_alt_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Creation Card Color",
          name: "archive-creation-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].archive_creation_color === null
                ? "#EF4444"
                : settingsConfig[0].archive_creation_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Background Color",
          name: "background-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].background_color === null
                ? "#F1F5F9"
                : settingsConfig[0].background_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Footer Color",
          name: "footer-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].footer_color === null
                ? "#F1F5F9"
                : settingsConfig[0].footer_color
              : "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Navigation Color",
          name: "navigation-color",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].navigation_color === null
                ? "#EF4444"
                : settingsConfig[0].navigation_color
              : "",
          flexdatalistdisabled: true,
        },
      ],
    },
    {
      Subtitle: "Look",
      Inputs: [
        {
          type: "checkbox",
          placeholder: "Sidebar State",
          name: "sidebar-state",
          value:
            settingsConfig !== undefined
              ? settingsConfig[0].sidebar_state === true
                ? "on"
                : "off"
              : "",
          popoverMessage: "Should the sidebar be closed or open by default?",
          flexdatalistdata: ["Closed", "Open"],
          flexdataid: Math.random().toString(36).substring(2, 8),
        },
      ],
    },
    {
      Subtitle: "Submit Changes",
      Inputs: [
        {
          type: "submit",
          placeholder: "Submit Changes",
          value: "Submit Change",
          popoverMessage: "Press this button to create the collection",
          postURL: "/admin/setting-changes",
        },
      ],
    },
    {
      Subtitle: "Reset To Defaults",
      Inputs: [
        {
          type: "submit",
          placeholder: "Set Default Settings",
          value: "Reset To Defaults",
          popoverMessage: "Reset all settings to defaults",
          postURL: "/admin/set-default-settings",
          confirmationRequired: true,
        },
      ],
    },
  ];
</script>

<div class="flex flex-wrap">
  <div class="w-full px-4">
    {#if tableData.includes(undefined) !== true}
      <CardSettings
        settings={adminSettings}
        title={"Site Settings"}
        clearForm={false}
      />
    {:else}
      <CardSettings settings={[]} title={"Site Settings"} />
    {/if}
  </div>
</div>
