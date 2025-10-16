import TopologyClient from './TopologyClient';

type Node = { id: string; label: string; group: string };
type Edge = { from: string; to: string; label?: string };

async function getTopology() {
  const base = process.env.INTERNAL_API_BASE || 'http://api:8000';
  const res = await fetch(`${base}/topology`, { cache: 'no-store' });

  if (!res.ok) {
    // Let Next show a clear error page (and log status)
    throw new Error(`Failed to fetch topology: ${res.status}`);
  }

  const json = await res.json();
  // light validation
  return {
    nodes: Array.isArray(json.nodes) ? json.nodes : [],
    edges: Array.isArray(json.edges) ? json.edges : [],
  } as { nodes: Node[]; edges: Edge[] };
}

export default async function Page() {
  const initial = await getTopology();
  return <TopologyClient initial={initial} />;
}
