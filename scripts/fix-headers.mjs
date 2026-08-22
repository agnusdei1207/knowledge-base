import { readdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const notesDir = 'C:\\workspace\\study\\src\\content\\docs\\notes';

async function getMarkdownFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await getMarkdownFiles(fullPath)));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }
  return files;
}

async function fixFile(filePath) {
  let content = await readFile(filePath, 'utf-8');
  let original = content;

  // Fix 02-hardware/059_water_usage_effectiveness.md broken formula
  content = content.replace(
    '\\text{순수 IT 장비 전력 소비량 (IT Eq#### 한줄 요약',
    '\\text{순수 IT 장비 전력 소비량 (IT Equipment Energy, kWh)}}\n\\end{aligned}\n$$\n\n#### 한줄 요약'
  );

  // Fix inline #### 한줄 요약
  content = content.replace(/([^\n])\s*#### 한줄 요약/g, '$1\n\n#### 한줄 요약');

  // Fix inline ## [Ⅰ-Ⅶ]
  content = content.replace(/([^\n])\s*(##\s+[Ⅰ-Ⅶ]\.\s+[^\n]+)/g, '$1\n\n$2');

  if (content !== original) {
    await writeFile(filePath, content, 'utf-8');
    return true;
  }
  return false;
}

async function main() {
  const files = await getMarkdownFiles(notesDir);
  let fixedCount = 0;
  for (const file of files) {
    const fixed = await fixFile(file);
    if (fixed) fixedCount++;
  }
  console.log(`Total files fixed for headers: ${fixedCount}`);
}

main().catch(console.error);
