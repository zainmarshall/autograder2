<!-- render a single $latex$ as a MathJax Components -->

<script lang="ts">
	import { onMount } from 'svelte'

	let { math } = $props<{ math: string }>()

	let container: HTMLSpanElement


	let mathjaxReady = false;

	function renderMath() {
		if (mathjaxReady && window.MathJax?.typesetPromise) {
			window.MathJax.typesetPromise([container]);
		}
	}


	onMount(() => {
		// Load MathJax config BEFORE the MathJax script
		if (!document.getElementById('mathjax-config')) {
			const config = document.createElement('script');
			config.id = 'mathjax-config';
			config.type = 'text/javascript';
			config.text = `window.MathJax = {tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}, svg: {fontCache: 'global'}};`;
			document.head.append(config);
		}
		if (!document.getElementById('mathjax-script')) {
			const script = document.createElement('script');
			script.id = 'mathjax-script';
			script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
			script.async = true;
			document.head.append(script);
			script.onload = () => {
				mathjaxReady = true;
				renderMath();
			};
		} else {
			mathjaxReady = true;
			renderMath();
		}
	});


	$effect(() => {
		renderMath();
	});

	export function typeset() {
		renderMath();
	}
</script>

<span bind:this={container}>
	{@html math}
</span>
