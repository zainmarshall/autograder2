<!-- App.svelte -->
<script lang="ts">
	import MathJax from '$lib/components/MathJax.svelte';

	let math = $state('$$x^3$$')
</script>

<div class ="text-white"> 
	<input bind:value={math} class=" p-2 rounded text-white bg-black" />

	<MathJax {math} />

</div>
