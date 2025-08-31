<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { userStore } from '$lib';
	import { onMount } from 'svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import ContestNavbar from '$lib/components/ContestNavbar.svelte';
	import { page } from '$app/stores';

	let { children } = $props();

	onMount(() => {
		userStore.fetchUser();
	});
</script>

<svelte:head>
	<!-- Tab name and Icon-->
	<link rel="icon" href={favicon} />
	<title>TJ Computer Team Grader</title>
</svelte:head>

<div class="min-h-screen bg-black">
	<!-- Show only one navbar: ContestNavbar if ?contest= is present, else Navbar, but never both -->
	{#if $page.url.pathname !== '/' && $page.url.searchParams.has('contest')}
		<ContestNavbar contestId={$page.url.searchParams.get('contest') ?? ''} />
	{:else if $page.url.pathname !== '/'}
		<Navbar />
	{/if}

	<!-- Render the page itself-->
	<main>{@render children?.()}</main>
</div>
