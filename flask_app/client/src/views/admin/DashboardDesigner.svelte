<script>
	import { dashboardSettingsEnable, DashboardSave } from "../../../scripts/DashboardDesigner/DashboardSettings.js";
	import { createText } from "../../../scripts/DashboardDesigner/CreateText.js";
	import { createChart } from "../../../scripts/DashboardDesigner/CreateChart.js";
	import { createImage } from "../../../scripts/DashboardDesigner/CreateImage.js";
	import { createTable } from "../../../scripts/DashboardDesigner/CreateTable.js";
	import { loadChart } from "../../../scripts/DashboardDesigner/LoadChart.js";
	import { onDestroy } from "svelte";

	let showActionBar = false;
	let parentOffset;

	onDestroy(
		// Remove added dashboard properties from the HTML element on destruction
		function () {
			j$("html").css("overflow", "");
			j$("html").css("background-color", "");
		}
	);

	// onLoad contains event listeners needing to be attached
	// when #DashboardDesignerContainer is loaded
	function onLoad() {
		j$("#DashboardDesignerContainer").on("contextmenu rightclick", function (event) {
			event.preventDefault();
			// Right mouse click
			if (event.which === 3) {
				// Make the action bar appear at mouse click
				showActionBar = true;
				parentOffset = j$(this).parent().offset();
				j$("#DashboardDesignerContainer > #DashboardDesignerActionBar").css({
					top: event.pageY - parentOffset.top + "px",
					right: j$(window).width() - event.pageX + "px",
				});
			}
			// If the center text exists remove it, as it is just used
			// as an initial guide
			j$("#DashboardDesignerContainer > center").remove();
		});
		// Make the action bar disappear when left clicking
		j$("#DashboardDesignerContainer").on("click", function () {
			showActionBar = false;
		});

		// Make the HTML have no overflow
		j$("html").css("background-color", "rgb(241, 245, 249)");

		j$(document).scroll(function () {
			j$("div#DashboardSettingsContainer").css({
				top: j$(document).scrollTop(),
			});
		});
	} // onLoad() end
</script>

<div use:onLoad id="DashboardDesignerContainer" class="h-screen w-screen border-solid border-blueGray-100 border-r border-b">
	<center style="font-size: 1.2rem; font-weight: bold;">Right Click to Create Chart</center>
	<div class="shadow-xl bg-white w-full flex flex-column justify-between items-center px-4" id="DashboardSettingsContainer">
		<form on:submit={DashboardSave}>
			<div class="w-full" style="margin-top: 100px;">
				<label class="block text-sm font-bold mb-2" for="dashboard-title"> Dashboard Title </label>
				<input style="height: 30px;" class="picker-input w-full" id="dashboard-title" type="text" value="Dashboard Title" name="dashboard_title" />
			</div>
			<div class="w-full" style="margin-top: 100px;">
				<label class="block text-sm font-bold mb-2" for="dashboard-height"> Dashboard Height (% Screenheight) </label>
				<div class="relative input-icon-container">
					<input style="height: 30px;" class="picker-input w-full" id="dashboard-height" type="number" value="100" name="dashboard_height" />
					<span class="absolute">%</span>
				</div>
			</div>
			<div class="w-full" style="margin-top: 25px;">
				<input style="height: 30px; " class="picker-input w-full cursor-pointer placeholder-blueGray-300 text-blueGray-600 hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring ease-linear transition-all duration-150" type="submit" value="Save Dashboard" name="submit" />
			</div>
		</form>
		<hr class="my-4 md:min-w-full" style="background-color: rgb(51, 65, 85); height: 2px;" />
		<div>
			<div class="w-full">
				<label class="block text-sm font-bold mb-2" for="dashboard-title"> Dashboard To Edit </label>
				<select class="picker-input w-full" id="dashboard-title" value="Mimic Value">
					<option value="mimic_value">Current Dashboard</option>
				</select>
			</div>
			<div class="w-full" style="margin-top: 25px;">
				<input style="height: 30px; " class="picker-input w-full cursor-pointer placeholder-blueGray-300 text-blueGray-600 hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring ease-linear transition-all duration-150" type="submit" value="Edit Dashboard" />
			</div>
		</div>
	</div>
	<div on:click={dashboardSettingsEnable} class="dashboard-settings-triangle cursor-pointer" />
	<div id="DashboardDesignerActionBar" style="background-color: rgb(239, 68, 68, 0.85);" class="absolute text-base z-50 float-left py-2 list-none text-left rounded shadow-lg mt-1 min-w-48 {showActionBar ? 'block' : 'hidden'}">
		<a on:click={createChart} href="#pablo" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Chart </a>
		<!-- Load an existing chart instead of creating a new one -->
		<a on:click={loadChart} href="#pablo" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Load Chart </a>
		<div class="h-0 my-2 border border-solid border-t-0 border-blueGray-800 opacity-25" />
		<a on:click={createText} href="#pablo" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Text </a>
		<a on:click={createImage} href="#pablo" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Image </a>
		<a on:click={createTable} href="#pablo" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Table </a>
	</div>
</div>

<style>
	.input-icon-container span {
		right: 5%;
		top: 5%;
	}
	.dashboard-settings-triangle {
		width: 100px;
		height: 100px;
		background-color: rgba(239, 68, 68, 0.5);
		transform: rotate(135deg) translate(-71%, 0);
		position: fixed;
		right: 0;
		top: 0;
		z-index: 51;
	}
	div#DashboardSettingsContainer {
		position: absolute;
		right: 0;
		top: 0;
		width: 200px;
		height: 100vh;
		background-color: white;
		display: none;
		border-left: 3px solid #e3e6f0;
		z-index: 50;
		flex-direction: column;
		justify-content: space-around;
	}
	/* Move the increment and decrement button over
    so we can see the icon in the number input field */
	input[type="number"]::-webkit-outer-spin-button,
	input[type="number"]::-webkit-inner-spin-button {
		transform: translateX(-75%);
	}
</style>
