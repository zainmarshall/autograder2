<script lang="ts">
    import { marked } from 'marked';

    let markdown = $state('');
    let html = $state('');

    $effect(() => {
        const fetchMarkdown = async () => {
            const res = await fetch('/src/lib/markdown/information/rules.md');
            markdown = await res.text();
            html = marked.parse(markdown);
        };
        fetchMarkdown();
    });
</script>

<div class="prose prose-invert max-w-3xl mx-auto p-8">
    {@html html}
</div>
