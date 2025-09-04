<script lang="ts">
	import { api } from '$lib/api';
	import type { Standing } from '$lib/api.ts';
	import Table from '$lib/components/Table.svelte';
	import { page } from '$app/stores';

	// standings state
	let standings = $state<Standing[]>([]);
	let contestTitle = $state<string>('');
	let pnum = $state<number>(0);
	let error = $state<string | null>(null);
	let loading = $state(true);
	let cid: string | null = null;

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
				contestTitle = data.title;
				pnum = data.pnum;
				standings = data.load;
			} catch (err) {
				console.error('Error fetching standings:', err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});


	function renderProblems(row: Standing) {
		if (!Array.isArray(row.problems)) return '';
		return row.problems.map((val) =>
			`<span class='px-2 py-1 rounded font-mono ${val > 0 ? 'text-green-400' : val < 0 ? 'text-red-400' : 'text-zinc-300'}'>${val}</span>`
		).join(' ');
	}

</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">{contestTitle} Standings</div>
	<Table data={standings} headers={[
		{ label: 'Rank', field: 'rank' },
		{ label: 'Name', field: 'name', link: (row) => ({ href: `/profile/${row.username}`, text: row.name }) },
		{ label: 'Username', field: 'username' },
		{ label: 'Solved', field: 'solved' },
		{ label: 'Penalty', field: 'penalty' },
		{ label: 'Problems', field: 'problems', render: renderProblems }
	]}/>
</div>
