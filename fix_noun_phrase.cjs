const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const dir = path.join('C:', 'workspace', 'study', 'src', 'content', 'docs', 'notes', '08-latest-tech');
const files = fs.readdirSync(dir).filter(f => f.match(/^0[0-7][0-9]_.*\.md$/) && f >= '001_' && f <= '075_');

function fixSentence(sentence) {
    let s = sentence.trim();
    // If it already ends with a noun phrase ending, skip
    if (!s.match(/[가-힣]다\.?$/) && !s.match(/[가-힣]다\.?\s*체계 적용$/)) {
        // If it ended with something like "체계 적용" already, just return
        return s;
    }
    
    // Remove trailing dot and " 체계 적용" if they mistakenly appended it
    s = s.replace(/\.?\s*체계 적용$/, '');
    s = s.replace(/\.$/, '');

    // Now it ends with "다"
    if (s.endsWith('한다')) {
        s = s.replace(/한다$/, ' 체계 적용');
    } else if (s.endsWith('이다')) {
        s = s.replace(/이다$/, ' 구조 구현');
    } else if (s.endsWith('된다')) {
        s = s.replace(/된다$/, ' 체계 구축');
    } else if (s.endsWith('다')) {
        // Generic verb ending e.g. "줄인다", "멈춥니다"
        s = s.slice(0, -1) + ' 기전 적용';
    }

    return s;
}

let changedFiles = 0;

files.forEach(f => {
    const filepath = path.join(dir, f);
    const content = fs.readFileSync(filepath, 'utf8');
    const lines = content.split('\n');
    let changed = false;
    
    let inSummary = false;
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('#### 한줄 요약')) {
            inSummary = true;
            continue;
        }
        
        if (inSummary && lines[i].trim().startsWith('-')) {
            const original = lines[i];
            const prefix = original.match(/^(\s*-\s+)(.*)$/);
            if (prefix) {
                const text = prefix[2];
                // Check if it's a verb ending
                if (text.match(/[다요]\.?(\s*체계 적용)?$/)) {
                    const fixed = fixSentence(text);
                    if (fixed !== text) {
                        lines[i] = prefix[1] + fixed;
                        changed = true;
                    }
                }
            }
            // After the first bullet, we assume the summary block ends when an empty line or another header appears, 
            // but just to be safe we only check lines that start with '-' immediately following.
        } else if (inSummary && lines[i].trim() === '') {
            // empty line is ok, might be another bullet
        } else if (inSummary && !lines[i].trim().startsWith('-')) {
            inSummary = false;
        }
    }
    
    if (changed) {
        fs.writeFileSync(filepath, lines.join('\n'), 'utf8');
        changedFiles++;
        console.log(`Fixed ${f}`);
    }
});

console.log(`Total changed: ${changedFiles}`);

try {
    execSync('git add -A', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git commit -m "08-latest-tech 001~075: 명사구 종결 교정"', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git push', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    console.log("Git push done.");
} catch(e) {
    console.error("Git error", e.message);
}
