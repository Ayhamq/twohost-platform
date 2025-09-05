import Link from 'next/link';
import { apiBase } from '@/components/api';

type Device = {
  id: string; site_id: string; name: string; vendor?: string; model?: string; role?: string; mgmt_ip?: string;
};

async function getDevices(): Promise<Device[]> {
  const res = await fetch(`${apiBase}/devices`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch devices');
  return res.json();
}

export default async function DevicesPage() {
  const devices = await getDevices();
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h1 className="h1">Devices</h1>
        <Link href="/devices/new" className="btn">+ Add Device</Link>
      </div>
      <table className="table">
        <thead><tr><th>Name</th><th>Vendor/Model</th><th>Role</th><th>Mgmt IP</th><th>Site ID</th></tr></thead>
        <tbody>
          {devices.map(d => (
            <tr key={d.id}>
              <td className="font-medium">{d.name}</td>
              <td>{d.vendor || '-'} / {d.model || '-'}</td>
              <td>{d.role || '-'}</td>
              <td>{d.mgmt_ip || '-'}</td>
              <td className="text-slate-500">{d.site_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
