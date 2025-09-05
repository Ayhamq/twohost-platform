'use client';
import { useState } from 'react';
import { apiBase } from '@/components/api';
import Link from 'next/link';

export default function NewSitePage() {
  const [name, setName] = useState('');
  const [slug, setSlug] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('Saving...');
    try {
      const res = await fetch(`${apiBase}/sites`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, slug }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Failed to create site');
      }
      setStatus('Site created ✅');
      setName(''); setSlug('');
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h1 className="h1">New Site</h1>
        <Link href="/sites" className="btn">← Back</Link>
      </div>
      <form onSubmit={onSubmit} className="space-y-4 max-w-md">
        <div>
          <label className="block text-sm font-medium">Name</label>
          <input value={name} onChange={e=>setName(e.target.value)} required className="w-full border rounded-xl p-2" placeholder="Malmö DC" />
        </div>
        <div>
          <label className="block text-sm font-medium">Slug</label>
          <input value={slug} onChange={e=>setSlug(e.target.value)} required pattern="^[a-z0-9-]+$" className="w-full border rounded-xl p-2" placeholder="malmo-dc" />
          <p className="text-xs text-slate-500 mt-1">Lowercase letters, numbers, hyphen.</p>
        </div>
        <button className="btn" type="submit">Create Site</button>
        {status && <p className="text-sm mt-2">{status}</p>}
      </form>
    </div>
  );
}
