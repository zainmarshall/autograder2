<script lang="ts">
    import { userStore, user, isAuthenticated } from '$lib';
    import { onMount } from 'svelte';
    let usacoDivision = $state('');
    let cfHandle = $state('');
    let isSubmitting = $state(false);
    let showEdit = $state(false);

    onMount(() => {
        userStore.fetchUser();
    });

    $effect(() => {
        if ($user) {
            const divisionMap: Record<string, string> = {
                'Bronze': 'bronze',
                'Silver': 'silver',
                'Gold': 'gold',
                'Platinum': 'plat',
                'Not Participated': ''
            };
            usacoDivision = divisionMap[$user.usaco_division] || '';
            cfHandle = $user.cf_handle || '';
        }
    });

    async function handleSubmit(event: Event) {
        event.preventDefault();
        if (!$user) return;
        isSubmitting = true;
        try {
            await userStore.updateStats({
                usaco_division: usacoDivision,
                cf_handle: cfHandle,
            });
            showEdit = false;
        } finally {
            isSubmitting = false;
        }
    }
</script>

{#if !$isAuthenticated}
    <div class="min-h-screen flex items-center justify-center">
        <div class="text-white">Loading... Who made such a terrible frontend? Such a terrible programmer... If you see this message ask for a cookie </div>
    </div>
{:else}
    <main class="flex flex-col items-center justify-center min-h-[70vh] px-4">
        <div class="w-full max-w-xl bg-white/80 dark:bg-zinc-900/90 shadow-xl rounded-2xl p-8 flex flex-col items-center">
            <div class="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-400 to-blue-600 flex items-center justify-center mb-4 shadow-md">
                <span class="text-4xl text-white font-bold">{$user?.display_name?.[0] ?? '?'}</span>
            </div>
            <h2 class="text-3xl font-bold text-zinc-900 dark:text-zinc-100 mb-2">{$user?.display_name}</h2>
            <div class="text-base text-zinc-500 dark:text-zinc-400 mb-6">@{$user?.username}</div>
            <div class="w-full space-y-3 mb-6">
                <div class="flex justify-between text-zinc-700 dark:text-zinc-200">
                    <span class="font-medium">USACO Division</span>
                    <span>{$user?.usaco_division}</span>
                </div>
                <div class="flex justify-between text-zinc-700 dark:text-zinc-200">
                    <span class="font-medium">Codeforces Handle</span>
                    <span>{$user?.cf_handle}</span>
                </div>
            </div>
            <button
                class="mb-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
                on:click={() => showEdit = true}
                disabled={showEdit}
            >
                Edit
            </button>
            {#if showEdit}
                <form on:submit={handleSubmit} class="w-full mt-4 space-y-4">
                    <div>
                        <label for="usaco_div" class="block text-zinc-700 dark:text-zinc-200 font-medium mb-2">
                            USACO Division:
                        </label>
                        <select
                            id="usaco_div"
                            bind:value={usacoDivision}
                            class="w-full bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 rounded px-3 py-2 border border-zinc-300 dark:border-zinc-700 focus:border-indigo-500 focus:outline-none"
                        >
                            <option value="">Not Participated</option>
                            <option value="bronze">Bronze</option>
                            <option value="silver">Silver</option>
                            <option value="gold">Gold</option>
                            <option value="plat">Platinum</option>
                        </select>
                    </div>
                    <div>
                        <label for="cf_handle" class="block text-zinc-700 dark:text-zinc-200 font-medium mb-2">
                            Codeforces Handle:
                        </label>
                        <input
                            id="cf_handle"
                            type="text"
                            bind:value={cfHandle}
                            placeholder="Leave blank if you don't have one"
                            class="w-full bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 rounded px-3 py-2 border border-zinc-300 dark:border-zinc-700 focus:border-indigo-500 focus:outline-none"
                        />
                    </div>
                    <button
                        type="submit"
                        disabled={isSubmitting}
                        class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 text-white font-semibold py-2 px-6 rounded-lg transition-colors w-full"
                    >
                        {isSubmitting ? 'Saving...' : 'Save'}
                    </button>
                </form>
                <p class="text-zinc-400 text-xs mt-4 text-center">
                    Note: If the entered information is suspicious, it will be verified in-person.
                </p>
            {/if}
        </div>
    </main>
{/if}