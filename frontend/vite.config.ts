import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
       plugins: [tailwindcss(), sveltekit()],
       server: {
	       host: '0.0.0.0',
	       watch: {
		       usePolling: true
	       },
	       proxy: {
		       '/api': 'http://autograder:3000',
		       '/oauth': 'http://autograder:3000',
		       '/social': 'http://autograder:3000',
		       '/update_stats': 'http://autograder:3000',
		       // '/api': 'http://localhost:3000',
		       // '/oauth': 'http://localhost:3000',
		       // '/social': 'http://localhost:3000',
		       // '/update_stats': 'http://localhost:3000',
	       }
       }
});