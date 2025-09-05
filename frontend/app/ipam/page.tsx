import { apiBase } from '@/components/api';

type VRF = { id: string; name: string; rd?: string | null };
type VLAN = { id: string; site_id: string; vid: number; name?: string | null };
type Prefix = { id: string; vrf_id?: string | null; cidr: string; description?: string | null };
type IP = { id: string; vrf_id?: string | null; address: string; dns_name?: string | null };

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${apiBase}${path}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed: ${path}`);
  return res.json();
}

export default async function IPAMPage() {
  const [vrfs, vlans, prefixes, ips] = await Promise.all([
    fetchJSON<VRF[]>('/ipam/vrfs'),
    fetchJSON<VLAN[]>('/ipam/vlans'),
    fetchJSON<Prefix[]>('/ipam/prefixes'),
    fetchJSON<IP[]>('/ipam/ip-addresses'),
  ]);

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <section className="card">
        <h2 className="h2 mb-2">VRFs</h2>
        <table className="table">
          <thead><tr><th>Name</th><th>RD</th><th>ID</th></tr></thead>
          <tbody>{vrfs.map(v => (<tr key={v.id}><td>{v.name}</td><td>{v.rd || '-'}</td><td className="text-slate-500">{v.id}</td></tr>))}</tbody>
        </table>
      </section>

      <section className="card">
        <h2 className="h2 mb-2">VLANs</h2>
        <table className="table">
          <thead><tr><th>Site</th><th>VID</th><th>Name</th><th>ID</th></tr></thead>
          <tbody>{vlans.map(v => (<tr key={v.id}><td className="text-slate-500">{v.site_id}</td><td>{v.vid}</td><td>{v.name || '-'}</td><td className="text-slate-500">{v.id}</td></tr>))}</tbody>
        </table>
      </section>

      <section className="card">
        <h2 className="h2 mb-2">Prefixes</h2>
        <table className="table">
          <thead><tr><th>CIDR</th><th>VRF</th><th>Description</th><th>ID</th></tr></thead>
          <tbody>{prefixes.map(p => (<tr key={p.id}><td>{p.cidr}</td><td className="text-slate-500">{p.vrf_id || '-'}</td><td>{p.description || '-'}</td><td className="text-slate-500">{p.id}</td></tr>))}</tbody>
        </table>
      </section>

      <section className="card">
        <h2 className="h2 mb-2">IP Addresses</h2>
        <table className="table">
          <thead><tr><th>IP</th><th>VRF</th><th>DNS</th><th>ID</th></tr></thead>
          <tbody>{ips.map(ip => (<tr key={ip.id}><td>{ip.address}</td><td className="text-slate-500">{ip.vrf_id || '-'}</td><td>{ip.dns_name || '-'}</td><td className="text-slate-500">{ip.id}</td></tr>))}</tbody>
        </table>
      </section>
    </div>
  );
}
