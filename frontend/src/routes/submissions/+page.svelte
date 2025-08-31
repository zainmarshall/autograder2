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
			{ label: "Contest", field: "contest" },
			{
				label: "Problem",
				field: "problem",
				render: (row) => `<a href="/problems/${row.problem}">${row.problem}</a>`
			},
			{ label: "Insight", field: "insight" },
			{ label: "Timestamp", field: "timestamp" },
		]}
	/>
</div>
