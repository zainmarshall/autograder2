export interface User {
	id: number;
	username: string;
	display_name: string;
	is_staff: boolean;
	usaco_division: string;
	cf_handle: string;
	particles_enabled: boolean;
}

export class UserStore {
	user = $state<User | null>(null);
	isAuthenticated = $derived(this.user !== null);

	setUser(user: User | null) {
		this.user = user;
	}

	updateUser(updates: Partial<User>) {
		if (this.user) {
			this.user = { ...this.user, ...updates };
		}
	}

	clearUser() {
		this.user = null;
	}

	async fetchUser() {
		try {
			const response = await fetch('/api/user/', {
				credentials: 'include'
			});
			if (response.ok) {
				const user = await response.json();
				this.setUser(user);
			} else {
				this.clearUser();
			}
		} catch (error) {
			console.error('Failed to fetch user:', error);
			this.clearUser();
		}
	}

	async login() {
		window.location.href = '/social/login/ion/';
	}

	async logout() {
		try {
			const response = await fetch('/oauth/logout/', {
				method: 'POST',
				credentials: 'include'
			});
			this.clearUser();
			window.location.href = '/';
		} catch (error) {
			console.error('Failed to logout:', error);
		}
	}

	async updateStats(data: { usaco_division: string; cf_handle: string }) {
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
				// Refresh user data after update
				await this.fetchUser();
			}
		} catch (error) {
			console.error('Failed to update stats:', error);
		}
	}
}

export const userStore = new UserStore();
