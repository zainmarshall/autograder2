<script lang="ts"> 
    // Data types
    type Tree = Record<number, number[]>;
    type Position = { x: number; y: number };
    type Positions = Record<number, Position>;

    // Define the sample tree
    let tree: Tree = $state({
        1: [2, 3, 4],
        2: [5, 6],
        3: [],
        4: [7],
        5: [],
        6: [],
        7: [],
    });


    let root = 1;
    let positions = $state(layout(tree));
    let dragNode: number | null = $state(null);
    let dragOffset = $state({ x: 0, y: 0 });

    // Store the leaves and buds as derived state from the tree
    let leaves = $derived(() => {
        let l: number[] = [];
        for (let node in tree) {
            if (tree[Number(node)].length === 0) l.push(Number(node));
        }
        return l;
    });
    let buds = $derived(() => {
        let b: number[] = [];
        for (let node in tree) {
            let n = Number(node);
            let children = tree[n];
            if (
                n !== root &&
                children.length > 0 &&
                children.every((c: number) => tree[c].length === 0)
            )
                b.push(n);
        }
        return b;
    });

    // Get all the children of a node, allows for moving buds with their leaves
    function getChildren(node: number) {
        let result: number[] = [];
        (function dfs(u: number) {
            tree[u].forEach((c) => {
                result.push(c);
                dfs(c);
            });
        })(node);
        return result;
    }

    function layout(
        tree: Tree,
        node = root,
        depth = 0,
        x = 400,
        spacing = 200,
    ): Positions {
        let pos: Positions = {};
        function dfs(n: number, d: number, cx: number, sp: number) {
            pos[n] = { x: cx, y: 50 + d * 100 };
            let children = tree[n];
            children.forEach((child, i) => {
                let childX =
                    cx - sp / 2 + (i * sp) / Math.max(1, children.length - 1);
                dfs(child, d + 1, childX, sp / 1.5);
            });
        }
        dfs(node, depth, x, spacing);
        return pos;
    }

    $effect(() => {
        positions = layout(tree);
    });

    function findParent(node: number) {
        for (let p in tree) {
            if (tree[Number(p)].includes(node)) return Number(p);
        }
        return null;
    }

    let originalPositions: Positions = {};

    function onMouseDown(event: MouseEvent, node: number) {
        if (!buds().includes(node)) return;
        dragNode = node;
        dragOffset.x = positions[node].x - event.clientX;
        dragOffset.y = positions[node].y - event.clientY;
        // Save original positions for snap-back
        originalPositions = { ...positions };
        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);
    }

    function onMouseMove(event: MouseEvent) {
        if (!dragNode) return;

        // Move the bud and all its children
        let nodesToMove = [dragNode, ...getChildren(dragNode)];
        let dx = event.clientX + dragOffset.x - positions[dragNode].x;
        let dy = event.clientY + dragOffset.y - positions[dragNode].y;

        let newPositions = { ...positions };
        nodesToMove.forEach((n) => {
            newPositions[n] = {
                x: positions[n].x + dx,
                y: positions[n].y + dy,
            };
        });
        positions = newPositions;
    }

    function onMouseUp(event: MouseEvent) {
        if (!dragNode) return;

        // Find closest valid node to drop onto
        let target: number | null = null;
        let minDist = Infinity;
        let descendants = getChildren(dragNode).concat(dragNode);
        for (let node in positions) {
            let n = Number(node);
            if (descendants.includes(n)) continue;
            let dx = positions[n].x - positions[dragNode].x;
            let dy = positions[n].y - positions[dragNode].y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < minDist && dist < 50) {
                minDist = dist;
                target = n;
            }
        }

        if (target) {
            // Remove from old parent
            for (let parent in tree) {
                tree[Number(parent)] = tree[Number(parent)].filter(
                    (c) => c !== dragNode,
                );
            }
            // Add to new parent
            tree[target].push(dragNode);
        } else {
            // Snap back to original positions
            positions = { ...originalPositions };
        }

        dragNode = null;
        window.removeEventListener("mousemove", onMouseMove);
        window.removeEventListener("mouseup", onMouseUp);
    }

    function isValidDropTarget(node: number) {
        if (!dragNode) return false;
        let descendants = getChildren(dragNode).concat(dragNode);
        return !descendants.includes(node);
    }
</script>

<!-- START HTML -->

<!-- Title and Counts -->
<div class="font-semibold text-white mb-4 flex flex-col items-center">
    <h3 class="text-lg ">Counts</h3>
    <p class="text-sm">
        Buds: {buds().length} | Leaves: {leaves().length}
    </p>
</div>

<!-- SVG to represent the tree structure -->
<svg width="800" height={Math.max(...Object.values(positions).map(p => p.y)) + 70}>
    <!-- Edges -->
    {#each Object.entries(tree) as [parent, children]}
        {#each children as child}
            <!-- Don't draw a line between a node and its child if the child is being dragged-->
            {#if !(dragNode === Number(child) && findParent(dragNode) === Number(parent))}
                <line
                    x1={positions[Number(parent)].x}
                    y1={positions[Number(parent)].y}
                    x2={positions[Number(child)].x}
                    y2={positions[Number(child)].y}
                    stroke="white"
                />
            {/if}
        {/each}
    {/each}

    <!-- Nodes -->
    {#each Object.keys(tree) as node}
        <circle
            cx={positions[Number(node)].x}
            cy={positions[Number(node)].y}
            r="20"
            class={`cursor-pointer transition duration-150 ease-in-out 
            focus:outline-none focus:stroke-2 hover:stroke-indigo-400 hover:stroke-2
            ${buds().includes(Number(node))
            ? "fill-red-600"
            : leaves().includes(Number(node))
            ? "fill-blue-800"
            : "fill-gray-800"}
            ${isValidDropTarget(Number(node)) ? "stroke-green-400 stroke-3" : "stroke-white stroke-1"}
            `}
            onmousedown={(e) => onMouseDown(e, Number(node))}
            role="button"
            tabindex="0"
        />

        <!-- Node Number Text Label-->
        <text
            x={positions[Number(node)].x}
            y={positions[Number(node)].y + 5}
            text-anchor="middle"
            class="fill-white text-[14px] font-sans bold select-none"
        >
            {node}
        </text>
    {/each}
</svg>
