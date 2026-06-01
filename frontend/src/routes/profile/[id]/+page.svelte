<script lang="ts">
    import { api } from '$lib/api';
    import type { User } from '$lib/api.ts';
    import { userStore, isAuthenticated } from '$lib';
    import {page } from '$app/stores';

	// user state
	let user = $state<User | null>(null);
    let error = $state<string | null>(null);
    let loading = $state(true);
    let cfAvatar = $state<string | null>(null);

	// form state
    let usacoDivision = $state('');
	let cfHandle = $state('');
       let personalEmail = $state('');

    

    // load user once on mount
    // Map backend division to select value
    function backendDivisionToSelectValue(division: string): string {
        const map: Record<string, string> = {
            'Bronze': 'bronze',
            'Silver': 'silver',
            'Gold': 'gold',
            'Platinum': 'plat',
            'Not Participated': '',
            '': '',
        };
        return map[division] ?? '';
    }

    $effect(() => {
        (async () => {
            try {
                const data = await api.fetchUserUID($page.params.id ?? '');
                user = data;
                usacoDivision = backendDivisionToSelectValue(data.usaco_division);
                cfHandle = data.cf_handle || '';
                personalEmail = data.personal_email || '';

                if (data.cf_handle) {
                    const cfProfile = await api.getCodeforcesProfile(data.cf_handle);
                    cfAvatar = cfProfile?.titlePhoto || null;
                } else {
                    cfAvatar = null;
                }
            } catch (err) {
                console.error('Error fetching user:', err);
                error = String(err);
            } finally {
                loading = false;
            }
        })();
    });

    // Map backend value to display label
    function usacoFormated(division: string) {
        const displayMap: Record<string, string> = {
            'Bronze': 'Bronze',
            'Silver': 'Silver',
            'Gold': 'Gold',
            'Platinum': 'Platinum',
            'Not Participated': 'Not Participated',
            '': 'Not Participated',
            null: 'Not Participated',
            undefined: 'Not Participated',
        };
        return displayMap[division] ?? 'Not Participated';
    }


     function getBorderColor(division: string): string {
        const colors: Record<string, string> = {
            'Bronze': '#CD7F32',
            'Silver': '#C0C0C0',
            'Gold': '#FFD700',
            'Platinum': '#E8F1FF',
            'Not Participated': '#6B7280',
            '': '#6B7280',
        };
        return colors[division] || '#6B7280';
    }

</script>

{#if !$isAuthenticated}
    <div class="min-h-screen flex items-center justify-center">
        <div class="text-white">Loading... Who made such a terrible frontend? Such a terrible programmer... If you see this message ask for a cookie </div>
    </div>
{:else}
    <main class="relative flex flex-col items-center justify-center min-h-[70vh] px-4">
        <div class="w-full max-w-xl bg-white/80 dark:bg-zinc-900/90 shadow-xl rounded-2xl p-8 flex flex-col items-center">
            <div class="w-42 h-42 rounded-full bg-gradient-to-br from-indigo-400 to-blue-600 flex items-center justify-center mb-4 shadow-md overflow-hidden">
                {#if cfAvatar}
                    <img
                        src={cfAvatar}
                        alt="Codeforces Avatar"
                        class="w-full h-full object-cover rounded-full border-4"
                        style="border-color: {getBorderColor(user?.usaco_division || '')};"
                        onerror={(e) => {
                            console.log('Image load error:', e);
                            const target = e.target as HTMLImageElement | null;
                            if (target) target.style.display = 'none';
                        }}
                    />
                {:else}
                    <span class="text-4xl text-white font-bold">{user?.display_name?.[0] ?? '?'}</span>
                {/if}
            </div>
            <h2 class="text-3xl font-bold text-zinc-900 dark:text-zinc-100 mb-2">{user?.display_name}</h2>
            <div class="text-base text-zinc-500 dark:text-zinc-400 mb-6">@{user?.username}</div>
            <div class="w-full space-y-3 mb-6">
                <div class="flex justify-between text-zinc-700 dark:text-zinc-200">
                    <span class="font-medium">USACO Division</span>
                    <span>{usacoFormated(user?.usaco_division || '')}</span>
                </div>
                <div class="flex justify-between text-zinc-700 dark:text-zinc-200">
                    <span class="font-medium">Codeforces Handle</span>
                    <span>
                        {#if user?.cf_handle}
                            <a
                                href={`https://codeforces.com/profile/${user.cf_handle}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                class="underline underline-offset-2 hover:text-indigo-400 transition-colors"
                            >
                                {user.cf_handle}
                            </a>
                        {:else}
                            <span class="text-zinc-400">None</span>
                        {/if}
                    </span>
                </div>
                <div class="flex justify-between text-zinc-700 dark:text-zinc-200">
                    <span class="font-medium">Personal Email</span>
                    <span>
                        {#if user?.personal_email}
                            {user.personal_email}
                        {:else}
                            <span class="text-zinc-400">None</span>
                        {/if}
                    </span>
                </div>
            </div>
        </div>
    </main>
{/if}