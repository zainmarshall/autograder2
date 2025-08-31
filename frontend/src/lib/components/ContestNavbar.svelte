<script lang="ts">
  import NavLink from './NavLink.svelte';
  import { page } from '$app/stores';
  const { contestId = '' }: { contestId?: string | number } = $props();

  // Helper to preserve all query params and set/replace contest
  function withContestParam(path: string) {
    const params = new URLSearchParams($page.url.search);
    params.set('contest', String(contestId));
    return `${path}?${params.toString()}`;
  }
</script>

<nav class="w-full bg-black border-b border-slate-800">
  <div class="max-w-7xl mx-auto px-4 flex items-center h-16 justify-between">
    <div class="flex items-center space-x-6">
      <a href="/" class="flex items-center space-x-2 select-none">
        <img src="/src/lib/assets/logo.png" alt="TJCT Grader" class="h-7 w-7" />
        <span class="text-xl font-bold text-slate-100 tracking-tight">TJCT Grader</span>
      </a>
      <NavLink href="/contests" active={false}>Return Home</NavLink>
      <NavLink href={withContestParam('/problems')} active={false}>Problems</NavLink>
      <NavLink href={withContestParam('/submit')} active={false}>Submit</NavLink>
      <NavLink href={withContestParam(`/standings`)} active={false}>Standings</NavLink>
    </div>
    <div class="flex items-center space-x-2">
    </div>
  </div>
</nav>
