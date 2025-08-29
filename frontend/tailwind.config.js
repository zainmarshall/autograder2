/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./src/**/*.{html,js,svelte,ts}',
	],
	theme: {
		extend: {
			colors: {
				primary: '#6366f1', // Indigo-500
				accent: '#a21caf', // Fuchsia-700
				background: '#0f172a', // Slate-900
				surface: '#1e293b', // Slate-800
				text: '#f1f5f9', // Slate-100
				success: '#22c55e', // Green-500
				warning: '#f59e42', // Orange-400
				error: '#ef4444', // Red-500
			},
		},
	},
	plugins: [],
};
