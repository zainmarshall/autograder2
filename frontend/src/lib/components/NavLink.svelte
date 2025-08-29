<script lang="ts">
	export let href: string = '#';
	export let active: boolean = false;
</script>

<a
	href={href}
	class="px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150
		text-slate-100 hover:text-indigo-400 hover:bg-slate-800
		{active ? 'text-indigo-400 border-b-2 border-indigo-500' : ''}"
>
	<slot />
</a>
