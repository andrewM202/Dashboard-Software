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
          placeholder: "Color",
          name: "color",
          value: "",
          popoverMessage: "This is the color",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Color",
          name: "color",
          value: "",
          popoverMessage: "This is the color",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Color",
          name: "color",
          value: "",
          popoverMessage: "This is the color",
          flexdatalistdisabled: true,
        },
        {
          type: "color",
          placeholder: "Color",
          name: "color",
          value: "",
          popoverMessage: "This is the color",
          flexdatalistdisabled: true,
        },
      ],
    },
    {
      Subtitle: "Submit Changes",
      Inputs: [
        {
          type: "submit",
          placeholder: "Collection Creation",
          value: "Submit Change",
          popoverMessage: "Press this button to create the collection",
          postURL: "/admin/color-changes",
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
