import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		proxy: {
			'/api': 'http://localhost:3000',
			'/oauth': 'http://localhost:3000',
			'/social': 'http://localhost:3000',
			'/update_stats': 'http://localhost:3000',
		}
	}
});
