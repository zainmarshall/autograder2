export interface Ranking {
    id: number;
    name: string;
    index: number;
    usaco: number;
    cf: number;
    inhouse: number;
    rank: number;
}

export interface Problem {
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

export interface Contest {
    id: number;
    name: string;
    rated: boolean;
    season: number;
    tjioi: boolean;
    start: Date;
    end: Date;
    editorial: string;
}

export interface Submission {
    id: number;
    language: string;
    code: string;
    usr: string;
    verdict: string;
    runtime: number;
    contest: string;
    problem: string;
    insight: string;
    timestamp: Date;
}


export interface Standing {
    id: number;
    name: string;
    solved: number;
    penalty: number;
    rank: number;
    problems: number[];
}

export interface User{
    id: number;
    email: string;
    personal_email: string;
    display_name: string;
    username: string;
    is_staff: boolean;
    is_active: boolean;
    usaco_division: string;
    usaco_rating: number;
    cf_handle: string;
    cf_rating: number;
    grade: string;
    first_time: boolean;
    is_tjioi: boolean;
    author_drops: number;
    inhouse: string;
    index: string;
    particles_enabled: boolean;
}

export const api = {
    loginIon: () => window.location.href = 'http://localhost:3000/login/ion/',
    logout: async () => fetch('/oauth/logout/', { method: 'POST', credentials: 'include' }),
    getUser: async () => fetch('/api/user/', { credentials: 'include' }),
    updateStats: async (data: Partial<User>) => {
        const res = await fetch('/api/user/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('Failed to update profile');
        return await res.json();
    },
    profile: async () => fetch('/profile/', { credentials: 'include' }),
    tjioiLogin: () => window.location.href = '/tjioi/login/',

    async fetchRankings(): Promise<Ranking[]> {
        const season = 2025;
        const res = await fetch(`http://localhost:3000/api/rankings/${season}/`, { credentials: 'include' });
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

    // 
    async fetchProblemset() {
        const res = await fetch(`http://localhost:3000/api/problems/`, { credentials: 'include' });
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

    async fetchContest(){
        const res = await fetch(`http://localhost:3000/api/contests/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch contests');
        const data = await res.json();
        return data.contests.map((r: any): Contest => ({
            id: Number(r.id),
            name: String(r.name),
            rated: Boolean(r.rated),
            season: Number(r.season),
            tjioi: Boolean(r.tjioi),
            start: new Date(r.start),
            end: new Date(r.end),
            editorial: String(r.editorial),
        }));
    },

    // return a single problem
    async fetchProblem(pid: number): Promise<Problem> {
        const res = await fetch(`http://localhost:3000/api/problems/${pid}/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch problem');
        const data = await res.json();
        return {
            id: Number(data.id),
            name: String(data.name),
            contest: Number(data.contest),
            points: Number(data.points),
            statement: String(data.statement),
            inputtxt: String(data.inputtxt),
            outputtxt: String(data.outputtxt),
            samples: String(data.samples),
            tl: Number(data.tl),
            ml: Number(data.ml),
            interactive: Boolean(data.interactive),
            testcases_zip: String(data.testcases_zip),
        };
    },

    // return full submissions list
    async fetchSubmissions(): Promise<Submission[]> {
        const res = await fetch(`http://localhost:3000/api/submissions/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch submissions');
        const data = await res.json();
        return data.results.map((r: any): Submission => ({
            id: Number(r.id),
            language: String(r.language),
            code: String(r.code),
            usr: String(r.usr),
            verdict: String(r.verdict),
            runtime: Number(r.runtime),
            contest: String(r.contest),
            problem: String(r.problem),
            insight: String(r.insight),
            timestamp: new Date(r.timestamp),
        }));
    },

    async fetchStandings(cid: string): Promise<Standing[]> {
        const res = await fetch(`http://localhost:3000/api/contests/${cid}/standings/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch standings');
        const data = await res.json();
        return data.standings.map((r: any): Standing => ({
            id: Number(r.id),
            name: String(r.name),
            solved: Number(r.solved),
            penalty: Number(r.penalty),
            rank: Number(r.rank),
            problems: r.problems.map((p: any) => Number(p)),
        }));
    },

    async fetchUser(): Promise<User> {
        const res = await fetch(`http://localhost:3000/api/user/`, { credentials: 'include' });
        if (!res.ok) throw new Error('Failed to fetch user');
        const data = await res.json();
        return {
            id: Number(data.id),
            email: String(data.email),
            personal_email: String(data.personal_email),
            display_name: String(data.display_name),
            username: String(data.username),
            is_staff: Boolean(data.is_staff),
            is_active: Boolean(data.is_active),
            usaco_division: String(data.usaco_division),
            usaco_rating: Number(data.usaco_rating),
            cf_handle: String(data.cf_handle),
            cf_rating: Number(data.cf_rating),
            grade: String(data.grade),
            first_time: Boolean(data.first_time),
            is_tjioi: Boolean(data.is_tjioi),
            author_drops: Number(data.author_drops),
            inhouse: String(data.inhouse),
            index: String(data.index),
            particles_enabled: Boolean(data.particles_enabled),
        };
    },
}