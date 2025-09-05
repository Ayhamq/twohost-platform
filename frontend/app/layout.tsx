import './globals.css';
import Link from 'next/link';

export const metadata = { title: '2-Host Console', description: 'Network IPAM & Automation' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="bg-white border-b">
          <div className="container py-4 flex items-center gap-6">
            <div className="text-xl font-bold">2‑Host Console</div>
            <nav className="flex gap-4">
              <Link className="btn" href="/">Dashboard</Link>
              <Link className="btn" href="/sites">Sites</Link>
              <Link className="btn" href="/devices">Devices</Link>
              <Link className="btn" href="/ipam">IPAM</Link>
            </nav>
          </div>
        </header>
        <main className="container py-8">{children}</main>
      </body>
    </html>
  );
}
