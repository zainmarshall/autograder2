<script lang="ts">
    import { api } from '$lib/api';
    import type { User } from '$lib/api.ts';
    import { isAuthenticated } from '$lib';
    import { page } from '$app/stores';

	// user state
	let user = $state<User | null>(null);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// form state
    let usacoDivision = $state('');
	let cfHandle = $state('');
	let isSubmitting = $state(false);

    

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
                const id: string = String($page.params.id);
                const data = await api.fetchUserUID(id);
                user = data;
                usacoDivision = backendDivisionToSelectValue(data.usaco_division);
                cfHandle = data.cf_handle || '';
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

</script>


<main class="flex flex-col items-center justify-center min-h-[70vh] px-4">
    <div class="w-full max-w-xl bg-white/80 dark:bg-zinc-900/90 shadow-xl rounded-2xl p-8 flex flex-col items-center">
        <div class="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-400 to-blue-600 flex items-center justify-center mb-4 shadow-md">
            <span class="text-4xl text-white font-bowld">{user?.display_name?.[0] ?? '?'}</span>
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
                <span>{user?.cf_handle}</span>
            </div>
        </div>
    </div>
</main>