
<script lang="ts">
    //the data is the objecs in the tagble
    //label is the header
    //field is like the fields from the bojetc
    // render is. function that you can call on every data point for a specific field
    // link hyperlinks a filed to something like a problem or smth. 
	let { data = [], headers = [] } = $props<{
		data: any[];
		headers: { label: string; field: string; render?: (row: any) => any; link?: (row: any) => { href: string, text?: string } }[];
	}>();

	// Helper to render a link for a field with underline effect
	function renderLink(row: any, linkFn: (row: any) => { href: string, text?: string }) {
		const { href, text } = linkFn(row);
		return `<a href="${href}" class='underline underline-offset-2 hover:text-indigo-400 transition-colors'>${text ?? href}</a>`;
	}
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