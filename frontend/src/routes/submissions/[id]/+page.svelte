<script lang="ts">
    import { api } from '$lib/api';
    import { page } from '$app/stores';

    let sub = $state<any>(null);
    let loading = $state(true);
    let error = $state<string | null>(null);

    $effect(() => {
        (async () => {
            try {
                sub = await api.fetchSubmissionDetail($page.params.id);
            } catch (err) {
                error = String(err);
            } finally {
                loading = false;
            }
        })();
    });

    function formatLang(l: string) {
        if (l === 'cpp') return 'C++';
        if (l === 'java') return 'Java';
        if (l === 'python') return 'Python';
        return l;
    }

    function formatTs(ts: string) {
        const d = new Date(ts);
        return d.toLocaleString();
    }

    function verdictClass(v: string) {
        if (v === 'Accepted' || v === 'AC') return 'text-emerald-400';
        if (v === 'Running' || v === 'RN') return 'text-amber-400';
        return 'text-red-400';
    }
</script>

<main class="max-w-4xl mx-auto px-4 py-8 text-white">
    {#if loading}
        <div class="text-zinc-400">Loading…</div>
    {:else if error}
        <div class="text-red-400">Error: {error}</div>
    {:else if sub}
        <div class="mb-6 flex items-baseline justify-between">
            <h1 class="text-2xl font-bold">Submission #{sub.id}</h1>
            <span class="font-semibold {verdictClass(sub.verdict)}">{sub.verdict}</span>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-6 text-sm">
            <div><span class="text-zinc-400">User:</span> <a href={`/profile/${sub.usr}`} class="text-indigo-400 hover:text-indigo-300 underline">{sub.usr}</a></div>
            <div><span class="text-zinc-400">Language:</span> {formatLang(sub.language)}</div>
            <div><span class="text-zinc-400">Problem:</span>
                {#if sub.problem_id}
                    <a href={`/problems/${sub.problem_id}`} class="text-indigo-400 hover:text-indigo-300 underline">{sub.problem}</a>
                {:else}
                    {sub.problem}
                {/if}
            </div>
            <div><span class="text-zinc-400">Contest:</span> {sub.contest ?? '—'}</div>
            <div><span class="text-zinc-400">Runtime:</span> {sub.runtime} ms</div>
            <div><span class="text-zinc-400">Submitted:</span> {formatTs(sub.timestamp)}</div>
        </div>

        {#if sub.insight}
            <section class="mb-6 p-4 rounded-md bg-zinc-900/70 border border-slate-800">
                <h2 class="text-lg font-semibold mb-2">Judge Insight</h2>
                <pre class="text-sm text-zinc-300 whitespace-pre-wrap">{sub.insight}</pre>
            </section>
        {/if}

        <section>
            <h2 class="text-lg font-semibold mb-2">Code</h2>
            <pre class="bg-zinc-950 border border-slate-800 rounded p-4 overflow-x-auto text-sm leading-relaxed"><code>{sub.code}</code></pre>
        </section>
    {/if}
</main>
