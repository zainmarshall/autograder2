<script lang="ts">
  import { onMount } from 'svelte';
  import { basicEditor } from 'prism-code-editor/setups';
  import 'prism-code-editor/prism/languages/python';
  import 'prism-code-editor/prism/languages/cpp';
  import 'prism-code-editor/prism/languages/java';

  let editorEl: HTMLDivElement;
  let editorInstance: any;
  let value = '';
  let language = $state('cpp');

  onMount(() => {
    editorInstance = basicEditor(editorEl, {
      language,
      theme: 'dracula',
      value,
      wordWrap: true,
      lineNumbers: true,
    }, () => {
      // ready
    });
    editorInstance.onUpdate = (val: string) => {
      value = val;
    };
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
    <label for="lang" class="block mb-2 font-semibold text-white">Language:</label>
    <select id="lang" bind:value={language} class="mb-4 px-3 py-2 rounded border border-zinc-300 dark:border-zinc-700 text-white bg-zinc-800">
      <option value="cpp">C++</option>
      <option value="java">Java</option>
      <option value="python">Python</option>
    </select>
    {#if language === 'java'}
      <div class="mb-4 p-2 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-900">
        Java users, make sure you are
        <a href="https://docs.google.com/document/d/17r0fh2rezqDhNoCoUtwVtExn8hRml0BjeAqxQZk9MCs/edit?usp=sharing" target="_blank" class="underline text-blue-700">naming the class "usercode"</a>.
      </div>
    {/if}
    <div style="display: grid;">
      <div bind:this={editorEl} style="height: 400px;"></div>
    </div>
  </div>
  <button class="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors">
    Submit
  </button>
</main>