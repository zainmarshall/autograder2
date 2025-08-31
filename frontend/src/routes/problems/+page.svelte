<script lang="ts">
	import { api } from '$lib/api';
	import type { Problem } from '$lib/api.ts';

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

	<div class="overflow-x-auto">
		<table class="w-full min-w-[600px] bg-zinc-950 rounded-lg overflow-hidden text-zinc-100">
			<thead>
				<tr>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">#</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Name</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Contest</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Points</th>
				</tr>
			</thead>
			<tbody>
				{#each problems as problem, i}
					<tr class="transition hover:bg-zinc-800/80 border-b border-zinc-800 last:border-none {i % 2 === 1 ? 'bg-zinc-900/80' : ''}">
						<td class="py-2 px-4 text-center">{problem.id}</td>
						<td class="py-2 px-4 text-center">
							<a class="underline hover:text-blue-400" href={`/problems/${problem.id}`}>
								{problem.name}
							</a>
						</td>
						<td class="py-2 px-4 text-center">{problem.contest}</td>
						<td class="py-2 px-4 text-center">{problem.points}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
