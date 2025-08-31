<script lang="ts">
	import { api } from '$lib/api';
	import type { Standing } from '$lib/api.ts';
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';

	// standings state
	let standings = $state<Standing[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);
	let cid: string | null = null;

	// load standings once on mount
	$effect(() => {
		cid = $page.url.searchParams.get('contest');
		(async () => {
			if (!cid) {
				error = 'No contest id specified.';
				loading = false;
				return;
			}
			try {
				const data = await api.fetchStandings(cid);
				standings = data;
			} catch (err) {
				console.error('Error fetching standings:', err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});

	// Helper to render the problems array as colored cells
	function renderProblems(row: Standing) {
		return row.problems.map((val, idx) =>
			`<span class='px-2 py-1 rounded font-mono ${val > 0 ? 'text-green-400' : val < 0 ? 'text-red-400' : 'text-zinc-300'}'>${val}</span>`
		).join(' ');
	}

	const headers = [
		{ label: 'ID', field: 'id' },
		{ label: 'Name', field: 'name' },
		{ label: 'Solved', field: 'solved' },
		{ label: 'Penalty', field: 'penalty' },
		{ label: 'Rank', field: 'rank' },
		{ label: 'Problems', field: 'problems', render: renderProblems },
	];
</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">Standings</div>
	<div class="mb-6 text-base text-zinc-400"> </div>

	{#if loading}
		<div>Loading...</div>
	{:else if error}
		<div class="text-red-500">{error}</div>
	{:else}
		<Table data={standings} headers={headers} />
	{/if}
</div>
