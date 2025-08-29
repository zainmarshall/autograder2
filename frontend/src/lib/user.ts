import { writable, derived } from 'svelte/store';

export interface User {
	id: number;
	username: string;
	display_name: string;
	is_staff: boolean;
	usaco_division: string;
	cf_handle: string;
	particles_enabled: boolean;
}

const user = writable<User | null>(null);

export const isAuthenticated = derived(user, $user => $user !== null);

export const userStore = {
	setUser: (userData: User | null) => user.set(userData),
	updateUser: (updates: Partial<User>) => user.update($user => $user ? { ...$user, ...updates } : null),
	clearUser: () => user.set(null),
	fetchUser: async () => {
		try {
			const response = await fetch('/api/user/', {
				credentials: 'include'
			});
			if (response.ok) {
				const userData = await response.json();
				user.set(userData);
			} else {
				user.set(null);
			}
		} catch (error) {
			console.error('Failed to fetch user:', error);
			user.set(null);
		}
	},
	 login: () => {
	 	window.location.href = '/login/ion/';
	},
	logout: async () => {
		try {
			const response = await fetch('/oauth/logout/', {
				method: 'POST',
				credentials: 'include'
			});
			user.set(null);
			window.location.href = '/';
		} catch (error) {
			console.error('Failed to logout:', error);
		}
	},
	updateStats: async (data: { usaco_division: string; cf_handle: string }) => {
		try {
			const response = await fetch('/update_stats/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
				credentials: 'include',
				body: new URLSearchParams({
					usaco_div: data.usaco_division.toLowerCase(),
					cf_handle: data.cf_handle,
				}),
			});
			if (response.ok) {
				await userStore.fetchUser();
			}
		} catch (error) {
			console.error('Failed to update stats:', error);
		}
	},
};

export { user };
