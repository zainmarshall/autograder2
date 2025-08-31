<script lang="ts">
	import { api } from '$lib/api';
	import type { Problem } from '$lib/api.ts';
    import Table from '$lib/components/Table.svelte';

	// problems state
	let problems = $state<Problem[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// load problems once on mount
	$effect(() => {
		(async () => {
			try {
				const data = await api.fetchProblemset();
				console.log('Fetched:', data);
				problems = data;
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

	<Table data={problems} headers={[
		{ label: '#', field: 'id' },
		{ label: 'Name', field: 'name' },
		{ label: 'Contest', field: 'contest' },
		{ label: 'Points', field: 'points' }
	]}/>
</div>
