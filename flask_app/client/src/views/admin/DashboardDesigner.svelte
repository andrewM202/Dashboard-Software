<script>
    let showActionBar = false;
    let parentOffset;
    let chartsCreated = 0;

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
                        left: event.pageX - parentOffset.left + "px",
                    });
                }
            }
        );
        // Make the action bar disappear when left clicking
        j$("#DashboardDesignerContainer").on("click", function () {
            showActionBar = false;
        });
    }

    // Event listener for creating a chart
    function createChart(event) {
        // Create a div where clicked
        j$("#DashboardDesignerContainer").append(
            `<div id="chart${chartsCreated}" style="top: ${
                event.pageY - parentOffset.top
            }px; left: ${
                event.pageX - parentOffset.left
            }px; width: 500px; height: 500px;" class="absolute bg-blueGray-700 text-white">
                <i style="padding-left: 7px; padding-top: 7px;" class="fa fa-bars" aria-hidden="true"></i>
                <h1 class="text-4xl text-white text-center">Chart Title</h1>
                <div
                    style="right: -4px; bottom: -4px; cursor: ns-resize;"
                    class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
                ></div>
                <div
                    style="left: -4px; bottom: -4px; cursor: ns-resize;"
                    class="bg-rose-400 h-4 w-4 absolute rounded-full px-2"
                ></div>
            </div>`
        );

        // Add event listeners to resizers, so we can resize
        // the chart
        let parent = j$(`#chart${chartsCreated}`);
        let minParentHeight = 250;
        j$(`#chart${chartsCreated} div`).mousedown(function (downEv) {
            downEv.preventDefault();
            j$(window).mousemove(function (moveEv) {
                let initialPos = j$(downEv.target).offset().top;
                let movePos = moveEv.pageY;
                let addHeight = movePos - initialPos;
                j$("body").css("cursor", "ns-resize");
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
    }
</script>

<div
    use:onLoad
    id="DashboardDesignerContainer"
    class="h-auto min-h-screen w-screen"
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
            Delete Chart
        </a>
        <div
            class="h-0 my-2 border border-solid border-t-0 border-blueGray-800 opacity-25"
        />
        <a
            href="#pablo"
            class="text-sm py-2 px-4 font-normal block w-full whitespace-no-wrap bg-transparent text-white"
        >
            Separated link
        </a>
    </div>
</div>
