<script>
	import { dashboardSettingsEnable, DashboardSave } from "../../../scripts/DashboardDesigner/DashboardSettings.js";
	import { createText } from "../../../scripts/DashboardDesigner/CreateText.js";
	import { createChart } from "../../../scripts/DashboardDesigner/CreateChart.js";
	import { createImage } from "../../../scripts/DashboardDesigner/CreateImage.js";
	import { createTable } from "../../../scripts/DashboardDesigner/CreateTable.js";
	import { onDestroy } from "svelte";
	import { retrieveChartSettings } from "../../../scripts/DashboardDesigner/RetrieveChartSettings.js";

	let showActionBar = false;
	let parentOffset;
	let charts_in_dashboard = [];

	onDestroy(
		// Remove added dashboard properties from the HTML element on destruction
		function () {
			j$("html").css("overflow", "");
			j$("html").css("background-color", "");
		}
	);

	function loadChart(evt) {
		evt.preventDefault();
		evt.stopPropagation();
		j$("body").append(`
            <div id="temporary-background-gray" style="position: absolute; left: 0; top: ${j$("html").scrollTop()}px;
            z-index: 10000000000;
            width: 100vw;
            height: 100vh;
            background-color: rgb(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            ">
                <div id="chart-settings-container" 
                    style="width: 75%; min-width: 400px;" 
                    class="relative bg-white rounded shadow-lg p-4"
                >
                    <i id="DashboardSettingsCloseIcon" style="width: 10px; height: 10px;" 
                    class="fas fa-times absolute top-10 right-10 cursor-pointer"></i>
                    <h1 style="border-bottom: 4px solid black;" class="text-xl font-bold mb-4">Load Existing Chart</h1>
                    <form id="load-chart-container" class="flex" style="justify-content: center; height: auto; flex-wrap: wrap; max-height: 75vh; overflow: scroll;">
                    </form>
                </div>    
            </div>
        `);

		// Make the background have no scroll
		j$("body").css("overflow", "hidden");

		// Add event listener for closing the settings
		j$(`#chart-settings-container #DashboardSettingsCloseIcon`).click(function () {
			j$("#temporary-background-gray").fadeOut(400, "swing", function () {
				j$("body").css("overflow", "auto");
				j$(this).remove();
			});
		});
		// Add event listener for closing the settings
		j$("#temporary-background-gray").click(function (ev) {
			// Only close if we click on the background, and ignore clicks on the settings
			if (j$(ev.target).is(j$("#temporary-background-gray"))) {
				j$("#temporary-background-gray").fadeOut(400, "swing", function () {
					j$("body").css("overflow", "auto");
					j$(this).remove();
				});
			}
		});

		function displayChartsToPick(charts) {
			charts.forEach((chart) => {
				j$("#load-chart-container").append(`
				<div id="${chart["chart_id"]}" class="chart-to-load" 
					style="margin-right: 10px; min-width: 30%; margin: 10px; 
					height: 150px; display: flex; justify-content: center; align-items: center;
					position: relative; border-radius: 15px; border: 5px solid black;
					background-color: rgba(239, 68, 68, 0.5); cursor: pointer;"
				>
					<div class="delete-chart-button" 
						style="height: 30px; width: 30px; border-radius: 50%;
						background-color: white; border: 5px solid black; position: absolute; 
						top: -15px; right: -15px; cursor: pointer; display: flex;
						justify-content: center; align-items: center;
					">
						<i style="width: 10px; height: 10px; margin-bottom: 5px;" class="fas fa-times cursor-pointer"></i>
					</div>
					<h2 style="font-size: 1.5rem; padding: 10px 10px;" class="font-bold">${chart["title_text"]}</h2>
				</div>
				`);

				j$(`div#${chart["chart_id"]} div.delete-chart-button`).click(function (event) {
					event.stopPropagation();
					// Confirm they want to delete
					j$(`body`).append(`
					<div id="temp-background-gray" class="leave-window-button" style="position: absolute; left: 0; top: ${j$("html").scrollTop()}px;
						z-index: 10000000000;
						width: 100vw;
						height: 100vh;
						background-color: rgb(0, 0, 0, 0.5);
						display: flex;
						justify-content: center;
						align-items: center;
					">
						<div class="overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex" style="margin: 0px; left: 50%; bottom: 25%; transform: translate(-50%, -50%);">
							<div class="relative w-auto my-6 max-w-sm">
								<div class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
									<div class="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t">
										<h3 class="text-3xl font-semibold">Deletion</h3>
										<button class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"><span class="leave-window-button bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">×</span></button>
									</div>
									<div class="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
										<button class="leave-window-button text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">Close</button>
										<button class="confirm-delete-button bg-emerald-500 text-white active:bg-emerald-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">Confirm delete</button>
									</div>
								</div>
							</div>
						</div>
					</div>
					`);

					j$(".leave-window-button").click(function () {
						j$("#temp-background-gray").fadeOut(400, "swing", function () {
							j$(this).remove();
						});
					});

					j$("button.confirm-delete-button").click(function () {
						j$.ajax({
							type: "DELETE",
							data: JSON.stringify({ chart_id: chart["chart_id"] }),
							url: `/admin/delete-chart`,
							success: function (response) {
								if (response.toLowerCase() === "success") {
									j$(`div#${chart["chart_id"]}`).remove();
								}
							},
						});
					});
				});

				j$(`div#${chart["chart_id"]} div.delete-chart-button`).hover(
					function () {
						j$(this).css("background-color", "rgba(239, 68, 68, 1.0)");
					},
					function () {
						j$(this).css("background-color", "white");
					}
				);

				j$(`div#${chart["chart_id"]}`).hover(
					function (event) {
						// Only change the background if we hover over the div, not the delete button
						if (event.target === event.currentTarget) {
							j$(this).css("background-color", "rgba(239, 68, 68, 0.8)");
						}
					},
					function () {
						j$(this).css("background-color", "rgba(239, 68, 68, 0.5)");
					}
				);

				j$(`div#${chart["chart_id"]}`).click(function (event) {
					if (event.target !== event.currentTarget && event.target != j$(`#${chart["chart_id"]} h2`)[0]) return;
					// Remove the background
					j$("#temporary-background-gray").fadeOut(400, "swing", function () {
						j$("body").css("overflow", "auto");
						j$(this).remove();
						// Load the chart, deleting attributes we don't want
						delete chart["top"];
						delete chart["right"];
						delete chart["width"];
						delete chart["height"];
						let newChart = createChart({}, chart);
						// Return the chart
						charts_in_dashboard.push(newChart);
					});
				});
			});
		}

		// Get charts
		j$.ajax({
			type: "GET",
			url: "/admin/charts",
			success: function (data) {
				// Display charts to load
				displayChartsToPick(JSON.parse(data));
			},
			error: function (err) {
				console.log(err);
			},
		});
	}

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

		j$("#create-chart-button").click(function (event) {
			// Prevent default stops the browser from scrolling you to the top of page
			// Which we don't want so you don't have to scroll back down to the new chart
			event.preventDefault();
			let chart = createChart();
			charts_in_dashboard.push(chart);
		});

		j$("#dashboard-save-existing-button").click(function () {
			let oldDashboardHeight = j$("#DashboardDesignerContainer").height();
			DashboardSave();
			let newDashboardHeight = j$("#DashboardDesignerContainer").height();
			let data = {
				dashboard_title: j$("#dashboard-title").val(),
				dashboard_height: j$("#DashboardDesignerContainer")[0].style["height"],
				dashboard_id: j$("#DashboardDesignerContainer").attr("dashboard-id"),
				charts: [],
			};
			for (let chart of charts_in_dashboard) {
				// Resize the % height and % top of the chart so the actual pixel size doesn't change if the height of the dashboard is different
				j$(`#chart${chart.id}`).css({
					height: ((j$(`#chart${chart.id}`).height() - (newDashboardHeight - oldDashboardHeight) * (j$(`#chart${chart.id}`).height() / j$("#DashboardDesignerContainer").height())) / j$("#DashboardDesignerContainer").height()) * 100 + "%",
					top: (oldDashboardHeight / newDashboardHeight) * Number(j$(`#chart${chart.id}`)[0].style["top"].replace("%", "")) + "%",
				});

				try {
					let chart_settings = {
						height: j$(`#chart${chart.id}`)[0].style["height"],
						width: j$(`#chart${chart.id}`)[0].style["width"],
						top: j$(`#chart${chart.id}`)[0].style["top"],
						right: j$(`#chart${chart.id}`)[0].style["right"],
						data: retrieveChartSettings(chart, j$(`#chart${chart.id}`)),
					};
					data.charts.push(chart_settings);
				} catch {
					console.log("Error, likely due to chart being deleted");
				}
			}
			// Update the new data
			j$.ajax({
				type: "POST",
				url: `${location.origin}/admin/save-dashboard`,
				data: JSON.stringify(data),
				success: function () {
					console.log("Dashboard Successfully Saved");
				},
				error: function (e) {
					error = "Server Error During Creation.";
					// Error logging
					console.log(e.statusText);
					console.log(e.responseText);
				},
			});
		});
	} // onLoad() end

	const loadDashboard = function () {
		j$("body").append(`
            <div id="temporary-background-gray" style="position: absolute; left: 0; top: ${j$("html").scrollTop()}px;
            z-index: 10000000000;
            width: 100vw;
            height: 100vh;
            background-color: rgb(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            ">
                <div id="dashboard-settings-container" 
                    style="width: 75%; min-width: 400px;" 
                    class="relative bg-white rounded shadow-lg p-4"
                >
                    <i id="DashboardSettingsCloseIcon" style="width: 10px; height: 10px;" 
                    class="fas fa-times absolute top-10 right-10 cursor-pointer"></i>
                    <h1 style="border-bottom: 4px solid black;" class="text-xl font-bold mb-4">Load Existing Dashboard</h1>
                    <form id="load-dashboard-container" class="flex" style="justify-content: center; height: auto; flex-wrap: wrap; max-height: 75vh; overflow: scroll;">
                    </form>
                </div>    
            </div>
        `);

		// Disable scrolling
		j$("body").css("overflow", "hidden");

		// Add event listener for closing the settings
		j$(`#dashboard-settings-container #DashboardSettingsCloseIcon`).click(function () {
			j$("#temporary-background-gray").fadeOut(400, "swing", function () {
				j$("body").css("overflow", "auto");
				j$(this).remove();
			});
		});
		// Add event listener for closing the settings
		j$("#temporary-background-gray").click(function (ev) {
			// Only close if we click on the background, and ignore clicks on the settings
			if (j$(ev.target).is(j$("#temporary-background-gray"))) {
				j$("#temporary-background-gray").fadeOut(400, "swing", function () {
					j$("body").css("overflow", "auto");
					j$(this).remove();
				});
			}
		});

		function displayDashboardsToPick(dashboards) {
			dashboards.forEach((dashboard) => {
				j$("#load-dashboard-container").append(`
					<div id="${dashboard["_id"]["$oid"]}" class="dashboard-to-load" 
						style="margin-right: 10px; min-width: 30%; margin: 10px; height: 150px; display: flex; justify-content: center; align-items: center;
						border-radius: 15px; border: 5px solid black;
						background-color: rgba(239, 68, 68, 0.5);
						cursor: pointer; position: relative;"
					>
						<div class="delete-dashboard-button" 
							style="height: 30px; width: 30px; border-radius: 50%;
							background-color: white; border: 5px solid black; position: absolute; 
							top: -15px; right: -15px; cursor: pointer; display: flex;
							justify-content: center; align-items: center;
						">
							<i style="width: 10px; height: 10px; margin-bottom: 5px;" class="fas fa-times cursor-pointer"></i>
						</div>
						<h2 style="font-size: 1.5rem; padding: 10px 10px;" class="font-bold">${dashboard["dashboard_title"]}</h2>
						
					</div>
				`);

				j$(`div#${dashboard["_id"]["$oid"]} div.delete-dashboard-button`).click(function (event) {
					event.stopPropagation();
					// Confirm they want to delete
					j$(`body`).append(`
					<div id="temp-background-gray" class="leave-window-button" style="position: absolute; left: 0; top: ${j$("html").scrollTop()}px;
						z-index: 10000000000;
						width: 100vw;
						height: 100vh;
						background-color: rgb(0, 0, 0, 0.5);
						display: flex;
						justify-content: center;
						align-items: center;
					">
						<div class="overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none justify-center items-center flex" style="margin: 0px; left: 50%; bottom: 25%; transform: translate(-50%, -50%);">
							<div class="relative w-auto my-6 max-w-sm">
								<div class="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
									<div class="flex items-start justify-between p-5 border-b border-solid border-blueGray-200 rounded-t">
										<h3 class="text-3xl font-semibold">Deletion</h3>
										<button class="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"><span class="leave-window-button bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">×</span></button>
									</div>
									<div class="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
										<button class="leave-window-button text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">Close</button>
										<button class="confirm-delete-button bg-emerald-500 text-white active:bg-emerald-600 font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150" type="button">Confirm delete</button>
									</div>
								</div>
							</div>
						</div>
					</div>
					`);

					j$(".leave-window-button").click(function () {
						j$("#temp-background-gray").fadeOut(400, "swing", function () {
							j$(this).remove();
						});
					});

					j$("button.confirm-delete-button").click(function () {
						j$.ajax({
							type: "DELETE",
							data: JSON.stringify({ dashboard_id: dashboard["_id"]["$oid"] }),
							url: `/admin/delete-dashboard`,
							success: function (response) {
								if (response.toLowerCase() === "success") {
									j$(`div#${dashboard["_id"]["$oid"]}`).remove();
								}
							},
						});
					});
				});

				j$(`div#${dashboard["_id"]["$oid"]} div.delete-dashboard-button`).hover(
					function () {
						j$(this).css("background-color", "rgba(239, 68, 68, 1.0)");
					},
					function () {
						j$(this).css("background-color", "white");
					}
				);

				j$(`div#${dashboard["_id"]["$oid"]}`).hover(
					function () {
						j$(this).css("background-color", "rgba(239, 68, 68, 0.8)");
					},
					function () {
						j$(this).css("background-color", "rgba(239, 68, 68, 0.5)");
					}
				);

				j$(`div#${dashboard["_id"]["$oid"]}`).click(function () {
					// Remove the background
					j$("#temporary-background-gray").fadeOut(400, "swing", function () {
						j$("body").css("overflow", "auto");
						// We are loading a new dashboard so we want to empty all the old ones out
						charts_in_dashboard = [];
						j$(this).remove();
						// Remove existing charts
						j$("#DashboardDesignerContainer div.chart").remove();
						// Set data for dashboard
						j$("input#dashboard-title").val(dashboard["dashboard_title"]);
						j$("input#dashboard-height").val(dashboard["dashboard_height"].replace("vh", ""));
						j$("#DashboardDesignerContainer").css("height", dashboard["dashboard_height"]);
						// Get the data for the dashboard's charts
						j$.ajax({
							type: "GET",
							url: `/admin/charts/get_charts_by_dashboard_id/${dashboard["_id"]["$oid"]}`,
							success: function (data) {
								// Remove the chart creation hint
								j$("center#chart-creation-hint").remove();
								// Set the dashboard ID
								j$("div#DashboardDesignerContainer").attr("dashboard-id", dashboard["_id"]["$oid"]);
								// Display dashboards to load
								const charts = JSON.parse(data);
								charts.forEach((chart) => {
									// Add chart to the dashboard
									let data = {
										// ID
										chart_id: chart.chart_id,
										// Background color
										background_color: chart.background_color,
										// Chart type
										chart_type: chart.chart_type,
										// Chart legend
										legend_enabled: chart.legend_enabled,
										// Scale labels
										yaxes_scale_label: chart.yaxes_scale_label,
										xaxes_scale_label: chart.xaxes_scale_label,
										// Scale labels enabled
										xaxes_scale_label_enabled: chart.xaxes_scale_label_enabled,
										yaxes_scale_label_enabled: chart.yaxes_scale_label_enabled,
										// Grid color
										xaxes_gridlines_color: chart.xaxes_gridlines_color,
										yaxes_gridlines_color: chart.yaxes_gridlines_color,
										// Scale label color
										yaxes_scalelabel_color: chart.yaxes_scalelabel_color,
										xaxes_scalelabel_color: chart.xaxes_scalelabel_color,
										// Legend font color
										legend_font_color: chart.legend_font_color,
										// Ticks font color
										xaxes_tick_color: chart.xaxes_tick_color,
										yaxes_tick_color: chart.yaxes_tick_color,
										// Grid enabled
										yaxes_gridline_enabled: chart.yaxes_gridline_enabled,
										xaxes_gridline_enabled: chart.xaxes_gridline_enabled,
										// Chart tite configuration
										title_fontsize: Number(chart.title_fontsize),
										title_fontcolor: chart.title_fontcolor,
										title_text: chart.title_text,
										title_enabled: chart.title_enabled,
										// Default font family
										default_font_family: chart.default_font_family,
										// Chart padding
										chart_padding: chart.chart_padding,
										width: chart.width,
										height: chart.height,
										top: chart.top,
										right: chart.right,
									};
									let result = createChart({}, data);
									// Add chart to the dashboard
									charts_in_dashboard.push(result);
								});
							},
						});
					});
				});
			});
		}

		// Get dashboards
		j$.ajax({
			type: "GET",
			url: "/admin/dashboards/get_all_dashboards",
			success: function (data) {
				// Display dashboards to load
				displayDashboardsToPick(JSON.parse(data));
			},
			error: function (err) {
				console.log(err);
			},
		});
	};
	let randomDashboardTitles = ["Dashboard Extreme", "The Arch Dashboard", "Dashboard of the Gods", "Dashboard of the Future", "Dashboard of the Past", "Dashboard of the Present", "The Universal Dashboard", "The Dashboard of the Demystified", "The Dashboard of the Unseen", "The Dashboard of the Unknown"];
