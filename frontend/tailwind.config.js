/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
	],
	theme: {
		extend: {
			colors: {
				primary: '#6366f1', 
				accent: '#a21caf', 
				background: '#0f172a', 
				surface: '#1e293b', 
				text: '#f1f5f9', 
				success: '#22c55e', 
				warning: '#f59e42', 
				error: '#ef4444', 
			},
		},
	},
	plugins: [],
};
