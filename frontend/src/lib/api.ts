
export interface Ranking {
    id: number;
    name: string;
    index: number;
    usaco: number;
    cf: number;
    inhouse: number;
    rank: number;
}

const base = 'http://localhost:3000';

export const api = {
    loginIon: () => window.location.href = `${base}/login/ion/`,
    logout: async () => fetch(`${base}/oauth/logout/`, { method: 'POST', credentials: 'include' }),
    getUser: async () => fetch(`${base}/api/user/`, { credentials: 'include' }),
    updateStats: async (data: { usaco_division: string; cf_handle: string }) =>
        fetch(`${base}/update_stats/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            credentials: 'include',
            body: new URLSearchParams({
                usaco_div: data.usaco_division.toLowerCase(),
                cf_handle: data.cf_handle,
            }),
        }),
    profile: async () => fetch(`${base}/profile/`, { credentials: 'include' }),
    tjioiLogin: () => window.location.href = `${base}/tjioi/login/`,

    async fetchRankings(): Promise<Ranking[]> {
        const season = 2025;
        const res = await fetch(`${base}/rankings/api/${season}/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch rankings');
        const data = await res.json();
        return data.rankings.map((r: any): Ranking => ({
            id: Number(r.id),
            name: String(r.name),
            index: Number(r.index),
            usaco: Number(r.usaco),
            cf: Number(r.cf),
            inhouse: Number(r.inhouse),
            rank: Number(r.rank),
        }));
    },

    async fetchProblemset() {
    const res = await fetch(`${base}/problems/api/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch problemset');
        const data = await res.json();
        return data.problems;
    },

    async fetchContests() {
    const res = await fetch(`${base}/contests/api/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch contests');
        const data = await res.json();
        return data.contests;
    },

    async fetchSubmissions() {
    const res = await fetch(`${base}/runtests/api/submissions/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch submissions');
        const data = await res.json();
        return data.submissions;
    }

};