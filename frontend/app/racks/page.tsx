'use client';

import { useEffect, useState } from 'react';

const apiBase =
  typeof window === 'undefined'
    ? process.env.INTERNAL_API_BASE || 'http://api:8000'
    : process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

type Rack = { id: string; site_id: string; name: string; u_height: number };
type Site = { id: string; name: string; slug: string };

export default function RacksPage() {
  const [racks, setRacks] = useState<Rack[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [form, setForm] = useState({ site_id: '', name: '', u_height: 42 });
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      const [rRes, sRes] = await Promise.all([
        fetch(`${apiBase}/racks`, { cache: 'no-store' }),
        fetch(`${apiBase}/sites`, { cache: 'no-store' }),
      ]);
      if (!rRes.ok) throw new Error('Failed to fetch racks');
      if (!sRes.ok) throw new Error('Failed to fetch sites');
      setRacks(await rRes.json());
      setSites(await sRes.json());
    } catch (e: any) {
      setError(e.message || 'Failed to load');
    }
  }

  useEffect(() => { load(); }, []);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch(`${apiBase}/racks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(await res.text());
      setForm({ site_id: '', name: '', u_height: 42 });
      load();
    } catch (e: any) {
      setError(e.message || 'Failed to create rack');
    }
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Racks</h1>

      <form onSubmit={onCreate} className="grid gap-3 max-w-xl border rounded-xl p-4">
        <div>
          <label className="block text-sm mb-1">Site</label>
          <select
            className="border rounded px-3 py-2 w-full"
            value={form.site_id}
            onChange={(e) => setForm({ ...form, site_id: e.target.value })}
            required
          >
            <option value="">Select site…</option>
            {sites.map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm mb-1">Name</label>
          <input
            className="border rounded px-3 py-2 w-full"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            placeholder="R01"
            required
          />
        </div>

        <div>
          <label className="block text-sm mb-1">Height (U)</label>
          <input
            type="number"
            min={1}
            className="border rounded px-3 py-2 w-full"
            value={form.u_height}
            onChange={(e) => setForm({ ...form, u_height: Number(e.target.value) || 42 })}
            required
          />
        </div>

        <button className="bg-black text-white rounded px-4 py-2 w-fit">Create Rack</button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
      </form>

      <div className="grid gap-3">
        {racks.length === 0 && <p className="text-gray-500">No racks yet.</p>}
        {racks.map((r) => (
          <div key={r.id} className="border rounded-xl p-4">
            <div className="font-medium">{r.name}</div>
            <div className="text-sm text-gray-600">Site: {r.site_id}</div>
            <div className="text-sm text-gray-600">Height: {r.u_height}U</div>
          </div>
        ))}
      </div>
    </div>
  );
}
