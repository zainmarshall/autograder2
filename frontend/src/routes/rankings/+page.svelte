<script lang="ts">
	import { api } from '$lib/api';
	import type { Ranking } from '$lib/api.ts';
    import Table from '$lib/components/Table.svelte';

	// rankings state
	let rankings = $state<Ranking[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// load rankings once on mount
	$effect(() => {
		(async () => {
			try {
				const data = await api.fetchRankings();
				console.log('Fetched:', data);
				rankings = data;
			} catch (err) {
				console.error('Error fetching rankings:', err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});

    const rankToMedal = (rank: number) => {
        if (rank === 1) return '🍪🍪🍪🏅';
        if (rank === 2) return '🍪🍪🥈';
        if (rank === 3) return '🍪🥉';
        return rank;
    };

	const usacoFormat = (usaco: number) => {
		if (usaco == 1900) return `Platinum (${usaco})`;
		if (usaco == 1600) return `Gold (${usaco})`;
		if (usaco == 1200) return `Silver (${usaco})`;
		if (usaco == 800) return `Bronze / NA (${usaco})`;
	};
</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">Rankings</div>
	<div class="mb-6 text-base text-zinc-400">
		<a
			class="underline hover:text-blue-400"
			href="https://docs.google.com/document/d/14CBtom9g0AKZkmncUQQJwV-dIwG54Arr26FnWfUcdvI/edit?usp=sharing"
			target="_blank"
		>
			Learn about how rankings are formulated
		</a>
	</div>

	<Table data={rankings} headers={[
		{ label: '#', field: 'rank', render: (row) => rankToMedal(row.rank) },
		{ label: 'Name', field: 'name', link: (row) => ({ href: `/profile/${row.username}`, text: row.name }) },
		{ label: 'Index', field: 'index' },
		{ label: 'USACO', field: 'usaco', render: (row) => usacoFormat(row.usaco) },
		{ label: 'Codeforces', field: 'cf' },
		{ label: 'In-Houses', field: 'inhouse' }
	]}/>
</div>
