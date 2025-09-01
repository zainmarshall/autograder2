<script lang="ts">
	const { href = '#', active = false, children } = $props<{
		href?: string;
		active?: boolean;
		children?: import('svelte').Snippet;
	}>();
</script>

<a
	href={href}
	class="px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150
		text-slate-100 hover:text-indigo-400 hover:bg-slate-800
		{active ? 'text-indigo-400 border-b-2 border-indigo-500' : ''}"
>
	{@render children?.()}
</a>
