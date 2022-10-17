<script>
	// core components
	import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
	import HeaderStats from "components/Headers/HeaderStats.svelte";
	import CardTable from "components/Cards/CardTable.svelte";
	import DataCreationCard from "components/Cards/DataCreationCard.svelte";
	import SettingsBar from "components/Headers/SettingsBar.svelte";
	import { dataSettingsStore, userSettingsStore } from "../../stores.js";

	// Defines input buttons for HeaderStats
	let DataSettings, UserSettings;

	$: DataSettings = $dataSettingsStore;
	$: UserSettings = $userSettingsStore;

	let navItems = [];
	$: if (DataSettings !== undefined) {
		let entries = Object.entries(DataSettings);
		for (let entry of entries) {
			// Only add the item if its not already in there
			if (!navItems.includes(entry[0])) {
				navItems.push(entry[0]);
			}
		}
	}

	// Searh function for headerstats
	function SearchResults(e) {
		e.preventDefault();
		let formSelector;
		// Instead of hard coding form selector, find first form element
		// and set that as selector
		for (let i = 0; i < e.path.length; i++) {
			if (e.path[i].tagName === "FORM") {
				formSelector = e.path[i];
				break;
			}
		}
		// console.log(selector);
		// Get data from form
		let data = j$(formSelector).serialize(); //j$(`form#${formID}`).serialize();
		// Clear form
		j$(formSelector).trigger("reset"); // j$(`form#${formID}`).trigger("reset");
		// Get search results for collection
		j$.ajax({
			type: "POST",
			url: "/admin/archive-data/search-data/",
			data: data,
			success: function (data) {
				// Data returns as string, turn into JSON
				data = JSON.parse(data);
				// On success, replace the correlating collection
				// data in the dataSettingsStore to the updated,
				// filtered data
				for (let entry of Object.entries($dataSettingsStore)) {
					if (entry[1].CollectionName === data.CollectionName) {
						$dataSettingsStore[entry[0]].Table.Data = [data.data];
					}
				}
			},
			error: function (error) {
				console.log("Error");
				console.log(error);
			},
		});
	}

	// Function for raw archive data table slider
	// This function is for resizing the parent div
	function archiveTableSliderStyling(e) {
		let parent = j$(e).parent()[0];
		j$(e).mousedown(function (downEv) {
			downEv.preventDefault();
			j$(window).mousemove(function (moveEv) {
				let initialPos = j$(e).offset().top;
				let movePos = moveEv.pageY;
				let addHeight = movePos - initialPos;
				j$("body").css("cursor", "ns-resize");
				if (j$(parent).innerHeight() >= 600) {
					if (j$(parent).innerHeight() + addHeight < 600) {
						j$(parent).innerHeight(600);
					} else {
						j$(parent).innerHeight(
							j$(parent).innerHeight() + addHeight
						);
					}
				}
			});
			j$(window).mouseup(function () {
				j$(window).unbind("mousemove");
				j$("body").css("cursor", "");
			});
		});
	}

	function loadSettingsEvent(event) {
		j$(event).click(function () {
			j$("body").append(`
                <div id="temporary-background-gray" style="position: absolute; left: 0; top: 0;
                z-index: 10000000000;
                width: 100vw;
                height: 100vh;
                background-color: rgb(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                ">
                    <div id="chart-settings-container" class="relative bg-white rounded shadow-lg p-4">
                        <i id="DashboardSettingsCloseIcon" style="width: 10px; height: 10px;" 
                        class="fas fa-times absolute top-10 right-10 cursor-pointer"></i>
                        <h1 class="text-xl font-bold mb-4">Chart Settings</h1>
                        <form>
                            <div class="flex justify-between">
                                <div class="w-1/2" style="margin-right: 10px;">
                                    <label class="block text-sm font-bold mb-2" for="text-color">
                                        Chart Background Color
                                    </label>
                                    <input
                                        style="height: 30px;"
                                        class="picker-input w-full"
                                        id="text-color"
                                        type="color"
                                        value="#000000"
                                    />
                                </div>
                                <div class="w-1/2" margin-left: 10px;>
                                    <label style="margin-left: 10px;" class="block text-sm font-bold mb-2" for="text-size">
                                        Chart Text Size
                                    </label>
                                    <input
                                        style="height: 30px;"
                                        class="picker-input w-full"
                                        id="text-size"
                                        type="number"
                                        value="4"
                                    />
                                </div>
                            </div>
                            <div class="flex justify-between" style="margin-top: 10px;">
                                <div class="w-1/2" style="margin-right: 10px;">
                                    <label class="block text-sm font-bold mb-2" for="text-font">
                                        Chart Text Font
                                    </label>
                                    <select
                                        style="height: 40px;"
                                        class="picker-input w-full"
                                        id="text-font"
                                        type="text"
                                        value="Arial"
                                    >
                                        <option value="Arial">Arial</option>
                                        <option value="Times New Roman">Times New Roman</option>
                                        <option value="Helvetica">Helvetica</option>
                                        <option value="Courier New">Courier New</option>
                                        <option value="Georgia">Georgia</option>
                                        <option value="Verdana">Verdana</option>
                                        <option value="Tahoma">Tahoma</option>
                                        <option value="Palatino">Palatino</option>
                                    </select>
                                </div>
                                <div class="w-1/2" style="margin-left: 10px;">
                                    <label class="block text-sm font-bold mb-2" for="chart-title">
                                        Chart Title
                                    </label>
                                    <input
                                        style="height: 40px;"
                                        class="picker-input w-full"
                                        id="chart-title"
                                        type="text"
                                        value="test"
                                        placeholder="Chart Title"
                                    />
                                </div>
                            </div>
                            <div class="flex justify-between" style="margin-top: 10px;">
                                <div class="w-1/2" style="margin-right: 10px;">
                                    <label class="block text-sm font-bold mb-2" for="chart-type">
                                        Chart Type
                                    </label>
                                    <select
                                        style="height: 40px;"
                                        class="picker-input w-full"
                                        id="chart-type"
                                        type="text"
                                    > 
                                        <option value="network">Network Graph</option>
                                        <option value="timeline">Timeline</option>
                                    </select>
                                </div>
                                <div class="w-1/2" style="margin-left: 10px;">
                                </div>
                            </div>
                            <div class="w-full" style="margin-right: 10px; margin-left: 10px; margin-top: 10px;">
                                <label class="block text-center text-sm font-bold mb-2" for="chart-type">
                                    Confirm Values
                                </label>
                                <input type="submit" value="Submit" style="background-color: rgb(0, 0, 0, 0.2)" class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150">
                            </div>
                        </form>
                    </div>    
                </div>
            `);

			// Event listener for clicking the submit button
			// and enacting all the settings
			j$("input[type=submit]").click(function (e) {
				e.preventDefault();
			});

			// Add event listener for closing the settings
			j$(`#chart-settings-container #DashboardSettingsCloseIcon`).click(
				function () {
					j$("#temporary-background-gray").remove();
				}
			);
			j$("#temporary-background-gray").click(function (ev) {
				// Only close if we click on the background, and ignore clicks on the settings
				if (j$(ev.target).is(j$("#temporary-background-gray"))) {
					j$("#temporary-background-gray").remove();
				}
			});
		});
	}

	// Create a mapping for the table so we know
	// form input -> input type

	// Bind openTab to AdminNavbar component
	let openTab = 0;
