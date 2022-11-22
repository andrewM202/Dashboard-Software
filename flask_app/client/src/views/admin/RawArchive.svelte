<script>
	// core components
	import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
	import HeaderStats from "components/Headers/HeaderStats.svelte";
	import CardTable from "components/Cards/CardTable.svelte";
	import DataCreationCard from "components/Cards/DataCreationCard.svelte";
	import SettingsBar from "components/Headers/SettingsBar.svelte";
	import { dataSettingsStore, userSettingsStore } from "../../stores.js";

	// Popover Stuff Start
	import { createPopper } from "@popperjs/core";
	import { onMount, tick } from "svelte";

	let popoverShow = false;
	let btnRef;
	let popoverRef;

	let btnRef2;
	let popoverRef2;
	let popoverShow2 = false;

	function toggleTooltip(btnref, popref, popShow) {
		if (popShow === "popoverShow" && popoverShow === true) {
			popoverShow = false;
		} else if (popShow === "popoverShow2" && popoverShow2 === true) {
			popoverShow2 = false;
		} else {
			if (popShow === "popoverShow") {
				popoverShow = true;
				createPopper(btnRef, popoverRef, {
					placement: "left",
				});
			} else if (popShow === "popoverShow2") {
				popoverShow2 = true;
				createPopper(btnRef2, popoverRef2, {
					placement: "left",
				});
			}
		}
	}

	class popover {
		constructor(btnRef, popoverRef) {
			this.popoverShow = false;
			this.btnRef = btnRef;
			this.popoverRef = popoverRef;
		}
		toggleTooltip() {
			if (this.popoverShow) {
				this.popoverShow = false;
			} else {
				this.popoverShow = true;
				createPopper(this.btnRef, this.popoverRef, {
					placement: "top",
					// Modifer to give padding to popover
					modifiers: [
						{
							name: "preventOverflow",
							options: {
								padding: 50,
							},
						},
					],
				});
			}
		}
	}
	// Popover Stuff End

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
				// Adjust the height of the archive table too so it resizes with its parent
				j$("#archiveDataTable0")
					.closest(".dataTables_scrollBody")
					.css("height", j$(parent).innerHeight() - 310);
				j$("#archiveDataTable0").DataTable().draw();
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

	// Use this variables and event listeners
	// to detect when we go out of fullscreen.
	// When we do set the datatable's height back to its normal
	// non-auto auto
	let datatableHeight = null;
	let datatableElem;
	document.addEventListener("fullscreenchange", exitHandler, false);
	document.addEventListener("mozfullscreenchange", exitHandler, false);
	document.addEventListener("MSFullscreenChange", exitHandler, false);
	document.addEventListener("webkitfullscreenchange", exitHandler, false);

	function exitHandler() {
		if (
			!document.webkitIsFullScreen &&
			!document.mozFullScreen &&
			!document.msFullscreenElement
		) {
			// Make the datatable's height back to what it was
			// before it was fullscreen
			j$(datatableElem).css("height", datatableHeight);
			datatableHeight = null;
		}
	}

	// This function is called for the very first data table only.
	function makeDataTableInitial(evt) {
		let table;
		let tableCreated = false;

		// Initialize datatable if its not already initialized
		if (!j$.fn.dataTable.isDataTable(`#${j$(evt)[0].id}`)) {
			table = new DataTable(`#${j$(evt)[0].id}`, {
				dom: "QBlfrtip",
				buttons: [
					{
						text: "copy",
						className: "cursor-pointer",
					},
					{
						text: "csv",
						className: "cursor-pointer",
					},
					{
						text: "excel",
						className: "cursor-pointer",
					},
					{
						text: "pdf",
						className: "cursor-pointer",
					},
					{
						text: "print",
						className: "cursor-pointer",
					},
					{
						// Button to download as JSON
						text: "Json",
						action: function (e, dt, node, config) {
							const name = `${
								Object.entries(DataSettings)[openTab][1]
									.CollectionName
							}.json`;
							const saveData = JSON.stringify(
								Object.entries(DataSettings)[openTab][1].Table
									.Data[0],
								undefined,
								2
							);

							const a = document.createElement("a");
							// const type = name.split(".").pop();
							a.href = URL.createObjectURL(
								new Blob([saveData], {
									// type: `text/${type === "txt" ? "plain" : type}`,
									type: "json",
								})
							);
							a.download = name;
							a.click();
						},
					},
					{
						// Fullscreen button
						text: "Fullscreen",
						action: function (e, dt, node, config) {
							// Make the datatable have an auto height while
							// we are in full screen mode so the datatable
							// fits the full screen
							if (datatableHeight === null) {
								datatableHeight = j$(
									j$(e.target).parentsUntil(
										"div.tableBorder"
									)[
										j$(e.target).parentsUntil(
											"div.tableBorder"
										).length - 1
									]
								)
									.parent()
									.css("height");

								j$(
									j$(e.target).parentsUntil(
										"div.tableBorder"
									)[
										j$(e.target).parentsUntil(
											"div.tableBorder"
										).length - 1
									]
								)
									.parent()
									.css("height", "auto");
								datatableElem = j$(
									j$(e.target).parentsUntil(
										"div.tableBorder"
									)[
										j$(e.target).parentsUntil(
											"div.tableBorder"
										).length - 1
									]
								).parent();
								j$(
									j$(e.target).parentsUntil(".tableBorder")[
										j$(e.target).parentsUntil(
											".tableBorder"
										).length - 1
									]
								)
									.parent()
									.fullScreen(true);
							}
						},
					},
				],
				searchBuilder: {},
				colReorder: true,
				rowReorder: {
					selector: "td:nth-child(1)",
				},
				fixedColumns: true,
				scrollY: "auto",
				scrollX: true,
				scrollCollapse: true,
				fixedHeader: {
					header: true,
					footer: true,
				},
				columnDefs: [{ targets: 0, visible: false }],
				keys: true,
				select: true,
				// initComplete called once in table lifespan when its created
				drawCallback: function () {
					// Make the page number of results (i.e. 10 results per page)
					// be 75px wide so the icon does not go over the number
					j$(".dataTables_length select").css("width", "75px");
					// Detect cell overflow for each table entry
					// now that we have completed creating the datatable
					for (let event of j$(`#${j$(evt)[0].id} td`)) {
						detectCellOverflow(event);
					}
				},
			});
		}
	}

	// This function is called every time the openTab variable is changed,
	// to see if we need to generate the datatable for this tab
	// because we only want to load the datatable when its visible. This also
	// allows the overflow popovers to generate correctly because if the element is hidden
	// it will never generate the overflow popover otherwise
	function makeDataTable() {
		let table;

		for (let dataTable of j$(".archiveDataTable")) {
			if (
				dataTable.id.split("archiveDataTable")[1] == openTab &&
				dataTable.id.split("archiveDataTable")[1] !== 0
			) {
				// Initialize datatable if its not already initialized
				if (!j$.fn.dataTable.isDataTable(`#${dataTable.id}`)) {
					table = new DataTable(`#${dataTable.id}`, {
						dom: "QBlfrtip",
						buttons: [
							"copy",
							"csv",
							"excel",
							"pdf",
							"print",
							{
								// Button to download as JSON
								text: "Json",
								action: function (e, dt, node, config) {
									const name = `${
										Object.entries(DataSettings)[openTab][1]
											.CollectionName
									}.json`;
									const saveData = JSON.stringify(
										Object.entries(DataSettings)[openTab][1]
											.Table.Data[0],
										undefined,
										2
									);

									const a = document.createElement("a");
									// const type = name.split(".").pop();
									a.href = URL.createObjectURL(
										new Blob([saveData], {
											// type: `text/${type === "txt" ? "plain" : type}`,
											type: "json",
										})
									);
									a.download = name;
									a.click();
								},
							},
							{
								// Fullscreen button
								text: "Fullscreen",
								action: function (e, dt, node, config) {
									// Make the datatable have an auto height while
									// we are in full screen mode so the datatable
									// fits the full screen
									if (datatableHeight === null) {
										datatableHeight = j$(
											j$(e.target).parentsUntil(
												"div.tableBorder"
											)[
												j$(e.target).parentsUntil(
													"div.tableBorder"
												).length - 1
											]
										)
											.parent()
											.css("height");

										j$(
											j$(e.target).parentsUntil(
												"div.tableBorder"
											)[
												j$(e.target).parentsUntil(
													"div.tableBorder"
												).length - 1
											]
										)
											.parent()
											.css("height", "auto");
										datatableElem = j$(
											j$(e.target).parentsUntil(
												"div.tableBorder"
											)[
												j$(e.target).parentsUntil(
													"div.tableBorder"
												).length - 1
											]
										).parent();
										j$(
											j$(e.target).parentsUntil(
												".tableBorder"
											)[
												j$(e.target).parentsUntil(
													".tableBorder"
												).length - 1
											]
										)
											.parent()
											.fullScreen(true);
									}
								},
							},
						],
						searchBuilder: {},
						colReorder: true,
						rowReorder: {
							selector: "td:nth-child(1)",
						},
						// fixedColumns: true,
						// scrollY: "auto",
						// scrollX: true,
						// scrollCollapse: true,
						// columnDefs: [{ targets: 0, visible: false }],
						keys: true,
						select: true,
						// initComplete called once in table lifespan when its created
						initComplete: function () {
							// Make the page number of results (i.e. 10 results per page)
							// be 75px wide so the icon does not go over the number
							j$(".dataTables_length select").css(
								"width",
								"75px"
							);
							// Detect cell overflow for each table entry
							// now that we have completed creating the datatable
							for (let event of j$(`#${dataTable.id} td`)) {
								detectCellOverflow(event);
							}
						},
						drawCallback: function () {
							// Make the page number of results (i.e. 10 results per page)
							// be 75px wide so the icon does not go over the number
							j$(".dataTables_length select").css(
								"width",
								"75px"
							);
							// Detect cell overflow for each table entry
							// now that we have completed creating the datatable
							for (let event of j$(`#${dataTable.id} td`)) {
								detectCellOverflow(event);
							}
						},
					});
				}
			}
		}
	}

	// On page load, svelte loads all elements for all tables
	// but they are not visible. This makes it so scrollWidth is 0
	// but innerWidth() is > 0. We need to wait until the scrollWidth is
	// not zero (when the table is clicked on and displayed) to check if it
	// should have the overflow popper applied to it
	let detectOverflowLater = [];

	onMount(() => {
		j$("nav").click(function () {
			for (let i = 0; i < detectOverflowLater.length; i++) {
				let e = j$(detectOverflowLater[i].event)[0];
				if (
					j$(e)[0].scrollWidth > Math.ceil(j$(e).innerWidth()) &&
					j$(e).children().length === 0
				) {
					// This element is now found to be overflown, remove it from
					// detectOverflowLater
					detectOverflowLater[i].remove = true;
					j$(e).append(`<div
                      style="background-color: rgb(251 113 133); white-space: normal; max-width: 500px; height: auto;"
                      class="hidden z-50 text-white font-semibold p-3 uppercase rounded-t-lg"
                    >
                      <span>${j$(e).text()}</span>
                    </div>`);
					let pop = new popover(e, j$(e).children("div")[0]);
					j$(e).mouseenter(function () {
						pop.toggleTooltip();
						j$(e).find("div").removeClass("hidden");
						j$(e).find("div").addClass("block");
					});
					j$(e).mouseleave(function () {
						pop.toggleTooltip();
						j$(e).find("div").addClass("hidden");
						j$(e).find("div").removeClass("block");
					});
				} else if (
					j$(e)[0].scrollWidth !== 0 &&
					j$(e)[0].scrollWidth === Math.ceil(j$(e).innerWidth())
				) {
					// This element is not found to be overflown, remove it from
					// detectOverflowLater
					detectOverflowLater[i].remove = true;
				}
			}
			let overflowCopy = [];
			for (let i = 0; i < detectOverflowLater.length; i++) {
				if (!detectOverflowLater[i].remove) {
					overflowCopy.push(detectOverflowLater[i]);
				}
			}
			detectOverflowLater = overflowCopy;
		});
	});
	async function detectCellOverflow(e) {
		await tick();
		// Detect if a <td> is overflowing in the card table.
		// If it is, add a hover to see the entire text
		setTimeout(function () {
			if (j$(e)[0].scrollWidth === 0) {
				detectOverflowLater.push({
					event: j$(e),
					remove: false,
				});
			} else if (
				j$(e)[0].scrollWidth > Math.ceil(j$(e).innerWidth()) &&
				j$(e).children().length === 0
			) {
				j$(e).append(`<div
                      style="background-color: rgb(251 113 133); white-space: normal; max-width: 500px; height: auto;"
                      class="hidden z-50 text-white font-semibold p-3 rounded-t-lg"
                    >
                      <span>${j$(e).text()}</span>
                    </div>`);
				let pop = new popover(e, j$(e).children("div")[0]);
				j$(e).mouseenter(function () {
					pop.toggleTooltip();
					j$(e).find("*").removeClass("hidden");
					j$(e).find("*").addClass("block");
				});
				j$(e).mouseleave(function () {
					pop.toggleTooltip();
					j$(e).find("*").addClass("hidden");
					j$(e).find("*").removeClass("block");
				});
			}
		}, 300);
	}

	// Create a mapping for the table so we know
	// form input -> input type

	// Bind openTab to AdminNavbar component
	let openTab = 0;

	$: openTab, makeDataTable();
