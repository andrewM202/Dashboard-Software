<script>
	// core components
	import CardStats from "components/Cards/CardStats.svelte";
	import { tick } from "svelte";

	// Optional Arguments
	export let cards;
	export let title;
	export let titleColor; // Pass in class for text color
	export let titleFontSize; // Pass in class for font size
	export let inputs;
	export let CollectionName;
	export let SearchFunction; // Pass in the search function for the form
	export let submitValue; // Value of the submit button
	export let headerBGColor;

	let submitButtonID = Math.random().toString(36).substring(2, 8);
	let submitID = Math.random().toString(36).substring(2, 8);

	async function positionSearchBar(e = j$(`#${submitID}`)) {
		await tick();
		if (inputs !== undefined) {
			if (inputs.length % 2 === 0) {
				j$(e).css({
					width: "100%",
				});
				j$(e).removeClass("lg:w-6/12");
			} else {
				j$(e).css({
					width: "",
				});
				j$(e).addClass("lg:w-6/12");
			}
		}
	}

	// Check to see if we want to make the search bar
	// full width whenever we change the selected collection
	$: inputs, positionSearchBar();

	async function styleFlexData() {
		await tick();
		let interval = setInterval(function () {
			if (j$("ul.flexdatalist-results").length !== 0) {
				clearInterval(interval);
				j$("ul.flexdatalist-results").css({
					"border-width": "0",
				});
				j$(".headerStatsFlexForm").click(function () {
					j$(".item").css({ cursor: "pointer" });
				});
			}
		}, 10);
	}

	function formLoad() {
		// Initialize localStorage for whether the header search is toggled by default.
		// If its already initialized, then enact the setting
		if (localStorage.getItem("searchToggle") == null) {
			localStorage.setItem("searchToggle", "false");
		} else if (localStorage.getItem("searchToggle") == "true") {
			j$("#HeaderStatsInputContainer form").css("display", "inherit");
		} else if (localStorage.getItem("searchToggle") == "false") {
			j$("#HeaderStatsInputContainer form").css("display", "none");
		}
	}

	function HeaderStatsInputToggle() {
		j$("#HeaderStatsInputContainer form").animate({
			height: "toggle",
		});
		if (localStorage.getItem("searchToggle") == "true") {
			localStorage.setItem("searchToggle", "false");
		} else if (localStorage.getItem("searchToggle") == "false") {
			localStorage.setItem("searchToggle", "true");
		}
	}

	// Function to set query filtering capabilities
	// to the filter icons in input fields
	function FilterFunction(evt) {
		console.log(evt);
	}
</script>

<!-- Header -->
<div
	id="HeaderStatsHeaderDiv"
	class="relative bg-red-500 md:pt-6 pt-6"
	style={headerBGColor}
>
	<div class="px-4 md:px-10 mx-auto w-full">
		<div>
			{#if title !== undefined}
				<div
					id="HeaderStatsTitleContainer"
					class="flex justify-center w-full"
				>
					<h3
						class="{titleColor} {titleFontSize} z-50 text-center font-normal leading-normal mt-0 mb-2"
					>
						{title}
					</h3>
					<!-- Icon for toggling search inputs -->
					<i
						on:click={HeaderStatsInputToggle}
						style="align-self: center; font-size: 20px;"
						class="fa fa-search mx-4 cursor-pointer"
						aria-hidden="true"
					/>
					<i
						style="align-self: center; font-size: 20px;"
						class="fa fa-wrench mx-4 cursor-pointer"
						aria-hidden="true"
					/>
					<i
						style="align-self: center; font-size: 20px;"
						class="fa fa-trash mx-4 cursor-pointer"
						aria-hidden="true"
					/>
				</div>
			{/if}
			<!-- Card stats -->
			{#if cards !== undefined}
				{#if cards.length > 0}
					<div class="flex flex-wrap justify-center py-4">
						{#each cards as card}
							<div class="w-full lg:w-6/12 xl:w-3/12 px-4 py-2">
								<CardStats
									statSubtitle={card.subtitle}
									statTitle={card.amount}
									statArrow="up"
									statPercent={card.increase}
									statPercentColor={card.increase >= 0
										? "text-emerald-500"
										: "text-red-500"}
									statDescripiron="Since {card.description}"
									statIconName="far fa-chart-bar"
									statIconColor="bg-red-500"
								/>
							</div>
						{/each}
					</div>
				{/if}
			{/if}
			<!-- Inputs -->
			{#if inputs !== undefined}
				<div
					id="HeaderStatsInputContainer"
					class="flex-auto py-10 pt-0"
				>
					<form style="display: none;" use:formLoad>
						<input
							type="hidden"
							name="CollectionName"
							value={CollectionName}
						/>
						<div class="flex flex-wrap">
							{#each inputs as input}
								<div class="w-full lg:w-6/12 py-1 px-4">
									<div class="relative w-full mb-3">
										<label
											class="w-full font-semibold text-lg text-center form-check-label inline-block text-gray-800"
											for={input.name}
											>{input.placeholder}</label
										>
										{#if input.flexdatalistdata !== undefined}
											<input
												use:styleFlexData
												list={input.flexdataid}
												data-min-length="0"
												type="text"
												placeholder={input.placeholder}
												name={input.name}
												id={input.name}
												class="headerStatsFlexForm flexdatalist border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
											/>
											<datalist id={input.flexdataid}>
												{#each input.flexdatalistdata as datarow}
													<option value={datarow} />
												{/each}
											</datalist>
										{:else}
											<input
												id={input.name}
												type={input.type}
												placeholder={input.placeholder}
												name={input.name}
												value={input.type === "Submit"
													? input.placeholder
													: ""}
												class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
											/>
											<i
												on:click={FilterFunction}
												style="top: 60%; right: 3%;"
												class="cursor-pointer absolute fa fa-filter"
												aria-hidden="true"
											/>
										{/if}
									</div>
								</div>
							{/each}
							<div
								class="w-full lg:w-6/12 py-2 px-4 pt-8"
								id={submitID}
							>
								<div class="relative w-full mb-3">
									<input
										on:click={SearchFunction}
										id={submitButtonID}
										type="Submit"
										placeholder="Submit"
										name="submit"
										value={submitValue !== undefined
											? submitValue
											: "Search"}
										class="cursor-pointer border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white hover:bg-gray-200 rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150"
									/>
								</div>
							</div>
						</div>
					</form>
				</div>
			{/if}
		</div>
	</div>
</div>