</script>

<div use:onLoad style="height: 100vh;" dashboard-id="" id="DashboardDesignerContainer" class="h-screen w-screen border-solid border-blueGray-100 border-r border-b">
	<center id="chart-creation-hint" style="font-size: 1.2rem; font-weight: bold;">Right Click to Create Chart</center>
	<div class="shadow-xl bg-white w-full flex flex-column justify-between items-center px-4" id="DashboardSettingsContainer">
		<form style="height: 80%; display: flex; flex-direction: column;">
			<div class="w-full">
				<label class="text-s uppercase py-3 font-bold block text-blueGray-700" for="dashboard-title">Dashboard Title</label>
				<input style="height: 30px;" class="picker-input w-full" id="dashboard-title" type="text" value={randomDashboardTitles[Math.floor(Math.random() * 10)]} name="dashboard_title" />
			</div>
			<div class="w-full" style="">
				<label class="text-s uppercase py-3 font-bold block text-blueGray-700" for="dashboard-height"> Dashboard Height (% Screenheight) </label>
				<div class="relative input-icon-container">
					<input style="height: 30px;" class="picker-input w-full" id="dashboard-height" type="number" value="100" name="dashboard_height" />
					<span class="absolute">%</span>
				</div>
			</div>
			<div class="w-full" style="align-self: flex-end;height: 100%;order: 1;display: flex;justify-content: flex-end;flex-direction: column;">
				<input id="dashboard-save-new-button" style="height: 30px;" class="my-4 picker-input w-full cursor-pointer placeholder-blueGray-300 text-blueGray-600 hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring ease-linear transition-all duration-150" type="button" value="Save as New Dashboard" name="submit" />
				<input id="dashboard-save-existing-button" style="height: 30px;" class="picker-input w-full cursor-pointer placeholder-blueGray-300 text-blueGray-600 hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring ease-linear transition-all duration-150" type="button" value="Save Existing Dashboard" name="submit" />
			</div>
		</form>
		<hr class="my-4 md:min-w-full" />
		<div style="height: 20%; width: 100%; display: flex; justify-content: flex-end; flex-direction: column;">
			<input on:click={loadDashboard} id="dashboard-load-button" style="height: 30px; margin-bottom: 20px;" class="picker-input w-full cursor-pointer placeholder-blueGray-300 text-blueGray-600 hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring ease-linear transition-all duration-150" type="submit" value="Load Dashboard" name="submit" />
		</div>
	</div>
	<div on:click={dashboardSettingsEnable} class="dashboard-settings-triangle cursor-pointer" />
	<div id="DashboardDesignerActionBar" style="background-color: rgb(239, 68, 68, 0.85);" class="absolute text-base z-50 float-left py-2 list-none text-left rounded shadow-lg mt-1 min-w-48 {showActionBar ? 'block' : 'hidden'}">
		<a id="create-chart-button" href="#" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Chart </a>
		<!-- Load an existing chart instead of creating a new one -->
		<a on:click={loadChart} id="load-chart-button" href="#" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Load Chart </a>
		<div class="h-0 my-2 border border-solid border-t-0 border-blueGray-800 opacity-25" />
		<a on:click={createText} href="#" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Text </a>
		<a on:click={createImage} href="#" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Image </a>
		<a on:click={createTable} href="#" class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"> Create Table </a>
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
		width: 300px;
		height: 100vh;
		background-color: rgb(255, 255, 255, 0.9);
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
