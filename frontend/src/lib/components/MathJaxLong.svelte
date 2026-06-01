<!--Takes in a string with $latex$ in it and renders each of those using MathJax.svelte-->

<script lang="ts">
import MathJax from './MathJax.svelte';

let { text = '' } = $props<{ text: string }>();

const parts = $derived(text.split(/(\$[^$]+\$)/g));
</script>

<p>
  {#each parts as part}
    {#if part.startsWith('$') && part.endsWith('$')}
      <MathJax math={part} />
    {:else}
      {@html part}
    {/if}
  {/each}
</p>
