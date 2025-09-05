import Link from 'next/link';
import { apiBase } from '@/components/api';

type Site = { id: string; name: string; slug: string; };

async function getSites(): Promise<Site[]> {
  const res = await fetch(`${apiBase}/sites`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch sites');
  return res.json();
}

export default async function SitesPage() {
  const sites = await getSites();
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h1 className="h1">Sites</h1>
        <Link href="/sites/new" className="btn">+ Add Site</Link>
      </div>
      <table className="table">
        <thead><tr><th>Name</th><th>Slug</th><th>ID</th></tr></thead>
        <tbody>
          {sites.map(s => (
            <tr key={s.id}>
              <td>{s.name}</td>
              <td><span className="badge">{s.slug}</span></td>
              <td className="text-slate-500">{s.id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
