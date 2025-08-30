
export interface Ranking {
    id: number;
    name: string;
    index: number;
    usaco: number;
    cf: number;
    inhouse: number;
    rank: number;
}

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

    async fetchRankings(): Promise<Ranking[]> {
        const season = 2025
        const res = await fetch(`http://localhost:3000/rankings/api/${season}/`, {
            credentials: 'include'
        })
        if (!res.ok) throw new Error('Failed to fetch rankings')
        const data = await res.json()
        return data.rankings.map((r: any): Ranking => ({
            id: Number(r.id),
            name: String(r.name),
            index: Number(r.index),
            usaco: Number(r.usaco),
            cf: Number(r.cf),
            inhouse: Number(r.inhouse),
            rank: Number(r.rank),
        }))
    }

};