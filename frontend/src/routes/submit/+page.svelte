<script lang="ts">
  /* TODO: Fix the editor lines things. also make the editgor reactive such tatht it actually updates the value wonc4 you click submti, asl o save preffered langauge iun cokokies usah that yo udoint n eed to continousley swiytch.  */
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import type { Problem } from '$lib/api.ts';
  import { basicEditor } from 'prism-code-editor/setups';
  import 'prism-code-editor/prism/languages/python';
  import 'prism-code-editor/prism/languages/cpp';
  import 'prism-code-editor/prism/languages/java';

  let editorEl: HTMLDivElement;
  let editorInstance: any;
  let value = '';
  let language = $state('cpp');

  let problems = $state<Problem[]>([]);
  let selectedProblem = $state<number | null>(null);

  async function handleSubmit(e: Event) {
    e.preventDefault();
    console.log('Selected Problem:', selectedProblem);
    console.log('Selected Language:', language);
    console.log('Editor Value:', value);
    if (!selectedProblem || !language || !value) {
      alert('Please select a problem, language, and enter code.');
      return;
    }
    try {
      value = editorInstance
      console.log('Submitting with Value:', value);
      // Get CSRF token from cookie
      const match = document.cookie.match(/csrftoken=([^;]+)/);
      const csrfToken = match ? match[1] : '';
      const res = await fetch('http://localhost:3000/status/process_submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'include',
        body: new URLSearchParams({
          problemid: String(selectedProblem),
          lang: language,
          code: value,
        }),
      });
      if (res.redirected) {
        window.location.href = res.url;
        return;
      }
      if (!res.ok) {
        const text = await res.text();
        alert('Submission failed: ' + text);
      } else {
        alert('Submitted!');
      }
    } catch (err) {
      alert('Error submitting: ' + err);
    }
  }

  onMount(() => {
    // Fetch problems asynchronously
    (async () => {
      const allProblems = await api.fetchProblemset();
      const contestId = $page.url.searchParams.get('contest');
      if (contestId) {
        problems = allProblems.filter((p: Problem) => String(p.contest) === contestId);
      } else {
        problems = allProblems;
      }
      if (problems.length > 0) selectedProblem = problems[0].id;

      editorInstance = basicEditor(editorEl, {
        language,
        theme: 'dracula',
        value,
        wordWrap: true,
        lineNumbers: true,
      }, () => {
        // ready
      });
      value = editorInstance.getValue();
    })();

    return () => editorInstance?.destroy?.();
  });

  $effect(() => {
    if (editorInstance) {
      editorInstance.setLanguage(language);
    }
  });
</script>

<main class="flex flex-col items-center justify-center min-h-[70vh] px-4 text-white bg-black">
<h1 class="text-2xl font-bold mb-4 pt-8">Submit</h1>
  <div class="w-full max-w-2xl mb-4">
    <div class="mb-4">
      <label for="problem" class="font-semibold text-white mr-2">Problem:</label>
      <select id="problem" bind:value={selectedProblem} class="px-4 py-2 rounded-lg border border-zinc-600 hover:border-indigo-600 text-white bg-zinc-900 transition-all shadow-sm mr-4 inline-block" style="vertical-align: middle;">
      {#each problems as problem}
        <option value={problem.id}>{problem.name}</option>
      {/each}
      </select>
      <label for="lang" class="font-semibold text-white mr-2">Language:</label>
      <select id="lang" bind:value={language} class="px-4 py-2 rounded-lg border border-zinc-600 hover:border-indigo-600 text-white bg-zinc-900 transition-all shadow-sm inline-block" style="vertical-align: middle;">
      <option value="cpp">C++</option>
      <option value="java">Java</option>
      <option value="python">Python</option>  
      </select>
    </div>
    {#if language === 'java'}
      <div class="mb-4 p-3 rounded-lg bg-zinc-900 border border-red-500 text-red-300 flex items-center gap-2 shadow">
        <span class="text-red-500 text-xl font-bold">&#33;</span>
        <span>
          Java users: Name your class <span class="font-mono font-bold text-red-400">usercode</span>. <!--<a href="https://docs.google.com/document/d/17r0fh2rezqDhNoCoUtwVtExn8hRml0BjeAqxQZk9MCs/edit?usp=sharing" target="_blank" class="underline text-indigo-400 hover:text-indigo-300">See details</a>-->
        </span>
      </div>
    {/if}
    <div
      bind:this={editorEl}
      class="w-full border border-zinc-700 rounded-lg"
      style="height: 500px; max-height: 500px; overflow-y: auto; background: #282A36;"
    ></div>
  </div>
  <button class="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors" onclick={handleSubmit}>
    Submit
  </button>
</main>