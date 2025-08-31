<script lang="ts">
	import { api } from '$lib/api';
	import type { Problem } from '$lib/api.ts';
    import Table from '$lib/components/Table.svelte';

	// problems state
	let problems = $state<Problem[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);

	import { page } from '$app/stores';

	// Helper to filter problems by contest
	function filterProblemsByContest(problems: Problem[], contestId: string | number | null) {
		if (!contestId) return problems;
		return problems.filter(p => String(p.contest) === String(contestId));
	}

	// load problems once on mount, and filter if ?contest= is present
	$effect(() => {
		(async () => {
			try {
				const data = await api.fetchProblemset();
				console.log('Fetched:', data);
				const contestId = $page.url.searchParams.get('contest');
				problems = filterProblemsByContest(data, contestId);
			} catch (err) {
				console.error('Error fetching rankings:', err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});
</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">Problems</div>
	<div class="mb-6 text-base text-zinc-400"></div>

	<Table data={problems} headers={[
		{ label: '#', field: 'id' },
		{
			label: 'Name',
			field: 'name',
			link: (row) => {
				const contestId = $page.url.searchParams.get('contest');
				return contestId
					? { href: `/problems/${row.id}?contest=${contestId}`, text: row.name }
					: { href: `/problems/${row.id}`, text: row.name };
			}
		},
		{ label: 'Contest', field: 'contest' },
		{ label: 'Points', field: 'points' }
	]}/>
</div>
