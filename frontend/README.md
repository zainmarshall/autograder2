# TJCT Grader Frontend

A modern SvelteKit frontend for the TJ Computer Team Grader system, featuring clean Svelte syntax with runes and Tailwind CSS styling.

## Features

- **Home Page**: Landing page with "Enter" button for authentication
- **Profile Page**: User profile management with USACO division and Codeforces handle settings
- **User Authentication**: Integration with Django backend authentication
- **Responsive Design**: Modern UI with Tailwind CSS
- **TypeScript**: Full TypeScript support for better development experience

## Tech Stack

- **Framework**: SvelteKit 2.x with Svelte 5 (runes)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Build Tool**: Vite
- **Backend**: Django REST API

## Development Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Django backend running on port 8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Integration

The frontend is configured to proxy API calls to the Django backend running on `http://localhost:8000`. Make sure the Django server is running with CORS enabled.

### Key Files

- `src/lib/user.ts` - User store and authentication logic
- `src/routes/+page.svelte` - Home page with login button
- `src/routes/profile/+page.svelte` - User profile page
- `src/routes/+layout.svelte` - Main layout with global styling

## API Endpoints

The frontend communicates with these Django endpoints:

- `GET /api/user/` - Get current user data
- `POST /oauth/logout/` - Logout user
- `POST /update_stats/` - Update user statistics
- `GET /social/login/ion/` - ION OAuth login

## Building for Production

```bash
npm run build
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run check` - TypeScript and Svelte checks
