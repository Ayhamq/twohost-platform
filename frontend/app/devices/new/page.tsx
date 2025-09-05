'use client';
import { useState, useEffect } from 'react';
import { apiBase } from '@/components/api';
import Link from 'next/link';

type Site = { id: string; name: string; slug: string; };

export default function NewDevicePage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [siteId, setSiteId] = useState('');
  const [name, setName] = useState('');
  const [vendor, setVendor] = useState('');
  const [model, setModel] = useState('');
  const [role, setRole] = useState('');
  const [mgmtIp, setMgmtIp] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${apiBase}/sites`).then(r => r.json()).then(setSites).catch(() => setSites([]));
  }, []);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus('Saving...');
    try {
      const res = await fetch(`${apiBase}/devices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          site_id: siteId || null,
          name,
          vendor: vendor || null,
          model: model || null,
          role: role || null,
          mgmt_ip: mgmtIp || null,
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Failed to create device');
      }
      setStatus('Device created ✅');
      setName(''); setVendor(''); setModel(''); setRole(''); setMgmtIp('');
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h1 className="h1">New Device</h1>
        <Link href="/devices" className="btn">← Back</Link>
      </div>
      <form onSubmit={onSubmit} className="space-y-4 max-w-md">
        <div>
          <label className="block text-sm font-medium">Site</label>
          <select value={siteId} onChange={e=>setSiteId(e.target.value)} required className="w-full border rounded-xl p-2">
            <option value="">Select a site…</option>
            {sites.map(s => <option key={s.id} value={s.id}>{s.name} ({s.slug})</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium">Name</label>
          <input value={name} onChange={e=>setName(e.target.value)} required className="w-full border rounded-xl p-2" placeholder="sw-core-01" />
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium">Vendor</label>
            <input value={vendor} onChange={e=>setVendor(e.target.value)} className="w-full border rounded-xl p-2" placeholder="cisco" />
          </div>
          <div>
            <label className="block text-sm font-medium">Model</label>
            <input value={model} onChange={e=>setModel(e.target.value)} className="w-full border rounded-xl p-2" placeholder="C9300-48" />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium">Role</label>
            <input value={role} onChange={e=>setRole(e.target.value)} className="w-full border rounded-xl p-2" placeholder="core / dist / access" />
          </div>
          <div>
            <label className="block text-sm font-medium">Mgmt IP</label>
            <input value={mgmtIp} onChange={e=>setMgmtIp(e.target.value)} className="w-full border rounded-xl p-2" placeholder="10.0.0.10" />
          </div>
        </div>
        <button className="btn" type="submit">Create Device</button>
        {status && <p className="text-sm mt-2">{status}</p>}
      </form>
    </div>
  );
}
