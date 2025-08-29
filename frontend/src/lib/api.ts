export const api = {
  loginIon: () => window.location.href = 'http://localhost:3000/login/ion/',
  logout: async () => fetch('/oauth/logout/', { method: 'POST', credentials: 'include' }),
  getUser: async () => fetch('/api/user/', { credentials: 'include' }),
  updateStats: async (data: { usaco_division: string; cf_handle: string }) =>
    fetch('/update_stats/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      credentials: 'include',
      body: new URLSearchParams({
        usaco_div: data.usaco_division.toLowerCase(),
        cf_handle: data.cf_handle,
      }),
    }),
  profile: async () => fetch('/profile/', { credentials: 'include' }),
  tjioiLogin: () => window.location.href = '/tjioi/login/',
};