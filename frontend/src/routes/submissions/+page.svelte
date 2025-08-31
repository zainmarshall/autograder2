<script lang="ts">
	import { api } from "$lib/api";
	import type { Submission } from "$lib/api.ts";
	import Table from "$lib/components/Table.svelte";

	// submissions state
	let submissions = $state<Submission[]>([]);
	let error = $state<string | null>(null);
	let loading = $state(true);

	// load submissions once on mount
	$effect(() => {
		(async () => {
			try {
				const data = await api.fetchSubmissions();
				console.log("Fetched:", data);
				submissions = data;
			} catch (err) {
				console.error("Error fetching submissions:", err);
				error = String(err);
			} finally {
				loading = false;
			}
		})();
	});
</script>

<div class="my- rounded-xl p-4 md:p-8 shadow-lg">
	<div class="mb-2 text-3xl font-bold text-zinc-100">Submissions</div>
	<div class="mb-6 text-base text-zinc-400"></div>

		<Table
			data={submissions}
			headers={[
				{ label: "#", field: "id" },
				{ label: "User", field: "usr" },
				{ label: "Language", field: "language" },
				{ label: "Verdict", field: "verdict" },
				{ label: "Runtime", field: "runtime" },
				{
					label: "Problem",
					field: "problem",
					link: (row) => {
						
						const id = row.problem_id || row.problem_id_num || row.problem.match(/\d+/)?.[0] || row.problem;
						return { href: `/problems/${id}`, text: row.problem };
					}
				},
				{
					label: "Timestamp",
					field: "timestamp",
					render: (row) => {
						const d = new Date(row.timestamp);
						const mm = String(d.getMonth() + 1).padStart(2, '0');
						const dd = String(d.getDate()).padStart(2, '0');
						const yyyy = d.getFullYear();
						let h = d.getHours();
						const m = String(d.getMinutes()).padStart(2, '0');
						const ampm = h >= 12 ? 'PM' : 'AM';
						h = h % 12;
						h = h ? h : 12;
						return `${mm}/${dd}/${yyyy} ${h}:${m} ${ampm}`;
					}
				},
			]}
		/>
</div>
