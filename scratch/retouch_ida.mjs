import fs from 'fs';
import path from 'path';

const dirs = [
  'C:/workspace/study/src/content/docs/notes/06-evaluation',
  'C:/workspace/study/src/content/docs/notes/07-law-policy',
  'C:/workspace/study/src/content/docs/notes/08-latest-tech'
];

let updatedCount = 0;

for (const dir of dirs) {
  if (!fs.existsSync(dir)) continue;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && f !== 'index.md');
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let lines = content.split('\n');
    let modified = false;
    
    // Find Section I
    let inSec1 = false;
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].startsWith('## Ⅰ. 개요')) {
        inSec1 = true;
        continue;
      }
      if (inSec1 && lines[i].startsWith('## ')) {
        inSec1 = false;
        break;
      }
      
      // Look for the definition line
      if (inSec1 && lines[i].trim().match(/^-\s*정의(?:\/개념)?\s*:/)) {
        let line = lines[i];
        
        // Target: "- 정의: **[주제어]**는 [설명]이다."
        let match = line.match(/^-\s*정의(?:\/개념)?\s*:\s*(\*\*[^*]+\*\*)(?:의|이|가|은|는|이란|란)?\s*(.*)/);
        if (match) {
          let subject = match[1];
          let rest = match[2];
          
          if (!rest.startsWith('는 ') && !rest.startsWith('은 ')) {
             rest = rest.trim();
             line = `- 정의: ${subject}는 ${rest}`;
          } else {
             line = `- 정의: ${subject}${rest}`;
          }
        } else {
          // If no **subject** at the beginning, we might just have text.
          // In that case, we can't easily auto-fix the subject, but we can fix the ending.
          line = line.replace(/^-\s*정의(?:\/개념)?\s*:/, '- 정의:');
        }
        
        // Remove ending dot if present temporarily
        line = line.replace(/\.$/, '').trim();
        
        // Ensure it ends with "이다"
        if (!line.endsWith('이다') && !line.endsWith('한다')) { // "한다" is also a valid verb ending
          // Sometimes it ends with noun. We append "이다"
          // If it ends with "이다" or "한다", we don't change.
          // Wait, if it doesn't end with "이다", we append it.
          if (!line.match(/(이다|한다|됨|음|함|다)$/)) {
            line = line + '이다';
          } else if (line.endsWith('다') && !line.endsWith('이다') && !line.endsWith('한다')) {
            // Already ends with 다
          } else if (line.match(/(됨|음|함)$/)) {
            // "되는 것이다" etc. Actually just leave "이다" append.
            // But let's just forcefully append 이다 if it doesn't end with "다"
          }
        }
        
        // Wait, the user explicitly wants "이다".
        if (!line.endsWith('이다')) {
            // If it ends with a noun like 체계, 방식, 기법.
            // Just append 이다.
            if (!line.endsWith('다')) {
               line = line + '이다';
            }
        }
        
        // Put the dot back
        line = line + '.';
        
        if (lines[i] !== line) {
          lines[i] = line;
          modified = true;
        }
      }
    }
    
    if (modified) {
      fs.writeFileSync(filePath, lines.join('\n'), 'utf8');
      updatedCount++;
      console.log(`Updated: ${filePath}`);
    }
  }
}

console.log(`Total files updated: ${updatedCount}`);
