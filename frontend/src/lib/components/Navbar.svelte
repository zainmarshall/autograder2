<script lang="ts">
  import NavLink from './NavLink.svelte'
  import { userStore, isAuthenticated } from '$lib'

  let active = $state('')
  let authed = $state(false)

  $effect(() => {
    const unsub = isAuthenticated.subscribe(v => {
      authed = v
    })
    return () => unsub()
  })
</script>

<nav class="w-full bg-black border-b border-slate-800">
  <div class="max-w-7xl mx-auto px-4 flex items-center h-16 justify-between">
    <div class="flex items-center space-x-6">
      <a href="/" class="flex items-center space-x-2 select-none">
        <img src="/src/lib/assets/logo.png" alt="TJCT Grader" class="h-7 w-7" />
        <span class="text-xl font-bold text-slate-100 tracking-tight">TJCT Grader</span>
      </a>
      <NavLink href="/profile" active={active === 'profile'}>Profile</NavLink>
      <NavLink href="/contests" active={active === 'contests'}>Contests</NavLink>
      <NavLink href="/submissions" active={active === 'submissions'}>Submissions</NavLink>
      <NavLink href="/problems" active={active === 'problems'}>Problemset</NavLink>
      <NavLink href="/submit" active={active === 'submit'}>Submit</NavLink>
      <NavLink href="/rankings" active={active === 'rankings'}>Rankings</NavLink>
      <NavLink href="/info" active={active === 'info'}>Info</NavLink>
      <NavLink href="/attendance" active={active === 'attendance'}>Attendance</NavLink>
    </div>

    <div class="flex items-center space-x-2">
      {#if authed}
        <button
          onclick={() => userStore.logout()}
          class="px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150 text-slate-100 hover:text-indigo-400 hover:bg-slate-800"
        >
          Log Out
        </button>
      {/if}
    </div>
  </div>
</nav>
