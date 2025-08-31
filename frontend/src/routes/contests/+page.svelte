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
		{ label: 'Name', field: 'name' },
		{ label: 'Rated', field: 'rated' },
		{ label: 'Season', field: 'season' },
		{ label: 'Date', field: 'start' },
	]}/>
</div>
