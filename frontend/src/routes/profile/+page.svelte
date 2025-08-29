<script lang="ts">
	import { userStore } from '$lib';
	import { onMount } from 'svelte';
	import Button from '$lib/components/Button.svelte';

	let usacoDivision = $state('');
	let cfHandle = $state('');
	let isSubmitting = $state(false);

	onMount(() => {
		userStore.fetchUser();
	});

	// Update form values when user data loads
	$effect(() => {
		if (userStore.user) {
			// Map display values back to form values
			const divisionMap: Record<string, string> = {
				'Bronze': 'bronze',
				'Silver': 'silver',
				'Gold': 'gold',
				'Platinum': 'plat',
				'Not Participated': ''
			};
			usacoDivision = divisionMap[userStore.user.usaco_division] || '';
			cfHandle = userStore.user.cf_handle || '';
		}
	});

	async function handleSubmit(event: Event) {
		event.preventDefault();
		if (!userStore.user) return;

		isSubmitting = true;
		try {
			await userStore.updateStats({
				usaco_division: usacoDivision,
				cf_handle: cfHandle,
			});
		} finally {
			isSubmitting = false;
		}
	}

	function handleLogout() {
		userStore.logout();
	}
</script>

{#if !userStore.isAuthenticated}
	<div class="min-h-screen flex items-center justify-center">
		<div class="text-white">Loading...</div>
	</div>
{:else}
	<!-- Navigation Header -->
	<header class="bg-slate-800 border-b border-slate-700">
		<nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between items-center h-16">
				<div class="flex items-center space-x-8">
					<h1 class="text-xl font-semibold text-white">TJCT Grader</h1>
					<div class="hidden md:flex space-x-4">
						<a href="/profile" class="text-blue-400 hover:text-blue-300">Home</a>
						<a href="/submissions" class="text-gray-300 hover:text-white">Submissions</a>
						<a href="/contests" class="text-gray-300 hover:text-white">Contests</a>
						<a href="/problems" class="text-gray-300 hover:text-white">Problemset</a>
						<a href="/submit" class="text-gray-300 hover:text-white">Submit</a>
						<a href="/rankings" class="text-gray-300 hover:text-white">Rankings</a>
					</div>
				</div>
				<div class="flex items-center space-x-4">
					<button
						onclick={handleLogout}
						class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
					>
						Log Out
					</button>
				</div>
			</div>
		</nav>
	</header>

	<main class="max-w-4xl mx-auto p-6">
		<div class="bg-white/5 backdrop-blur-sm rounded-lg p-6">
			<h2 class="text-2xl font-bold text-white mb-6">Profile</h2>

			{#if userStore.user?.is_staff}
				<div class="mb-4">
					<a
						href="/admin"
						class="text-blue-400 hover:text-blue-300 underline"
					>
						Django Admin
					</a>
				</div>
			{/if}

			<div class="space-y-4">
				<div class="text-white">
					<strong>Name:</strong> {userStore.user?.display_name}
				</div>
				<div class="text-white">
					<strong>Username:</strong> {userStore.user?.username}
				</div>
			</div>

			<form onsubmit={handleSubmit} class="mt-6 space-y-4">
				<div>
					<label for="usaco_div" class="block text-white font-medium mb-2">
						USACO Division:
					</label>
					<select
						id="usaco_div"
						bind:value={usacoDivision}
						class="w-full bg-slate-700 text-white rounded px-3 py-2 border border-slate-600 focus:border-blue-500 focus:outline-none"
					>
						<option value="">Not Participated</option>
						<option value="bronze">Bronze</option>
						<option value="silver">Silver</option>
						<option value="gold">Gold</option>
						<option value="plat">Platinum</option>
					</select>
				</div>

				<div>
					<label for="cf_handle" class="block text-white font-medium mb-2">
						Codeforces Handle:
					</label>
					<input
						id="cf_handle"
						type="text"
						bind:value={cfHandle}
						placeholder="Leave blank if you don't have one"
						class="w-full bg-slate-700 text-white rounded px-3 py-2 border border-slate-600 focus:border-blue-500 focus:outline-none"
					/>
				</div>

				<button
					type="submit"
					disabled={isSubmitting}
					class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-semibold py-2 px-4 rounded transition-colors"
				>
					{isSubmitting ? 'Saving...' : 'Save'}
				</button>
			</form>

			<p class="text-gray-400 text-sm mt-4">
				Note: If the entered information is suspicious, it will be verified in-person.
			</p>
		</div>
	</main>
{/if}
