<script>
	import { link } from "svelte-routing";

	export let location;

	function signIn(e) {
		e.preventDefault();
		j$.ajax({
			type: "POST",
			url: `${location.origin}/auth/login`,
			data: j$("#SignUpForm").serialize(),
			success: function (location) {
				window.location = location;
			},
			error: async function (e) {
				// Error logging
				console.log(e.statusText);
				console.log(e.responseText);
				// If we get an error about the CSRF token, we need to get a new one and try again
				if (e.responseText.indexOf("The CSRF session token is missing") !== -1) {
					const response = await fetch("/auth/getcsrf", {
						credentials: "same-origin",
					}).then((res) => {
						csrf_token = res.headers.get(["X-CSRFToken"]);
						j$.ajaxSetup({
							beforeSend: function (xhr, settings) {
								if (!/^(GET|HEAD|OPTIONS|TRACE)j$/i.test(settings.type) && !this.crossDomain) {
									xhr.setRequestHeader("X-CSRFToken", csrf_token);
								}
							},
						});
						j$.ajax({
							type: "POST",
							url: `${location.origin}/auth/login`,
							data: j$("#SignUpForm").serialize(),
							success: function (location) {
								window.location = location;
							},
							error: function (e) {
								// Error logging
								console.log(e.statusText);
								console.log(e.responseText);
							},
						});
					});
				}
			},
		});
	}
</script>

<div class="container mx-auto px-4 h-full">
	<div class="flex content-center items-center justify-center h-full">
		<div class="w-full lg:w-4/12 px-4">
			<div class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-blueGray-200 border-0">
				<div class="flex-auto px-4 lg:px-10 py-10 pt-0">
					<div class="py-4 text-blueGray-400 text-center mb-3 font-bold">
						<small>Sign in</small>
					</div>
					<form id="SignUpForm">
						<div class="relative w-full mb-3">
							<label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-email"> Username </label>
							<input id="grid-email" type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Username" name="username" />
						</div>

						<div class="relative w-full mb-3">
							<label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" for="grid-password"> Password </label>
							<input id="grid-password" type="password" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" placeholder="Password" name="password" />
						</div>
						<div>
							<label class="inline-flex items-center cursor-pointer">
								<input id="customCheckLogin" type="checkbox" class="form-checkbox border-0 rounded text-blueGray-700 ml-1 w-5 h-5 ease-linear transition-all duration-150" />
								<span class="ml-2 text-sm font-semibold text-blueGray-600"> Remember me </span>
							</label>
						</div>

						<div class="text-center mt-6">
							<button class="bg-blueGray-800 text-white active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150" type="submit" on:click={signIn}> Sign In </button>
						</div>
					</form>
				</div>
			</div>
			<div class="flex flex-wrap mt-6 relative">
				<div class="w-1/2">
					<a href="#pablo" class="text-blueGray-200">
						<small>Forgot password?</small>
					</a>
				</div>
				<div class="w-1/2 text-right">
					<a use:link href="/auth/register" class="text-blueGray-200">
						<small>Create new account</small>
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
