<script lang="ts">
	import { api } from '$lib/api';
	import { onMount } from 'svelte';
	let user: any = null;

	onMount(async () => {
		const res = await api.getUser();
		if (res.ok) {
			user = await res.json();
			window.location.href = '/profile';
		} else {
			user = null;
		}
	});
</script>

<main class="min-h-screen flex items-center justify-center bg-black">
	<div class="w-full max-w-md mx-4 p-8 rounded-lg border border-slate-800 bg-black">
		<div class="text-center">
			<!-- Title -->
			<h1 class="text-3xl font-bold text-slate-100 mb-8 tracking-tight select-none">
				TJCT Grader
			</h1>

			<!-- Enter Button -->
			<div class="mb-8">
				<button on:click={() => api.loginIon()} class="w-full bg-indigo-600 hover:bg-indigo-800 text-white font-semibold py-3 px-4 rounded-lg transition-colors">Enter</button>
			</div>


			<!-- Info Text-->
			<div class="text-slate-400 text-sm">
				Welcome to the automatic grader for TJ Computer Team.<br />
				Please email <a href="mailto:tjctgrader@gmail.com" class="underline hover:text-indigo-400">tjctgrader@gmail.com</a> and message the officers if you have any questions.
			</div>
		</div>
	</div>
</main>
