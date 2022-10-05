<script>
    import Chart from "chart.js";

    let showActionBar = false;
    let parentOffset;
    let chartsCreated = 0;
    let textCreated = 0;

    // onLoad contains event listeners needing to be attached
    // when #DashboardDesignerContainer is loaded
    function onLoad() {
        j$("#DashboardDesignerContainer").on(
            "contextmenu rightclick",
            function (event) {
                event.preventDefault();
                // Right mouse click
                if (event.which === 3) {
                    // Make the action bar appear at mouse click
                    showActionBar = true;
                    parentOffset = j$(this).parent().offset();
                    j$(
                        "#DashboardDesignerContainer > #DashboardDesignerActionBar"
                    ).css({
                        top: event.pageY - parentOffset.top + "px",
                        right: j$(window).width() - event.pageX + "px",
                    });
                }
            }
        );
        // Make the action bar disappear when left clicking
        j$("#DashboardDesignerContainer").on("click", function () {
            showActionBar = false;
        });
    } // onLoad() end

    // Event listener for creating a chart
    function createChart(event) {
        // Create a div where clicked
        j$("#DashboardDesignerContainer").append(
            `<div id="chart${chartsCreated}" style="top: ${j$(
                "#DashboardDesignerContainer > #DashboardDesignerActionBar"
            ).css("top")}; right: ${
                parseInt(
                    j$(
                        "#DashboardDesignerContainer > #DashboardDesignerActionBar"
                    ).css("right")
                ) - 500
            }px; width: 500px; height: 500px;" class="absolute bg-blueGray-700 text-white">
                <div class="chart-icon-container flex justify-between">
                    <i style="padding-left: 7px; padding-top: 7px;" class="fa fa-bars cursor-pointer chart-mover" aria-hidden="true"></i>
                    <i style="padding-right: 7px; padding-top: 7px;" class="fa fa-cog cursor-pointer chart-settings" aria-hidden="true"></i>
                </div>
                <h1 class="text-4xl text-white text-center">Chart Title</h1>
                <div
                    style="right: -4px; bottom: -4px; cursor: move;"
                    class="resizer bg-rose-400 h-4 w-4 absolute rounded-full px-2"
                ></div>
                <div
                    style="left: -4px; bottom: -4px; cursor: move;"
                    class="resizer bg-rose-400 h-4 w-4 absolute rounded-full px-2"
                ></div>
                <div class="p-4" style="height: calc(100% - 83px)">
                    <canvas id="bar-chart" />
                </div>
            </div>`
        );

        // Initialize a new chart.js chart
        let xValues = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000];

        new Chart(
            document
                .querySelector(`#chart${chartsCreated} canvas#bar-chart`)
                .getContext("2d"),
            {
                type: "line",
                data: {
                    labels: xValues,
                    datasets: [
                        {
                            data: [
                                860, 1140, 1060, 1060, 1070, 1110, 1330, 2210,
                                7830, 2478,
                            ],
                            borderColor: "red",
                            fill: false,
                        },
                        {
                            data: [
                                1600, 1700, 1700, 1900, 2000, 2700, 4000, 5000,
                                6000, 7000,
                            ],
                            borderColor: "green",
                            fill: false,
                        },
                        {
                            data: [
                                300, 700, 2000, 5000, 6000, 4000, 2000, 1000,
                                200, 100,
                            ],
                            borderColor: "blue",
                            fill: false,
                        },
                    ],
                },
                options: {
                    legend: { display: false },
                    maintainAspectRatio: false,
                    responsive: true,
                    scales: {
                        xAxes: [
                            {
                                ticks: {
                                    fontColor: "rgba(255,255,255,.7)",
                                },
                                scaleLabel: {
                                    display: false,
                                    labelString: "Month",
                                    fontColor: "white",
                                },
                            },
                        ],
                        yAxes: [
                            {
                                ticks: {
                                    fontColor: "rgba(255,255,255,.7)",
                                },
                                scaleLabel: {
                                    display: false,
                                    labelString: "Month",
                                    fontColor: "white",
                                },
                            },
                        ],
                    },
                },
            }
        );

        let chartsNumber = chartsCreated;

        // Add event listeners to resizers, so we can resize
        // the chart
        let parent = j$(`#chart${chartsCreated}`);
        let minParentHeight = 250;
        let minParentWidth = 250;
        j$(`#chart${chartsCreated} div.resizer`).mousedown(function (downEv) {
            downEv.preventDefault();
            j$(window).mousemove(function (moveEv) {
                let initialPosY = j$(downEv.target).offset().top;
                let movePosY = moveEv.pageY;
                let addHeight = movePosY - initialPosY;

                let initialPosX = j$(downEv.target).offset().left;
                let movePosX = moveEv.pageX;
                let addWidth = movePosX - initialPosX;

                j$("body").css("cursor", "move");

                console.log("Parent innerWidth: " + j$(parent).innerWidth());

                // Add the difference in width to the parent element
                if (j$(parent).innerWidth() >= minParentHeight) {
                    if (j$(parent).innerWidth() + addWidth < minParentWidth) {
                        j$(parent).innerWidth(minParentWidth);
                    } else {
                        j$(parent).innerWidth(
                            j$(parent).innerWidth() + addWidth
                        );
                        j$(parent).css(
                            "right",
                            parseInt(j$(parent).css("right")) - addWidth
                        );
                    }
                }

                // Add the difference in height to the parent element
                if (j$(parent).innerHeight() >= minParentHeight) {
                    if (
                        j$(parent).innerHeight() + addHeight <
                        minParentHeight
                    ) {
                        j$(parent).innerHeight(minParentHeight);
                    } else {
                        j$(parent).innerHeight(
                            j$(parent).innerHeight() + addHeight
                        );
                    }

                    // Resize parent element too if the resizer makes it go
                    // out of bounds
                    if (
                        j$("#DashboardDesignerContainer").height() <
                        j$(parent).height() + j$(parent).offset().top
                    ) {
                        j$("#DashboardDesignerContainer").height(
                            j$(parent).height() + j$(parent).offset().top
                        );
                    }
                }
            });
            j$(window).mouseup(function () {
                j$(window).unbind("mousemove");
                j$("body").css("cursor", "");
            });
        });
        j$(window).width();
        // Event listener for moving the chart around
        j$(`#chart${chartsNumber} i.chart-mover`).mousedown(function (downEv) {
            j$(window).mousemove(function (moveEv) {
                j$(parent).css({
                    top: moveEv.pageY - parentOffset.top + "px",
                    right:
                        j$(window).width() -
                        moveEv.pageX -
                        j$(`#chart${chartsNumber}`).width() +
                        "px",
                });
            });
            j$(window).mouseup(function () {
                j$(window).unbind("mousemove");
            });
        });

        // Chart settings part 1. Append the settings cog to the chart so we can
        // have a settings menu for the chart
        j$(`#chart${chartsNumber} i.chart-settings`).append(`
            <div
                id="ChartActionBar"
                class="hidden absolute bg-orange-500 text-base z-50 float-left py-2 list-none text-left rounded shadow-lg mt-1 min-w-48"
                style="left: ${j$(`#chart${chartsNumber}`).width() - 200}px;"
            >
                <a
                    href="#pablo"
                    class="change-settings-button text-xl py-1 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
                >
                    Chart Settings
                </a>
                <a
                    href="#pablo"
                    class="delete-chart-button text-xl py-1 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
                >
                    Delete Chart
                </a>
            </div>
            `);
        j$(
            `#chart${chartsNumber} i.chart-settings #ChartActionBar a.change-settings-button`
        ).click(function () {
            j$("body").append(`
                <div id="temporary-background-gray" style="position: absolute; left: 0; top: 0;
                z-index: 10000000000;
                width: ${j$("body").width()}px;
                height: ${j$("body").height()}px;
                background-color: rgb(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                ">
                    <div id="chart-settings-container" class="relative bg-white rounded shadow-lg p-4">
                        <i id="DashboardSettingsCloseIcon" style="width: 10px; height: 10px;" 
                        class="fas fa-times absolute top-10 right-10 cursor-pointer"></i>
                        <h1 class="text-xl font-bold mb-4">Chart Settings</h1>
                        <div class="flex justify-between">
                            <div class="w-1/2">
                                <label class="block text-sm font-bold mb-2" for="text-color">
                                    Chart Background Color
                                </label>
                                <input
                                    style="height: 30px; margin-right: 10px;"
                                    class="picker-input w-full"
                                    id="text-color"
                                    type="color"
                                    value="#000000"
                                />
                            </div>
                            <div class="w-1/2">
                                <label style="margin-left: 10px;" class="block text-sm font-bold mb-2" for="text-size">
                                    Chart Text Size
                                </label>
                                <input
                                    style="height: 30px; margin-left: 10px;"
                                    class="picker-input w-full"
                                    id="text-size"
                                    type="number"
                                    value="1.6rem"
                                />
                            </div>
                        </div>
                        <div class="flex justify-between">
                            <div class="w-1/2">
                                <label class="block text-sm font-bold mb-2" for="text-font">
                                    Chart Text Font
                                </label>
                                <select
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
                        </div>
                    </div>    
                </div>
            `);

            // Add event listener for closing the settings
            j$(`#chart-settings-container #DashboardSettingsCloseIcon`).click(
                function () {
                    j$("#temporary-background-gray").remove();
                }
            );
        });

        // Event listener for chart settings part 2. This event listener
        // toggles the chart settings menu when the user clicks on the
        // chart settings icon.
        j$(`#chart${chartsCreated} i.chart-settings`).click(function () {
            // Adjust the left attribute of the chart settings menu
            // incase the chart has beeen resized, so it still shows up
            // at the right location under the settings cog icon
            j$(`#chart${chartsNumber} i.chart-settings #ChartActionBar`).css({
                left: j$(`#chart${chartsNumber}`).width() - 200,
            });
            // Toggle the hide/show attribute of the chart settings menu
            j$(
                `#chart${chartsNumber} i.chart-settings #ChartActionBar`
            ).toggle();
        });

        // Event listener for chart settings part 3. This event listener
        // disables the Chart Action Bar if anyone clicks outside of the
        // settings cog
        j$("#DashboardDesignerContainer").click(function (event) {
            // If the target is not the settings cog icon itself
            // we want to hide the settings menu
            if (
                event.target != j$(`#chart${chartsNumber} i.chart-settings`)[0]
            ) {
                j$(
                    `#chart${chartsNumber} i.chart-settings #ChartActionBar`
                ).hide();
            }
        });

        // Event listener for deleting a chart from click the delete
        // settings menu item
        j$(
            `#chart${chartsNumber} i.chart-settings #ChartActionBar .delete-chart-button`
        ).click(function (event) {
            j$(event.target)
                .parent()
                .parent()
                .parent()
                .parent(`#chart${chartsNumber}`)
                .remove();
        });

        // Resize the dashboard chart container if the new chart we are creating
        // goes outside of the dashboard chart container
        if (
            j$("#DashboardDesignerContainer").height() <
            j$(`#chart${chartsCreated}`).height() +
                j$(`#chart${chartsCreated}`).offset().top
        ) {
            j$("#DashboardDesignerContainer").height(
                j$(`#chart${chartsCreated}`).height() +
                    j$(`#chart${chartsCreated}`).offset().top
            );
        }

        // Increment the chartsCreated variable now that a new chart is created
        chartsCreated++;
    } // createChart() end

    // Function for creating text
    function createText(event) {
        // Create a text node where clicked
        j$("#DashboardDesignerContainer").append(`
            <div id="text${textCreated}" style="top: ${j$(
            "#DashboardDesignerContainer > #DashboardDesignerActionBar"
        ).css("top")}; right: ${j$(
            "#DashboardDesignerContainer > #DashboardDesignerActionBar"
        ).css("right")};
        z-index: 10;"
        class="absolute"
        ">
                <div class="chart-icon-container flex justify-between">
                    <i style="padding-left: 7px; padding-top: 7px;" class="fa fa-bars cursor-pointer text-mover" aria-hidden="true"></i>
                    <i style="padding-right: 7px; padding-top: 7px;" class="fa fa-cog cursor-pointer text-settings" aria-hidden="true"></i>
                </div>
                <h1 style="font-size: 1.6rem;"
                class="relative"
                >Text
                </h1>
            </div>`);

        // Event listener for moving the text around
        let textCreatedNumber = textCreated;
        j$(`#text${textCreatedNumber} i.text-mover`).mousedown(function (
            downEv
        ) {
            j$(window).mousemove(function (moveEv) {
                j$(`#text${textCreatedNumber}`).css({
                    top: moveEv.pageY - parentOffset.top + "px",
                    // left: moveEv.pageX - parentOffset.left + "px",
                    right:
                        j$(window).width() -
                        moveEv.pageX -
                        j$(`#text${textCreatedNumber}`).width() +
                        "px",
                });
            });
            j$(window).mouseup(function () {
                j$(window).unbind("mousemove");
            });
        });

        // Event listener for changing the title of the h1 tag
        j$(`#text${textCreatedNumber} h1`).dblclick(function () {
            // Get the text/title of the h1
            let h1Text = j$(`#text${textCreatedNumber} h1`).text().trim();
            // Add an input to change the h1's text
            j$(`#text${textCreatedNumber}`).append(`
                <input type="text" value="${h1Text}" style="width: ${j$(`#text${textCreatedNumber}`).width() + 50}px;">
            `);

            // Make the h1 tag invisible while editing
            j$(`#text${textCreatedNumber} h1`).toggle();

            j$(window).keyup(function (event) {
                console.log("test");
                // If they press the return button
                if (event.key === "Enter") {
                    // If there is actual text in the input
                    if (j$(`#text${textCreatedNumber} input`).val() !== "") {
                        // Put the h1 tag with the input's text
                        j$(`#text${textCreatedNumber} h1`).text(
                            j$(`#text${textCreatedNumber} input`).val()
                        );
                        j$(`#text${textCreatedNumber} h1`).toggle();
                        j$(`#text${textCreatedNumber} input`).remove();

                        // Remove this event listener now that editing is done
                        j$(window).unbind("keyup");
                    }
                }
            });
        });

        // Chart settings part 1. Append the settings cog to the chart so we can
        // have a settings menu for the chart
        j$(`#text${textCreatedNumber} i.text-settings`).append(`
            <div
                id="TextActionBar"
                class="hidden absolute bg-orange-500 text-base z-50 float-left py-2 list-none text-left rounded shadow-lg mt-1 min-w-48"
                style="left: ${
                    j$(`#text${textCreatedNumber}`).width() - 200
                }px;"
            >
                <a
                    href="#pablo"
                    class="text-settings-button text-xl py-1 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
                >
                    Text Settings
                </a>
                <a
                    href="#pablo"
                    class="delete-text-button text-xl py-1 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
                >
                    Delete Text
                </a>
            </div>
            `);

        j$(
            `#text${textCreatedNumber} i.text-settings #TextActionBar a.text-settings-button`
        ).click(function () {
            j$("body").append(`
                <div id="temporary-background-gray" style="position: absolute; left: 0; top: 0;
                z-index: 10000000000;
                width: ${j$("body").width()}px;
                height: ${j$("body").height()}px;
                background-color: rgb(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                ">
                    <div id="text-settings-container" class="relative bg-white rounded shadow-lg p-4">
                        <i id="DashboardSettingsCloseIcon" style="width: 10px; height: 10px;" 
                        class="fas fa-times absolute top-10 right-10 cursor-pointer"></i>
                        <h1 class="text-xl font-bold mb-4">Text Settings</h1>
                        <div class="flex justify-between">
                            <div class="w-1/2">
                                <label class="block text-sm font-bold mb-2" for="text-color">
                                    Text Color
                                </label>
                                <input
                                    style="height: 30px; margin-right: 10px;"
                                    class="picker-input w-full"
                                    id="text-color"
                                    type="color"
                                    value="#000000"
                                />
                            </div>
                            <div class="w-1/2">
                                <label style="margin-left: 10px;" class="block text-sm font-bold mb-2" for="text-size">
                                    Text Size
                                </label>
                                <input
                                    style="height: 30px; margin-left: 10px;"
                                    class="picker-input w-full"
                                    id="text-size"
                                    type="number"
                                    value="1.6rem"
                                />
                            </div>
                        </div>
                        <div class="flex justify-between">
                            <div class="w-1/2">
                                <label class="block text-sm font-bold mb-2" for="text-font">
                                    Text Font
                                </label>
                                <select
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
                        </div>
                    </div>    
                </div>
            `);

            // Add event listener for closing the settings
            j$(`#text-settings-container #DashboardSettingsCloseIcon`).click(
                function () {
                    j$("#temporary-background-gray").remove();
                }
            );
        });

        // Event listener for chart settings part 2. This event listener
        // toggles the chart settings menu when the user clicks on the
        // chart settings icon.
        j$(`#text${textCreatedNumber} i.text-settings`).click(function () {
            // Adjust the left attribute of the chart settings menu
            // incase the chart has beeen resized, so it still shows up
            // at the right location under the settings cog icon
            j$(`#text${textCreatedNumber} i.text-settings #TextActionBar`).css({
                left: j$(`#text${textCreatedNumber}`).width() - 200,
            });
            // Toggle the hide/show attribute of the chart settings menu
            j$(
                `#text${textCreatedNumber} i.text-settings #TextActionBar`
            ).toggle();
        });

        // Event listener for chart settings part 3. This event listener
        // disables the Chart Action Bar if anyone clicks outside of the
        // settings cog
        j$("#DashboardDesignerContainer").click(function (event) {
            // If the target is not the settings cog icon itself
            // we want to hide the settings menu
            if (
                event.target !=
                j$(`#text${textCreatedNumber} i.text-settings`)[0]
            ) {
                j$(
                    `#text${textCreatedNumber} i.text-settings #TextActionBar`
                ).hide();
            }
        });

        // Event listener for deleting a chart from click the delete
        // settings menu item
        j$(
            `#text${textCreatedNumber} i.text-settings #TextActionBar .delete-text-button`
        ).click(function (event) {
            j$(event.target)
                .parent()
                .parent()
                .parent()
                .parent(`#text${textCreatedNumber}`)
                .remove();
        });

        textCreated++;
    } // createText() end
</script>

<div
    use:onLoad
    id="DashboardDesignerContainer"
    class="h-auto min-h-screen w-screen border-solid border-blueGray-100 border-r border-b"
>
    <div
        id="DashboardDesignerActionBar"
        class="absolute bg-orange-500 text-base z-50 float-left py-2 list-none text-left rounded shadow-lg mt-1 min-w-48 {showActionBar
            ? 'block'
            : 'hidden'}"
    >
        <a
            on:click={createChart}
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Create Chart
        </a>
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Delete Selected Charts
        </a>
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Group Selected Charts
        </a>
        <div
            class="h-0 my-2 border border-solid border-t-0 border-blueGray-800 opacity-25"
        />
        <a
            on:click={createText}
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Create Text
        </a>
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Create Decorative Box
        </a>
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Create Image
        </a>
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Create Table
        </a>
    </div>
</div>
