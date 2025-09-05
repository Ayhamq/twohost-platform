2-Host Frontend (Next.js + Tailwind)

Local dev:
  1) cd frontend
  2) npm install
  3) set NEXT_PUBLIC_API_BASE=http://localhost:8000 (or create .env.local)
  4) npm run dev
  5) open http://localhost:3000

Docker:
  Add this service to docker-compose.yml:

    web:
      build: ./frontend
      environment:
        - NEXT_PUBLIC_API_BASE=http://api:8000
      ports:
        - "3000:3000"
      depends_on:
        - api

Put this folder at ./frontend alongside ./backend in your project root.
