<script>
  // core components
  import CardSettings from "components/Cards/CardSettings.svelte";
  export let location;

  let adminSettings = [
    {
      Subtitle: "Color Customization",
      Inputs: [
        {
          type: "color",
          placeholder: "Sidebar Color",
          name: "sidebar-color",
          value: "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Header Color",
          name: "archive-header-color",
          value: "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Table Color",
          name: "archive-table-color",
          value: "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Archive Creation Card Color",
          name: "archive-creation-color",
          value: "",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Background Color",
          name: "background-color",
          value: "",
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
          value: "",
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
  <div class="w-full px-4 h-90vh">
    <CardSettings settings={adminSettings} title={"Site Settings"} />
  </div>
</div>
