export default function Page() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      <section className="card">
        <h2 className="h2 mb-2">Welcome</h2>
        <p className="text-sm text-slate-600">This is the 2‑Host web console. Use the navigation to manage sites, devices, and IPAM.</p>
      </section>
      <section className="card">
        <h2 className="h2 mb-2">Quick Links</h2>
        <ul className="list-disc ml-5 text-sm">
          <li>Sites: add your locations first.</li>
          <li>Devices: register switches/routers and mgmt IPs.</li>
          <li>IPAM: VRFs, VLANs, Prefixes, and IPs.</li>
        </ul>
      </section>
    </div>
  );
}
