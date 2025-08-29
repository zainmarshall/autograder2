<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { userStore } from '$lib';
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import { page } from '$app/stores';

	let { children } = $props();

	onMount(() => {
		userStore.fetchUser();
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>TJ Computer Team Grader</title>
</svelte:head>

<div class="min-h-screen bg-black">
	{#if $page.url.pathname !== '/'}
		<Navbar />
	{/if}
	<main>{@render children?.()}</main>
</div>
