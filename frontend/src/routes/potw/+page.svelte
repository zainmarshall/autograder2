<script lang="ts">
    import { api } from '$lib/api';

    let potw = $state<{ beginner: any, intermediate: any, advanced: any } | null>(null);
    let loading = $state(true);
    let error = $state<string | null>(null);

    $effect(() => {
        (async () => {
            try {
                potw = await api.fetchPOTW();
            } catch (err) {
                error = String(err);
            } finally {
                loading = false;
            }
        })();
    });
</script>

<main class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-slate-100 mb-6">Problem of the Week</h1>

    {#if loading}
        <div class="text-zinc-400">Loading…</div>
    {:else if error}
        <div class="text-red-400">Error: {error}</div>
    {:else if potw}
        {#each [
            { key: 'beginner', label: 'Beginner', color: 'border-emerald-500' },
            { key: 'intermediate', label: 'Intermediate', color: 'border-amber-500' },
            { key: 'advanced', label: 'Advanced', color: 'border-rose-500' }
        ] as level}
            {@const entry = potw[level.key as 'beginner' | 'intermediate' | 'advanced']}
            <section class="mb-6 rounded-xl border-l-4 {level.color} bg-zinc-900/70 border border-slate-800 shadow-lg p-6">
                <h2 class="text-xl font-bold text-slate-100 mb-2">{level.label}</h2>
                {#if entry}
                    <div class="text-zinc-200 mb-2">{entry.title}</div>
                    {#if entry.link}
                        <a href={entry.link} target="_blank" rel="noopener noreferrer"
                           class="inline-block text-indigo-400 underline hover:text-indigo-300">
                            Click to see →
                        </a>
                    {/if}
                {:else}
                    <div class="text-zinc-500 italic">No problem set yet.</div>
                {/if}
            </section>
        {/each}
    {/if}
</main>
