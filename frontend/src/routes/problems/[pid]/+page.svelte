<script lang="ts">
    import { api } from '$lib/api';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import type { Problem } from '$lib/api.ts';

    let problem = $state<Problem | null>(null);
    let error = $state<string | null>(null);
    let loading = $state(true);

    onMount(async () => {
        try {
            const pid = $page.params.pid;
            problem = await api.fetchProblem(Number(pid));
        } catch (err) {
            error = String(err);
        } finally {
            loading = false;
        }
    });
</script>

<!-- STRUCTURE

CARD 1: Info - Problem name, problem id, time limit, memory limit

CARD 2: Statment

Card 3: Input

CARD 4: Output

Card 5: Samples
-->


<main class="flex flex-col items-center min-h-[70vh] px-2 py-8">

    <!-- header-->
    <div class="w-full max-w-3xl flex flex-col sm:flex-row items-start justify-between mb-6 px-2">
        <div class="flex-1 min-w-0">
            <h2 class="text-2xl sm:text-3xl font-bold text-zinc-900 dark:text-zinc-100 leading-tight">{problem?.name}</h2>
            <div class="text-sm text-zinc-500 dark:text-zinc-400 mt-1">#{problem?.id}</div>
        </div>
        <div class="flex flex-row gap-6 mt-2 sm:mt-0">
            <div class="flex flex-col items-start">
                <span class="text-xs text-zinc-500">Time Limit</span>
                <span class="font-medium text-zinc-800 dark:text-zinc-200">{problem?.tl} ms</span>
            </div>
            <div class="flex flex-col items-start">
                <span class="text-xs text-zinc-500">Memory Limit</span>
                <span class="font-medium text-zinc-800 dark:text-zinc-200">{problem?.ml} MB</span>
            </div>
        </div>
    </div>

    <!-- contents -->
    <div class="w-full max-w-3xl text-left bg-transparent">
        <!-- Statement -->
        <section class="mb-8">
            <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Statement</h3>
            <div class="prose max-w-none text-base text-white">{problem?.statement}</div>
        </section>

        <!-- Input -->
        <section class="mb-8">
            <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Input</h3>
            <div class="prose max-w-none text-base text-white">{problem?.inputtxt}</div>
        </section>

        <!-- Output -->
        <section class="mb-8">
            <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Output</h3>
            <div class="prose max-w-none text-base text-white">{problem?.outputtxt}</div>
        </section>

        <!-- Samples -->
        <section class="mb-8">
            <h3 class="text-xl font-semibold text-zinc-900 dark:text-zinc-100 mb-2">Samples</h3>
            <div class="prose max-w-none text-base text-white">{problem?.samples}</div>
        </section>
    </div>

    <button class="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors" onclick={() => { 
        const contestId = $page.url.searchParams.get('contest');
        let url = `/submit?problem=${problem?.id}`;
        if (contestId) url += `&contest=${contestId}`;
        window.location.href = url;
    }}>
		Submit
	</button>
</main>
