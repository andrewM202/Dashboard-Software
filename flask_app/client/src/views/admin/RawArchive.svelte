<script>
	// core components
	import AdminNavbar from "components/Navbars/AdminNavbar.svelte";
	import HeaderStats from "components/Headers/HeaderStats.svelte";
	import DataCreationCard from "components/Cards/DataCreationCard.svelte";
	import SettingsBar from "components/Headers/SettingsBar.svelte";
	import { dataSettingsStore, userSettingsStore } from "../../stores.js";
	import { newTableEntry } from "../../../scripts/RawArchive/NewTableEntry.js";
	import { loadSettingsEvent } from "../../../scripts/RawArchive/CollectionWideSettings.js";

	// Popover Stuff Start
	import { createPopper } from "@popperjs/core";
	import { onMount, tick } from "svelte";

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
		let data = j$(formSelector).serialize();
		// Clear form
		j$(formSelector).trigger("reset");
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

	// This function is called every time the openTab variable is changed,
	// to see if we need to generate the datatable for this tab
	// because we only want to load the datatable when its visible. This also
	// allows the overflow popovers to generate correctly because if the element is hidden
	// it will never generate the overflow popover otherwise
	function makeDataTable(evt) {
		let table;

		if (!j$.fn.dataTable.isDataTable(`#${j$(evt)[0].id}`)) {
			let tempInterval = setInterval(function () {
				if (j$(`#${j$(evt)[0].id}`).is(":visible")) {
					clearInterval(tempInterval);
					j$(
						j$(`#${j$(evt)[0].id}`)
							.parentsUntil(".tableBorder")
							.parent()[0]
					).css({
						height: j$(
							j$(`#${j$(evt)[0].id}`)
								.parentsUntil(".tableBorder")
								.parent()[0]
						).innerHeight(),
					});
				}
			}, 10);
			// Initialize datatable if its not already initialized
			if (!j$.fn.dataTable.isDataTable(`#${j$(evt)[0].id}`)) {
				table = new DataTable(`#${j$(evt)[0].id}`, {
					dom: "QBlfrtip",
					buttons: [
						{
							text: "New",
							className: "newButton cursor-pointer",
							action: function (e, dt, node, config) {
								newTableEntry(e);
								console.log(
									table.rows({ selected: true }).data()
								);
								// These db field names match up with the data in table.rows().data()
								let tableHeaders =
									Object.entries(DataSettings)[
										j$(evt)[0].id.split(
											"archiveDataTable"
										)[1]
									][1].Table.Headers;
								let dbFieldNames =
									Object.entries(DataSettings)[
										j$(evt)[0].id.split(
											"archiveDataTable"
										)[1]
									][1].Table.DBFieldNames;
								console.log(dbFieldNames);
								console.log(tableHeaders);
							},
						},
						{
							text: "Edit",
							className: "editButton cursor-pointer",
							action: function (e, dt, node, config) {},
						},
						{
							text: "Delete",
							className: "deleteButton cursor-pointer",
							action: function (e, dt, node, config) {},
						},
						{
							text: "Select All",
							className: "cursor-pointer",
							action: function (e, dt, node, config) {
								if (
									table.rows({ search: "applied" }).data()
										.length ===
									table.rows(".selected").data().length
								) {
									table.rows().deselect();
								} else {
									table.rows({ search: "applied" }).select();
								}
							},
						},
						{
							extend: "copy",
							text: "Copy",
							className: "cursor-pointer downloadButton",
						},
						{
							extend: "csv",
							text: "Csv",
							className: "cursor-pointer downloadButton",
						},
						{
							extend: "excel",
							text: "Excel",
							className: "cursor-pointer downloadButton",
						},
						{
							extend: "pdf",
							text: "Pdf",
							className: "cursor-pointer downloadButton",
						},
						{
							extend: "print",
							text: "Print",
							className: "cursor-pointer downloadButton",
						},
						{
							// Button to download as JSON
							text: "Json",
							className: "cursor-pointer downloadButton",
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
								// If the user hits the fullscreen button a second
								// time, it will go out of fullscreen
								if (document.webkitIsFullScreen) {
									document.webkitExitFullscreen();
								} else if (document.mozFullScreen) {
									document.exitFullscreen();
								} else if (document.msFullscreenElement) {
									document.msExitFullscreen();
								}
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
					keys: true,
					select: {
						style: "multi",
					},
					aaSorting: [], // This allows by default no sorting, but can still click on header to sort
					// initComplete called once in table lifespan when its created
					initComplete: function () {
						// Make the page number of results (i.e. 10 results per page)
						// be 75px wide so the icon does not go over the number
						j$(".dataTables_length select").css("width", "75px");
						// Detect cell overflow for each table entry
						// now that we have completed creating the datatable
						for (let event of j$(`#${j$(evt)[0].id} td`)) {
							detectCellOverflow(event);
						}
						// Add an x-overflow so that the table itself can scroll,
						// but not the header or footer
						j$(`#${j$(evt)[0].id}`).wrap(
							"<div class='x-overflow-auto' style='max-width: 100%; width: 100%; overflow-x: auto;'></div>"
						);
					},
					drawCallback: function () {
						// Make the page number of results (i.e. 10 results per page)
						// be 75px wide so the icon does not go over the number
						j$(".dataTables_length select").css("width", "75px");
						// Detect cell overflow for each table entry
						// now that we have completed creating the datatable
						for (let event of j$(`#${j$(evt)[0].id} td`)) {
							detectCellOverflow(event);
						}
						j$(".deleteButton").css({
							"background-color": "rgb(251 113 133)", // Red
						});
						j$(".editButton").css({
							"background-color": "#FFE15D", // Yellow
						});
						j$(".newButton").css({
							"background-color": "#ADE792", // Green
						});
						j$(".downloadButton").css({
							"background-color": "rgb(199 210 254)", // Indigo
						});
					},
				});
				// Event listener to see which header is clicked
				j$(`#${j$(evt)[0].id} thead`).on("click", "th", function () {
					let index = table.column(this).index();
					console.log(index);
				});
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

	// Bind openTab to AdminNavbar component
	let openTab = 0;
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
		{#if openTab == i}
			<!-- <div
			class={navItems[openTab] === section[0] ? "block" : "hidden"}
			id="TableHiddenBlockContainer"
		> -->
			<div id="TableHiddenBlockContainer">
				<HeaderStats
					id={section[0]}
					cards={section[1].Cards}
					title={navItems[openTab]}
					titleFontSize={"text-4xl"}
					inputs={section[1].HeaderSearchInputs}
					CollectionName={section[1].CollectionName}
					SearchFunction={SearchResults}
					headerBGColor={UserSettings[0].archive_header_color !==
						undefined &&
					UserSettings[0].archive_header_color !== null
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
								class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
							/>
							<div
								use:archiveTableSliderStyling
								style="left: -4px; bottom: -4px; cursor: ns-resize;"
								class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
							/>
							<div
								class="dataTableContainer w-full bg-white p-4"
								style="height: auto; overflow-y: scroll;"
							>
								<table
									use:makeDataTable
									class="archiveDataTable"
									id="archiveDataTable{i}"
									collectionName={section[1].collectionName}
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
									UserSettings[0].archive_creation_color !==
										null
										? `Background-color: ${UserSettings[0].archive_creation_color}`
										: undefined}
								/>
							{/if}
						</div>
					</div>
				</div>
			</div>
		{/if}
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
</style>
