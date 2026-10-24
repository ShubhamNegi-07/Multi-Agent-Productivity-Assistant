# Assistant Hub frontend

This directory is the target workspace for the React migration. The API
contract is currently available in [`src/lib/api.ts`](./src/lib/api.ts).

## Choose a scaffold

### Vite React + TypeScript

From `Main-multi-agent`:

```powershell
npm create vite@latest frontend-app -- --template react-ts
Set-Location frontend-app
npm install
npm install tailwindcss @tailwindcss/vite
npm install -D @types/node
npx shadcn@latest init
npx shadcn@latest add sidebar card scroll-area avatar button input textarea badge dialog tooltip command sheet dropdown-menu
npm run dev
```

For Tailwind CSS v4 with Vite, add the `@tailwindcss/vite` plugin to
`vite.config.ts`, then import Tailwind in `src/index.css`:

```css
@import "tailwindcss";
```

The existing API client can be copied into the generated app with:

```powershell
Copy-Item ..\frontend\src\lib\api.ts src\lib\api.ts
```

### Next.js + TypeScript

From `Main-multi-agent`:

```powershell
npx create-next-app@latest frontend-app --ts --eslint --tailwind --app --src-dir --import-alias "@/*"
Set-Location frontend-app
npx shadcn@latest init
npx shadcn@latest add sidebar card scroll-area avatar button input textarea badge dialog tooltip command sheet dropdown-menu
npm run dev
```

The Next.js starter uses the current Tailwind setup supported by the selected
starter version. Set `NEXT_PUBLIC_API_BASE_URL` when the API is not running on
the default local URL.

## Tailwind CSS v3 alternative

Use this only when the project must remain on Tailwind v3:

```powershell
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

Add the source globs to `tailwind.config.ts`:

```ts
content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"]
```

Then use the v3 directives in `src/index.css` or `src/app/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## API environment variables

Vite:

```powershell
$env:VITE_API_BASE_URL = "http://localhost:8000"
```

Next.js:

```powershell
$env:NEXT_PUBLIC_API_BASE_URL = "http://localhost:8000"
```

The client defaults to `http://localhost:8000` when no variable is provided.
