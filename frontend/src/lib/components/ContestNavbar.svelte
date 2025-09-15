<script lang="ts">
  import NavLink from "./NavLink.svelte";
  import { page } from "$app/stores";
  import { api } from "$lib/api";
  import type { Contest } from "$lib/api.ts";
  //add the contest start and end date as a prop

  const { contestId = "" }: { contestId?: string | number } = $props();

  // Helper to preserve all query params and set/replace contest
  function withContestParam(path: string) {
    const params = new URLSearchParams($page.url.search);
    params.set("contest", String(contestId));
    return `${path}?${params.toString()}`;
  }

  let timeString = $state("--:--:--")
  let contest = $state<Contest | null>(null);
  let error = $state<string | null>(null);
  let loading = $state(true);
  $effect(() => {
    (async () => {
      try {
        const data = await api.fetchContestCID(Number(contestId));
        console.log("Fetched:", data);
        contest = data;
        console.log("Contest data:", contest);
      } catch (err) {
        console.error("Error fetching contests:", err);
        error = String(err);
      } finally {
        loading = false;
      }
    })();
  });

  // returns if the current time > start time and < end time
  function isContestActive(): boolean {
    const now = new Date();
    if (!contest || !contest.end || !contest.start) {
      console.log("error");
      return false;
    }
    return now > contest.start && now < contest.end;
  }

  //update timeleft every second
  function updateTimeString() {
    timeString = timeLeft();
  }

  $effect(() => {
    if (contest && contest.end) {
      const interval = setInterval(() => {
        updateTimeString();
      }, 1000);
      updateTimeString(); // initial update
      return () => clearInterval(interval);
    }
  });

  function timeLeft(): string {
    const now = new Date();
    const end = new Date(contest?.end ?? 0);
    const diff = end.getTime() - now.getTime();
    if (diff <= 0) return "00:00:00";
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(
      2,
      "0",
    )}:${String(seconds).padStart(2, "0")}`;
  }

  function contestEnded(): boolean {
    const now = new Date();
    if (!contest || !contest.end) {
      console.log("error");
      return false;
    }
    console.log("Now:", now, "End:", contest?.end);
    return now > contest?.end;
  }
</script>

<nav class="w-full bg-black border-b border-slate-800">
  <!--left side-->
  <div class="max-w-7xl mx-auto px-4 flex items-center h-16 justify-between">
    <div class="flex items-center space-x-6">
      <a href="/" class="flex items-center space-x-2 select-none">
        <img src="/src/lib/assets/logo.png" alt="TJCT Grader" class="h-7 w-7" />
        <span class="text-xl font-bold text-slate-100 tracking-tight">
          {#if !loading}
            {contest?.name}
          {:else}
            timothy oh
          {/if}
        </span>
      </a>
      <NavLink href="/contests" active={false}>Return Home</NavLink>
      <NavLink href={withContestParam("/problems")} active={false}
        >Problems</NavLink
      >
      <NavLink href={withContestParam("/submit")} active={false}>Submit</NavLink
      >
      <NavLink href={withContestParam(`/standings`)} active={false}
        >Standings</NavLink
      >
    </div>
    <div class="flex items-center space-x-2"></div>
    <div class="flex items-center space-x-2">
      <div class="px-3 py-2 rounded-md text-sm font-medium text-slate-100">
        <div class="flex items-center space-x-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.414-1.414L11 9.586V6z"
              clip-rule="evenodd"
            />
          </svg>
          <div>
            {#if !loading}
              {#if isContestActive()}
                Time Left: {timeString}
              {:else if contestEnded()}
                Contest Ended
              {:else}
                Contest Not Started
              {/if}
            {:else}
              timothy
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
</nav>
