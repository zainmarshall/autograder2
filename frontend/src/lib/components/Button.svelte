<script lang="ts">
	export let type: 'button' | 'submit' = 'button';
	export let variant: 'primary' | 'secondary' | 'danger' = 'primary';
	export let disabled: boolean = false;
	export let className: string = '';
</script>

<button
	type={type}
	disabled={disabled}
	class="px-4 py-2 rounded-lg font-semibold transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500
		{variant === 'primary' ? 'bg-indigo-600 hover:bg-indigo-700 text-white' : ''}
		{variant === 'secondary' ? 'bg-slate-700 hover:bg-slate-600 text-slate-100' : ''}
		{variant === 'danger' ? 'bg-red-600 hover:bg-red-700 text-white' : ''}
		{disabled ? 'opacity-50 cursor-not-allowed' : ''}
		{className}"
>
	<slot />
</button>
