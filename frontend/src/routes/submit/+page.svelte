<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import type { Problem } from '$lib/api.ts';
  import CodeMirror from 'svelte-codemirror-editor';
  import { cpp } from '@codemirror/lang-cpp';
  import { java } from '@codemirror/lang-java';
  import { python } from '@codemirror/lang-python';

  const BACKEND_URL = 'http://localhost:8003';

  let code = $state('');
  let language = $state('cpp');
  let problems = $state<Problem[]>([]);
  let selectedProblem = $state<number | null>(null);
  let submitting = $state(false);
  let errorMsg = $state<string | null>(null);

  let langExtension = $derived(
    language === 'java' ? java() :
    language === 'python' ? python() :
    cpp()
  );

  function getCSRF() {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    errorMsg = null;
    if (!selectedProblem || !language || !code.trim()) {
      errorMsg = 'Select a problem and write some code first.';
      return;
    }
    submitting = true;
    try {
      // Need CSRF cookie from backend before POST
      await fetch(`${BACKEND_URL}/api/`, { credentials: 'include' });
      const csrf = getCSRF();
      const res = await fetch(`${BACKEND_URL}/status/process_submit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrf,
        },
        credentials: 'include',
        body: new URLSearchParams({
          problemid: String(selectedProblem),
          lang: language,
          code,
        }),
      });
      if (res.ok || res.redirected) {
        const contestId = $page.url.searchParams.get('contest');
        window.location.href = contestId ? `/submissions?contest=${contestId}` : '/submissions';
        return;
      }
      const txt = await res.text();
      errorMsg = `Submission failed (${res.status}): ${txt.slice(0, 200)}`;
    } catch (err) {
      errorMsg = `Submission error: ${err}`;
    } finally {
      submitting = false;
    }
  }

  // Persist last-used language in localStorage (acts as default for next submit)
  function saveLang(l: string) {
    try { localStorage.setItem('preferred_lang', l); } catch {}
  }

  onMount(async () => {
    try {
      const saved = localStorage.getItem('preferred_lang');
      if (saved === 'cpp' || saved === 'java' || saved === 'python') language = saved;
    } catch {}

    const all = await api.fetchProblemset();
    const contestId = $page.url.searchParams.get('contest');
    problems = contestId ? all.filter(p => String(p.contest) === contestId) : all;
    const pidParam = $page.url.searchParams.get('problem');
    if (pidParam) {
      const found = problems.find(p => p.id === Number(pidParam));
      if (found) selectedProblem = found.id;
    } else if (problems.length > 0) {
      selectedProblem = problems[0].id;
    }
  });
</script>

<main class="max-w-3xl mx-auto px-4 py-8 text-white">
  <h1 class="text-2xl font-bold mb-6">Submit</h1>

  <div class="mb-4 flex flex-wrap items-center gap-4">
    <label for="problem" class="font-semibold">Problem:</label>
    <select id="problem" bind:value={selectedProblem}
            class="px-3 py-2 rounded-md border border-zinc-700 text-white bg-zinc-900 focus:border-indigo-500 focus:outline-none">
      {#each problems as p}
        <option value={p.id}>{p.id} — {p.name}</option>
      {/each}
    </select>

    <label for="lang" class="font-semibold">Language:</label>
    <select id="lang" bind:value={language} onchange={() => saveLang(language)}
            class="px-3 py-2 rounded-md border border-zinc-700 text-white bg-zinc-900 focus:border-indigo-500 focus:outline-none">
      <option value="cpp">C++</option>
      <option value="java">Java</option>
      <option value="python">Python</option>
    </select>
  </div>

  {#if language === 'java'}
    <div class="mb-4 p-3 rounded-md bg-zinc-900 border border-red-500 text-red-300 flex items-center gap-2">
      <span class="text-red-500 text-xl font-bold">!</span>
      <span>Java users: name your class <span class="font-mono font-bold text-red-400">usercode</span>.</span>
    </div>
  {/if}

  <div class="rounded-md border border-zinc-700 overflow-hidden mb-4">
    <CodeMirror bind:value={code} lang={langExtension} styles={{ '&': { height: '500px', fontSize: '14px' } }} />
  </div>

  {#if errorMsg}
    <div class="mb-4 p-3 rounded-md bg-red-900/40 border border-red-500 text-red-300">{errorMsg}</div>
  {/if}

  <button onclick={handleSubmit} disabled={submitting}
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
    {submitting ? 'Submitting…' : 'Submit'}
  </button>
</main>