</script>

<SettingsBar SettingsFunction={loadSettingsEvent} />
{#if DataSettings !== undefined && UserSettings !== undefined}
	<AdminNavbar
		bind:openTab
		{navItems}
		navBarBGColor={UserSettings[0].navigation_color !== undefined &&
		UserSettings[0].navigation_color !== null
			? `Background-color: ${UserSettings[0].navigation_color}`
			: undefined}
	/>
	{#each Object.entries(DataSettings) as section}
		<div
			class={navItems[openTab] === section[0] ? "block" : "hidden"}
			id="TableHiddenBlockContainer"
		>
			<HeaderStats
				id={section[0]}
				cards={section[1].Cards}
				title={navItems[openTab]}
				titleFontSize={"text-4xl"}
				inputs={section[1].HeaderSearchInputs}
				CollectionName={section[1].CollectionName}
				SearchFunction={SearchResults}
				headerBGColor={UserSettings[0].archive_header_color !==
					undefined && UserSettings[0].archive_header_color !== null
					? `Background-color: ${UserSettings[0].archive_header_color}`
					: undefined}
			/>
			<div
				style={UserSettings[0].background_color !== undefined &&
				UserSettings[0].background_color !== null
					? `Background-color: ${UserSettings[0].background_color}`
					: undefined}
				class="block lg:px-10 mx-auto w-full my-12"
			>
				<div class="flex flex-wrap ml-8 w-full">
					<div
						class="w-full relative h-650-px bg-blueGray-700 mt-12 mb-12 flex flex-col p-6"
					>
						<div
							use:archiveTableSliderStyling
							style="right: -4px; bottom: -4px; cursor: ns-resize;"
							class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
						/>
						<div
							use:archiveTableSliderStyling
							style="left: -4px; bottom: -4px; cursor: ns-resize;"
							class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
						/>
						<CardTable
							color="dark"
							data={section[1].Table.Data[0]}
							CollectionName={section[1].CollectionName}
							headers={section[1].Table.Headers}
							DBFieldNames={section[1].Table.DBFieldNames}
							title={section[1].Table.Title}
							tableBGColor={UserSettings[0]
								.archive_table_color !== undefined &&
							UserSettings[0].archive_table_color !== null
								? `Background-color: ${UserSettings[0].archive_table_color}`
								: undefined}
							tableHeaderColor={UserSettings[0]
								.archive_table_header_color !== undefined &&
							UserSettings[0].archive_table_header_color !== null
								? `Background-color: ${UserSettings[0].archive_table_header_color}`
								: undefined}
							tableAltColor={UserSettings[0]
								.archive_table_alt_color !== undefined &&
							UserSettings[0].archive_table_alt_color !== null
								? UserSettings[0].archive_table_alt_color
								: undefined}
							inputs={section[1].CreationCard.Inputs}
						/>
					</div>
				</div>
			</div>
			<div
				style={UserSettings[0].background_color !== undefined &&
				UserSettings[0].background_color !== null
					? `Background-color: ${UserSettings[0].background_color}`
					: undefined}
				class="lg:px-10 mx-auto w-full"
			>
				<div class="flex flex-wrap ml-8">
					<div class="w-full h-auto bg-blueGray-700 mb-12 p-6">
						{#if section[1].CreationCard !== undefined}
							<DataCreationCard
								CollectionName={section[1].CollectionName}
								flexdata={section[1].CreationCard
									.Flexdatalistdata}
								title={section[1].CreationCard.Title}
								inputs={section[1].CreationCard.Inputs}
								creationColor={UserSettings[0]
									.archive_creation_color !== undefined &&
								UserSettings[0].archive_creation_color !== null
									? `Background-color: ${UserSettings[0].archive_creation_color}`
									: undefined}
							/>
						{/if}
					</div>
				</div>
			</div>
		</div>
	{/each}
{/if}
