<script lang="ts">
	let { data = [], headers = [] } = $props<{
		data: any[];
		headers: { label: string; field: string }[];
	}>();
</script>

<div class="overflow-x-auto">
	<table class="w-full min-w-[600px] bg-zinc-950 rounded-lg overflow-hidden text-zinc-100">
		<thead>
			<tr>
				{#each headers as header}
					<th class="py-3 px-4 bg-indigo-800 font-semibold text-center border-b border-indigo-700">
						{header.label}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each data as datum, i}
				<tr class="transition hover:bg-zinc-800/80 border-b border-zinc-800 last:border-none {i % 2 === 1 ? 'bg-zinc-900/80' : ''}">
					{#each headers as header}
						<td class="py-2 px-4 text-center">{datum[header.field]}</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>