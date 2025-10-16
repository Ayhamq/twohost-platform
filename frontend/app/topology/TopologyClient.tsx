'use client';

import dynamic from 'next/dynamic';
import { useEffect, useState } from 'react';

// avoid SSR for the graph lib
const ForceGraph2D = dynamic(() => import('react-force-graph').then(m => m.ForceGraph2D), { ssr: false });

type Node = { id: string; label: string; group: string };
type Edge = { from: string; to: string; label?: string };

export default function TopologyClient({ initial }: { initial: { nodes: Node[]; edges: Edge[] } }) {
  const [data, setData] = useState(initial);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    // defensive: ensure arrays
    if (!Array.isArray(initial?.nodes) || !Array.isArray(initial?.edges)) {
      setErr('Bad data format from API');
    }
  }, [initial]);

  if (err) return <div className="p-4 text-red-600">{err}</div>;
  if (!data?.nodes?.length && !data?.edges?.length) return <div className="p-4">No topology data yet.</div>;

  return (
    <div className="w-full h-screen bg-white">
      <ForceGraph2D
        graphData={{
          nodes: data.nodes.map(n => ({ id: n.id, name: n.label, group: n.group })),
          links: data.edges.map(e => ({ source: e.from, target: e.to, label: e.label })),
        }}
        nodeLabel={(n: any) => n.name}
        nodeAutoColorBy="group"
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={1}
        linkLabel={(l: any) => l.label}
      />
    </div>
  );
}
