
export interface Ranking {
    id: number;
    name: string;
    index: number;
    usaco: number;
    cf: number;
    inhouse: number;
    rank: number;
}

export interface Problem{
    id: number;
    name: string;
    contest: number | null;
    points: number;
    statement: string;
    inputtxt: string;
    outputtxt: string;
    samples: string;
    tl: number;
    ml: number;
    interactive: boolean;
    testcases_zip: string | null;
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
        const season = 2025;
        const res = await fetch(`http://localhost:3000/rankings/api/${season}/`, { credentials: 'include' });
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
        const res = await fetch(`http://localhost:3000/problems/api/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch problemset');
        const data = await res.json();
        return data.problems.map((r: any): Problem => ({
            id: Number(r.id),
            name: String(r.name),
            contest: Number(r.contest),
            points: Number(r.points),
            statement: String(r.statement),
            inputtxt: String(r.inputtxt),
            outputtxt: String(r.outputtxt),
            samples: String(r.samples),
            tl: Number(r.tl),
            ml: Number(r.ml),
            interactive: Boolean(r.interactive),
            testcases_zip: String(r.testcases_zip),
        }));
    },

    async fetchContests() {
        const res = await fetch('/contests/api/', { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch contests');
        const data = await res.json();
        return data.contests;
    },

    async fetchSubmissions() {
        const res = await fetch('/runtests/api/submissions/', { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch submissions');
        const data = await res.json();
        return data.submissions;
    }

};