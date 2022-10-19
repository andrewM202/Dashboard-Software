<script>
	export let SettingsFunction = function () {};
	export let KeyIconDisabled = false;
	export let CogsIconDisabled = false;
</script>

<div
	id="SettingsBarContainer"
	class="flex justify-end items-center align-center"
	style="background: rgb(210,207,207);
    background: linear-gradient(90deg, rgba(210,207,207,1) 0%, rgba(249,249,249,1) 50%, rgba(209,208,208,1) 100%);
    width: 100%; height: 30px; filter: drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) drop-shadow(0 8px 5px rgb(0 0 0 / 0.08));"
>
	{#if KeyIconDisabled !== true}
		<i class="fa fa-key mr-4 cursor-pointer" aria-hidden="true" />
	{/if}
	{#if CogsIconDisabled !== true}
		<i
			use:SettingsFunction
			class="fa fa-cogs mr-4 cursor-pointer"
			aria-hidden="true"
		/>
	{/if}
</div>
