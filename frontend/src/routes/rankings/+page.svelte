<script lang="ts">
  // Hardcoded season for now
  const season = 2025;

  // SvelteKit load function to fetch rankings
  export async function load() {
    const res = await fetch(`/rankings/api/${season}/`, { credentials: 'include' });
    if (!res.ok) throw new Error('Failed to fetch rankings');
    const data = await res.json();
    // Parse string values to numbers for sorting
    const parsedRankings = data.rankings.map((r: any) => ({
      ...r,
      index: parseFloat(r.index),
      inhouse: parseFloat(r.inhouse),
    }));
    return { rankings: parsedRankings };
  }

  // Props from load
  export let rankings: any[] = [];

  // Sorting state
  let sortKey = 'rank';
  let sortAsc = true;

  // Function to handle sorting
  function sortTable(key: string) {
    if (sortKey === key) {
      sortAsc = !sortAsc;
    } else {
      sortKey = key;
      sortAsc = true;
    }
  }

  // Reactive sorted rankings
  $: sortedRankings = [...rankings].sort((a, b) => {
    if (a[sortKey] < b[sortKey]) return sortAsc ? -1 : 1;
    if (a[sortKey] > b[sortKey]) return sortAsc ? 1 : -1;
    return 0;
  });
</script>

<div class="my-8 p-8 bg-white rounded-xl shadow-md">
  <div class="text-3xl font-bold mb-2">Rankings</div>
  <div class="text-base text-gray-500 mb-6">
    <a class="underline hover:text-blue-600" href="https://docs.google.com/document/d/14CBtom9g0AKZkmncUQQJwV-dIwG54Arr26FnWfUcdvI/edit?usp=sharing" target="_blank">
      Learn about how rankings are formulated
    </a>
  </div>

  <div class="overflow-x-auto">
    <table class="w-full bg-gray-50 rounded-lg overflow-hidden">
      <thead>
        <tr>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('rank')}>
            # {#if sortKey==='rank'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('name')}>
            Name {#if sortKey==='name'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('usaco')}>
            USACO {#if sortKey==='usaco'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('cf')}>
            Codeforces {#if sortKey==='cf'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('inhouse')}>
            In-Houses {#if sortKey==='inhouse'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
          <th class="py-3 px-4 bg-gray-100 font-semibold text-center cursor-pointer select-none border-b border-gray-200" on:click={() => sortTable('index')}>
            Index {#if sortKey==='index'}<span class="ml-1 text-xs">{sortAsc ? '▲' : '▼'}</span>{/if}
          </th>
        </tr>
      </thead>
      <tbody>
        {#each sortedRankings as ranking}
          <tr class="transition hover:bg-blue-50">
            <td class="py-2 px-4 text-center">{ranking.rank}</td>
            <td class="py-2 px-4 text-center"><a class="text-blue-600 hover:underline" href={"/profile/" + ranking.id}>{ranking.name}</a></td>
            <td class="py-2 px-4 text-center">{ranking.usaco}</td>
            <td class="py-2 px-4 text-center">{ranking.cf}</td>
            <td class="py-2 px-4 text-center">{ranking.inhouse?.toFixed(3)}</td>
            <td class="py-2 px-4 text-center">{ranking.index?.toFixed(3)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>