// frontend/components/api.ts
export const apiBase =
  typeof window === 'undefined'
    ? (process.env.INTERNAL_API_BASE || 'http://api:8000')           // SSR (inside docker)
    : (process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'); // Browser (on your PC)
