# Tailwind Usage and Structure in /routes

## 1. Layouts and Main Containers
- `min-h-screen`, `flex`, `items-center`, `justify-center`, `bg-black`, `px-4`, `py-8`, `min-h-[70vh]`, `w-full`, `max-w-md`, `max-w-2xl`, `max-w-3xl`, `max-w-xl`, `mx-4`, `rounded-lg`, `rounded-2xl`, `rounded-full`, `shadow-lg`, `shadow-xl`, `border`, `border-slate-800`, `border-zinc-300`, `dark:border-zinc-700`, `bg-white/80`, `dark:bg-zinc-900/90`, `bg-zinc-800`, `bg-slate-900`, `bg-gradient-to-br`, `from-indigo-400`, `to-blue-600`, `bg-yellow-100`, `border-l-4`, `border-yellow-500`, `bg-transparent`, `space-y-3`, `gap-6`, `flex-col`, `flex-row`, `items-start`, `items-center`, `justify-between`, `min-w-0`, `mt-1`, `mt-2`, `mt-4`, `mt-8`, `mb-2`, `mb-4`, `mb-6`, `mb-8`, `p-2`, `p-4`, `p-8`, `pt-8`, `px-2`, `px-3`, `px-4`, `py-2`, `py-3`, `py-6`, `py-8`, `w-24`, `h-24`, `font-mono`

## 2. Headings and Text
- `text-3xl`, `text-2xl`, `text-xl`, `text-4xl`, `font-bold`, `font-semibold`, `font-medium`, `tracking-tight`, `select-none`, `text-slate-100`, `text-slate-400`, `text-zinc-100`, `text-zinc-200`, `text-zinc-400`, `text-zinc-500`, `text-zinc-700`, `text-zinc-800`, `text-zinc-900`, `dark:text-zinc-100`, `dark:text-zinc-200`, `dark:text-zinc-400`, `dark:text-zinc-800`, `text-white`, `text-blue-700`, `text-blue-400`, `text-pink-400`, `text-red-400`, `text-red-500`, `text-yellow-900`, `text-base`, `text-sm`, `text-xs`, `text-center`, `font-bowld`

## 3. Buttons and Links
- `bg-indigo-600`, `hover:bg-indigo-700`, `hover:bg-indigo-800`, `text-white`, `font-semibold`, `py-2`, `py-3`, `px-4`, `px-6`, `rounded-lg`, `transition-colors`, `w-full`, `mt-4`, `mb-2`, `disabled:bg-indigo-800`, `hover:underline`, `underline`, `hover:text-indigo-400`, `hover:text-blue-400`, `hover:text-blue-700`, `text-indigo-400`, `text-blue-700`, `text-blue-400`

## 4. Cards and Panels
- `rounded-lg`, `rounded-2xl`, `shadow-lg`, `shadow-xl`, `bg-white/80`, `dark:bg-zinc-900/90`, `border`, `border-slate-800`, `border-zinc-300`, `dark:border-zinc-700`, `p-4`, `p-8`, `md:p-8`, `my-`, `mb-4`, `mb-6`, `mb-8`, `max-w-md`, `max-w-2xl`, `max-w-3xl`, `max-w-xl`, `w-full`, `flex`, `flex-col`, `flex-row`, `items-center`, `items-start`, `justify-between`, `space-y-3`, `gap-6`, `bg-slate-900`, `bg-zinc-800`, `bg-gradient-to-br`, `from-indigo-400`, `to-blue-600`, `bg-yellow-100`, `border-l-4`, `border-yellow-500`, `bg-transparent`

## 5. Forms and Inputs
- `block`, `mb-2`, `mb-4`, `px-3`, `py-2`, `rounded`, `border`, `border-zinc-300`, `dark:border-zinc-700`, `text-white`, `bg-zinc-800`, `focus:border-indigo-500`, `focus:outline-none`, `w-full`, `mt-4`, `space-y-4`, `disabled:bg-indigo-800`

## 6. Miscellaneous
- `prose`, `max-w-none`, `font-mono`, `shadow-md`, `bg-slate-800`, `rounded`, `rounded-xl`, `rounded-2xl`, `rounded-full`, `text-center`, `text-left`, `text-base`, `text-sm`, `text-xs`, `mt-1`, `mt-2`, `mt-4`, `mt-8`, `mb-2`, `mb-4`, `mb-6`, `mb-8`, `p-2`, `p-4`, `p-8`, `pt-8`, `px-2`, `px-3`, `px-4`, `py-2`, `py-3`, `py-6`, `py-8`, `w-24`, `h-24`, `font-bowld`

---

## Usage Contexts
- **Main containers/pages:** layout, error, login, submit, profile, problems, contests, rankings, standings, submissions
- **Cards/panels:** for grouping content, user info, problem info, contest info, etc.
- **Headings:** page titles, section titles, user names, problem names
- **Buttons/links:** actions (login, submit, edit, etc.), navigation, external links
- **Forms/inputs:** language select, user info edit, submission forms
- **Text/labels:** info, descriptions, error messages, meta info

---

## Next Steps
- Review and standardize repeated structures (cards, headings, buttons, forms, etc.)
- Consider extracting common classes into reusable components or Tailwind @apply utilities.
- See this file for a full list of all classes and their usage context.
