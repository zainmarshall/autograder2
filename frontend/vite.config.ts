import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		proxy: {
			'/api': 'http://autograder:8000',
			'/oauth': 'http://autograder:8000',
			'/social': 'http://autograder:8000',
			'/update_stats': 'http://autograder:8000',
		}
	}
});