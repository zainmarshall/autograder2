<script lang="ts">
	import { userStore } from '$lib';
	import { onMount } from 'svelte';
	import Button from '$lib/components/Button.svelte';

	onMount(() => {
		userStore.fetchUser();
	});

	$effect(() => {
		if (userStore.isAuthenticated) {
			window.location.href = '/profile';
		}
	});
</script>

<main class="min-h-screen flex items-center justify-center bg-black">
	<div class="w-full max-w-md mx-4 p-8 rounded-lg border border-slate-800 bg-black">
		<div class="text-center">
			<h1 class="text-3xl font-bold text-slate-100 mb-8 tracking-tight select-none">
				TJCT Grader
			</h1>
			<div class="mb-8">
				<Button on:click={() => userStore.login()} className="w-full text-lg py-3">Enter</Button>
			</div>
			<div class="text-slate-400 text-sm">
				Welcome to the automatic grader for TJ Computer Team.<br />
				Please email <a href="mailto:tjctgrader@gmail.com" class="underline hover:text-indigo-400">tjctgrader@gmail.com</a> and message the officers if you have any questions.
			</div>
		</div>
	</div>
</main>
