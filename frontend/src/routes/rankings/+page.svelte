<script lang="ts">
	import { api } from '$lib/api';
	import type { Ranking } from '$lib/api.ts';

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
        if (rank === 1) return '🥇';
        if (rank === 2) return '🥈';
        if (rank === 3) return '🥉';
        return '';
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

	<div class="overflow-x-auto">
		<table class="w-full min-w-[600px] bg-zinc-950 rounded-lg overflow-hidden text-zinc-100">
			<thead>
				<tr>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">#</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Name</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">USACO</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Codeforces</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">In-Houses</th>
					<th class="py-3 px-4 bg-zinc-800 font-semibold text-center border-b border-zinc-700">Index</th>
				</tr>
			</thead>
			<tbody>
				{#each rankings as ranking, i}
					<tr class="transition hover:bg-zinc-800/80 border-b border-zinc-800 last:border-none {i % 2 === 1 ? 'bg-zinc-900/80' : ''}">
						{#if ranking.rank == 1 || ranking.rank == 2 || ranking.rank == 3}
							<td class="py-2 px-4 text-center font-bold text-blue-400">{rankToMedal(ranking.rank)}</td>
                            {:else}
						    <td class="py-2 px-4 text-center">{ranking.rank}</td>
						{/if}

                        
						<td class="py-2 px-4 text-center"><a class="text-blue-400 hover:underline" href={'/profile/' + ranking.id}>{ranking.name}</a></td>
						<td class="py-2 px-4 text-center">{ranking.usaco}</td>
						<td class="py-2 px-4 text-center">{ranking.cf}</td>
						<td class="py-2 px-4 text-center">{Number(ranking.inhouse).toFixed(3)}</td>
						<td class="py-2 px-4 text-center">{Number(ranking.index).toFixed(3)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
