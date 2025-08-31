<script lang="ts">
	import { api } from '$lib/api';
	import type { Contest } from '$lib/api.ts';
    import Table from '$lib/components/Table.svelte';

	// contests state
	let contests = $state<Contest[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// load contests once on mount
	$effect(() => {
		(async () => {
			try {
				const data = await api.fetchContest();
				console.log('Fetched:', data);
				contests = data;
			} catch (err) {
				console.error('Error fetching contests:', err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});
</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">Contests</div>
	<div class="mb-6 text-base text-zinc-400"> </div>


	<Table data={contests} headers={[
		{ label: '#', field: 'id' },
		{
			label: 'Name',
			field: 'name',
			link: (row) => ({ href: `/problems?contest=${row.id}`, text: row.name })
		},
		{
			label: 'Rated',
			field: 'rated',
			render: (row) => row.rated ? '✓' : '✗'
		},
		{ label: 'Season', field: 'season' },
				{
					label: 'Date',
					field: 'start',
					render: (row) => {
						const d = new Date(row.start);
						const mm = String(d.getMonth() + 1).padStart(2, '0');
						const dd = String(d.getDate()).padStart(2, '0');
						const yyyy = d.getFullYear();
						return `${mm}/${dd}/${yyyy}`;
					}
				},
	]}/>
</div>
