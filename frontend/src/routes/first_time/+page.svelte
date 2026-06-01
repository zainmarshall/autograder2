<script lang="ts">
    import { api } from '$lib/api';
    import { onMount } from 'svelte';

    const BACKEND_URL = 'http://localhost:8003';

    let email = $state('');
    let submitting = $state(false);
    let error = $state<string | null>(null);

    function getCSRF() {
        const m = document.cookie.match(/csrftoken=([^;]+)/);
        return m ? m[1] : '';
    }

    onMount(async () => {
        // If user not first_time, bounce
        try {
            const u = await api.fetchUser();
            if (!u.first_time) window.location.href = '/profile';
        } catch {}
        // Prime CSRF cookie
        await fetch(`${BACKEND_URL}/api/`, { credentials: 'include' });
    });

    async function submit(e: Event) {
        e.preventDefault();
        submitting = true;
        error = null;
        try {
            const res = await fetch(`${BACKEND_URL}/update_first_time/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRF(),
                },
                credentials: 'include',
                body: new URLSearchParams({ email }),
            });
            if (res.ok || res.redirected) {
                window.location.href = '/profile';
            } else {
                error = `Failed (${res.status})`;
            }
        } catch (err) {
            error = String(err);
        } finally {
            submitting = false;
        }
    }
</script>

<main class="min-h-screen flex items-center justify-center bg-black px-4">
    <div class="w-full max-w-md p-8 rounded-2xl shadow-xl bg-zinc-900/90 border border-slate-800">
        <h1 class="text-3xl font-bold text-slate-100 mb-2 text-center">Welcome!</h1>
        <p class="text-zinc-400 text-center mb-6">Just one thing first. Enter your personal email so we can reach you about contests and travel comps.</p>

        <form onsubmit={submit} class="space-y-4">
            <div>
                <label for="email" class="block text-zinc-200 font-medium mb-2">Personal Email</label>
                <input id="email" type="email" required bind:value={email} placeholder="you@gmail.com"
                       class="w-full bg-zinc-800 text-zinc-100 rounded px-3 py-2 border border-zinc-700 focus:border-indigo-500 focus:outline-none" />
            </div>
            {#if error}<div class="text-red-400 text-sm">{error}</div>{/if}
            <button type="submit" disabled={submitting}
                    class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
                {submitting ? 'Saving…' : 'Continue'}
            </button>
        </form>
    </div>
</main>
