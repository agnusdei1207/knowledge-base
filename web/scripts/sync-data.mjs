// Copy data/ from repo root into web/data/ before dev/build
import { cpSync, existsSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = resolve(__dirname, '..', '..', 'data');
const dest = resolve(__dirname, '..', 'data');

if (!existsSync(src)) {
  console.error(`[sync-data] source not found: ${src}`);
  process.exit(1);
}
if (!existsSync(dest)) mkdirSync(dest, { recursive: true });
cpSync(src, dest, { recursive: true, filter: (s) => !s.includes('_schema') });
console.log(`[sync-data] copied ${src} → ${dest}`);
