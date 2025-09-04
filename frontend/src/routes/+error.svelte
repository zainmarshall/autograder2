<script lang="ts">
  const { error, status } = $props();
</script>

<main class="min-h-screen flex items-center justify-center bg-black">
  <div class="flex flex-col items-center justify-center bg-slate-900 rounded-xl shadow-lg p-10 max-w-lg w-full">
    <h1 class="text-5xl font-bold mb-2 text-red-400">404</h1>
    <p class="text-2xl font-semibold mb-4 text-slate-100">Oops, this page is not found.</p>
    <div class="bg-slate-800 rounded p-4 font-mono text-pink-400 text-base mb-4 text-center">
      <span>int* ptr = nullptr;</span><br />
      <span>*ptr = 42; <span class="text-slate-400"></span></span>
    </div>
    <a href="/" class="mt-4 text-indigo-400 hover:underline">Return Home</a>
  </div>
</main>
  