<script>
    import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
    import HeaderStats from "components/Headers/HeaderStats.svelte";
    import CardSettings from "components/Cards/CardSettings.svelte";

    let titleSearchInputs = [
        {
            type: "Text",
            placeholder: "First Name",
            name: "FirstName",
        },
        {
            type: "Text",
            placeholder: "Last Name",
            name: "LastName",
        },
        {
            type: "Text",
            placeholder: "Organizations",
            name: "Organizations",
        },
        {
            type: "Text",
            placeholder: "Titles",
            name: "Titles",
        },
        {
            type: "Text",
            placeholder: "Opinions",
            name: "Opinion",
        },
        {
            type: "Submit",
            placeholder: "Search",
            name: "",
        },
    ];
</script>

<AdminNavbar title={"Archive Designer"} />
<HeaderStats
    title={"Archive Designer"}
    titleFontSize={"text-6xl"}
    titleColor={"text-black"}
    inputs={titleSearchInputs}
/>
<div class="mt-4 w-full md:w-11/12 h-auto px-4"><CardSettings /></div>