</script>

<SettingsBar SettingsFunction={loadSettingsEvent} />
{#if DataSettings !== undefined && UserSettings !== undefined && DataSettings != null && UserSettings != null}
	<AdminNavbar
		bind:openTab
		{navItems}
		navBarBGColor={UserSettings[0].navigation_color !== undefined &&
		UserSettings[0].navigation_color !== null
			? `Background-color: ${UserSettings[0].navigation_color}`
			: undefined}
	/>
	{#each Object.entries(DataSettings) as section, i}
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
						style="height: auto;"
						class="tableBorder w-full relative h-650-px bg-blueGray-700 mt-12 mb-12 flex flex-col p-6"
					>
						<div
							use:archiveTableSliderStyling
							style="right: -4px; bottom: -4px; cursor: ns-resize;"
							class="slider h-4 w-4 absolute rounded-full px-2"
						/>
						<div
							use:archiveTableSliderStyling
							style="left: -4px; bottom: -4px; cursor: ns-resize;"
							class="slider h-4 w-4 absolute rounded-full px-2"
						/>
						<div
							class="dataTableContainer w-full bg-white p-4 overflow-x-auto"
							style="height: auto;"
						>
							{#if i === 0}
								<table
									use:makeDataTableInitial
									class="archiveDataTable"
									id="archiveDataTable{i}"
								>
									<thead>
										<tr>
											{#each section[1].Table.Headers as header}
												<th>{header}</th>
											{/each}
										</tr>
									</thead>
									<tbody>
										{#if section[1].Table.Data[0] !== undefined}
											{#each section[1].Table.Data[0] as row}
												<tr>
													{#each Object.entries(row) as entry, entryNum}
														{#if section[1].Table.DBFieldNames.includes(entry[0])}
															{#if entryNum !== 0}
																<td
																	>{entry[1]}</td
																>
															{/if}
														{/if}
													{/each}
												</tr>
											{/each}
										{/if}
									</tbody>
								</table>
							{:else}
								<table
									class="archiveDataTable"
									id="archiveDataTable{i}"
								>
									<thead>
										<tr>
											{#each section[1].Table.Headers as header}
												<th>{header}</th>
											{/each}
										</tr>
									</thead>
									<tbody>
										{#if section[1].Table.Data[0] !== undefined}
											{#each section[1].Table.Data[0] as row}
												<tr>
													{#each Object.entries(row) as entry, entryNum}
														{#if section[1].Table.DBFieldNames.includes(entry[0])}
															{#if entryNum !== 0}
																<td
																	>{entry[1]}</td
																>
															{/if}
														{/if}
													{/each}
												</tr>
											{/each}
										{/if}
									</tbody>
								</table>
							{/if}
						</div>
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

<style>
	td {
		max-width: 14rem;
		/* max-width: 50ch; */
		white-space: nowrap;
		text-overflow: ellipsis;
		overflow: hidden;
	}
	.slider {
		background-color: rgb(251 113 133);
	}
</style>
