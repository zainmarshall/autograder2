<script lang="ts">
	import { api } from '$lib/api';
	import type { Contest } from '$lib/api.ts';

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
	<div class="mb-6 text-base text-zinc-400">
		<a
			class="underline hover:text-blue-400"
			href="https://docs.google.com/document/d/14CBtom9g0AKZkmncUQQJwV-dIwG54Arr26FnWfUcdvI/edit?usp=sharing"
			target="_blank"
		>
			Learn about how contests are formulated
		</a>
	</div>

	<div class="overflow-x-auto">
		<table class="w-full min-w-[600px] bg-zinc-950 rounded-lg overflow-hidden text-zinc-100">

           <!-- 
            export interface Contest {
    id: number;
    name: string;
    rated: boolean;
    season: number;
    tjioi: boolean;
    start: Date;
    end: Date;
    editorial: string;
}-->
			<thead>
				<tr>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">#</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Name</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Rated</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Season</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Start</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">End</th>
				</tr>
			</thead>
			<tbody>
				{#each contests as contest, i}
					<tr class="transition hover:bg-zinc-800/80 border-b border-zinc-800 last:border-none {i % 2 === 1 ? 'bg-zinc-900/80' : ''}">
						<td class="py-2 px-4 text-center">{contest.id}</td>
						<td class="py-2 px-4 text-center">
							<a class="underline hover:text-blue-400" href={`/contests/${contest.id}`}>
								{contest.name}
							</a>
						</td>
						<td class="py-2 px-4 text-center">{contest.rated ? 'Yes' : 'No'}</td>
						<td class="py-2 px-4 text-center">{contest.season}</td>
                        <!-- format start and date much shorter-->
						<td class="py-2 px-4 text-center">{contest.start.toLocaleDateString()} {contest.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
						<td class="py-2 px-4 text-center">{contest.end.toLocaleDateString()} {contest.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
