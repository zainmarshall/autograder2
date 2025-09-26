<script lang="ts">
	let { data = [], headers = [] } = $props<{
		data: any[];
		headers: { label: string; field: string; render?: (row: any) => any; link?: (row: any) => { href: string; text?: string } }[];
	}>();

	let sortField = $state<string | null>(null);
	let sortAsc = $state(true);

	let sortedData = $derived([...data].sort((a, b) => {
		if (!sortField) return 0;
		const valA = a[sortField];
		const valB = b[sortField];
		if (valA == null) return 1;
		if (valB == null) return -1;
		if (valA < valB) return sortAsc ? -1 : 1;
		if (valA > valB) return sortAsc ? 1 : -1;
		return 0;
	}));

	function toggleSort(field: string) {
		if (sortField === field) {
			sortAsc = !sortAsc;
		} else {
			sortField = field;
			sortAsc = true;
		}
	}

	// render link helper
	function renderLink(row: any, linkFn: (row: any) => { href: string; text?: string }) {
		const { href, text } = linkFn(row);
		return `<a href="${href}" class='underline underline-offset-2 hover:text-indigo-400 transition-colors'>${text ?? href}</a>`;
	}
</script>

<div class="overflow-x-auto">
	<table class="w-full min-w-[600px] bg-zinc-950 rounded-lg overflow-hidden text-zinc-100">
		<thead>
			<tr>
				{#each headers as header}
					<th
						class="py-3 px-4 bg-indigo-800 font-semibold text-center border-b border-indigo-700 cursor-pointer select-none group"
						onclick={() => toggleSort(header.field)}
					>
						<div class="flex items-center justify-center gap-1">
							{header.label}
							{#if sortField === header.field}
								{#if sortAsc}
									<!-- Up chevron -->
									<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 group-hover:opacity-80 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
									</svg>
								{:else}
									<!-- Down chevron -->
									<svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 group-hover:opacity-80 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
									</svg>
								{/if}
							{:else}
								<!-- Neutral chevron -->
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="w-4 h-4 opacity-30 group-hover:opacity-80 transition-opacity"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
								</svg>
							{/if}
						</div>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each sortedData as datum, i}
				<tr class="transition hover:bg-zinc-800/80 border-b border-zinc-800 last:border-none {i % 2 === 1 ? 'bg-zinc-900/80' : ''}">
					{#each headers as header}
						<td class="py-2 px-4 text-center">
							{#if header.link}
								{@html renderLink(datum, header.link)}
							{:else if header.render}
								{@html header.render(datum)}
							{:else}
								{datum[header.field]}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>
