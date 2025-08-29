<script lang="ts">
	import NavLink from './NavLink.svelte';
	import { userStore } from '$lib';

	export let active: string = '';
</script>

<nav class="w-full bg-black border-b border-slate-800">
	<div class="max-w-7xl mx-auto px-4 flex items-center h-16 justify-between">
		<div class="flex items-center space-x-6">
			<a href="/" class="flex items-center space-x-2 select-none">
				<img src="/src/lib/assets/logo.png" alt="TJCT Grader" class="h-7 w-7" />
				<span class="text-xl font-bold text-slate-100 tracking-tight">TJCT Grader</span>
			</a>
			<NavLink href="/profile" active={active === 'profile'}>Profile</NavLink>
			<NavLink href="/submissions" active={active === 'submissions'}>Submissions</NavLink>
			<NavLink href="/contests" active={active === 'contests'}>Contests</NavLink>
			<NavLink href="/problems" active={active === 'problems'}>Problemset</NavLink>
			<NavLink href="/submit" active={active === 'submit'}>Submit</NavLink>
			<NavLink href="/rankings" active={active === 'rankings'}>Rankings</NavLink>
		</div>
		<div class="flex items-center space-x-2">
			{#if userStore.isAuthenticated}
				<button onclick={() => userStore.logout()} class="text-slate-400 hover:text-red-400 font-medium transition">Log Out</button>
			{/if}
		</div>
	</div>
</nav>
