# Sehat AI frontend

Next.js 16 frontend using TypeScript, the App Router, and Tailwind CSS 4.

## Run locally

```powershell
cd application\frontend
npm install
npm run dev
```

Open `http://localhost:3000`. Set `NEXT_PUBLIC_API_BASE_URL` when the FastAPI service is not running at `http://127.0.0.1:8000`.

## Quality commands

```powershell
npm test
npm run typecheck
npm run lint
npm run build
```

Pages are server components unless browser-only behavior requires a client boundary. `components/api-status.tsx` is intentionally client-side because it checks local API readiness after hydration.
