import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import yaml from 'js-yaml';

export type ClientStatus = 'active' | 'pending' | 'lost' | 'churned';

export type Client = {
  id: string;
  name: string;
  status: ClientStatus;
  mrr: number;
  contact: string;
  domain: string;
  addedAt: string;
  notes?: string;
};

type ClientsFile = { clients: Client[] };

function loadClients(): Client[] {
  // Try multiple locations (build vs runtime, dev vs prod)
  const candidates = [
    join(process.cwd(), 'data', 'clients.yaml'),
    join(process.cwd(), '..', 'data', 'clients.yaml'),
    join('/vercel/path-handler/data', 'clients.yaml'),
  ];
  for (const path of candidates) {
    if (existsSync(path)) {
      const content = readFileSync(path, 'utf-8');
      const parsed = yaml.load(content) as ClientsFile;
      return parsed.clients ?? [];
    }
  }
  return [];
}

// Cached at module load
let cache: Client[] | null = null;
export function getClients(): Client[] {
  if (cache) return cache;
  cache = loadClients();
  return cache;
}
