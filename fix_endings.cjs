const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const dir = 'C:\\workspace\\study\\src\\content\\docs\\notes\\08-latest-tech';
const files = fs.readdirSync(dir).filter(f => {
    if (!f.endsWith('.md')) return false;
    const match = f.match(/^(\d+)_/);
    if (!match) return false;
    const num = parseInt(match[1], 10);
    return num >= 151 && num <= 226;
});

console.log(`Found ${files.length} files to process.`);

for (const file of files) {
    const filepath = path.join(dir, file);
    let content = fs.readFileSync(filepath, 'utf-8');
    
    // Rule: Section 7 ending
    const sec7Idx = content.indexOf('## Ⅶ. 결론');
    if (sec7Idx !== -1) {
        let sec7Content = content.substring(sec7Idx);
        let lines = sec7Content.split('\n');
        
        for (let i = lines.length - 1; i >= 0; i--) {
            let line = lines[i].trim();
            if (line.startsWith('-') && (
                line.endsWith('한다.') || line.endsWith('이다.') || 
                line.endsWith('된다.') || line.endsWith('있다.') || line.endsWith('없다.') ||
                line.endsWith('한다') || line.endsWith('이다') || 
                line.endsWith('된다') || line.endsWith('있다') || line.endsWith('없다') ||
                line.endsWith('임.') || line.endsWith('음.') || 
                line.endsWith('임') || line.endsWith('음')
            )) {
                // Determine a sensible noun phrase ending based on content or just fallback
                if (line.includes('적용')) {
                    line = line.replace(/([다임음])\.?$/, ' 체계 적용');
                } else if (line.includes('준수') || line.includes('원칙')) {
                    line = line.replace(/([다임음])\.?$/, ' 원칙 준수');
                } else {
                    line = line.replace(/한다\.?$/, ' 체계 적용');
                    line = line.replace(/이다\.?$/, ' 원칙 준수');
                    line = line.replace(/된다\.?$/, ' 체계 확립');
                    line = line.replace(/있다\.?$/, ' 역량 확보');
                    line = line.replace(/없다\.?$/, ' 리스크 방지');
                    line = line.replace(/임\.?$/, ' 구현 필수');
                    line = line.replace(/음\.?$/, ' 체계 확립');
                }
                
                // Fallback for remaining cases
                line = line.replace(/다\.?$/, ' 필수');
                
                // Fix potential weirdness like "적용 체계 적용"
                line = line.replace(/적용 체계 적용$/, '적용 필수');
                line = line.replace(/준수 원칙 준수$/, '준수 필수');
                
                lines[i] = line;
                break;
            }
        }
        content = content.substring(0, sec7Idx) + lines.join('\n');
    }
    
    fs.writeFileSync(filepath, content, 'utf-8');
}

console.log('Done replacing. Running git commands...');
try {
    execSync('git add -A', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git commit -m "08-latest-tech 151~226: 명사구 종결 교정"', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git push', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    console.log("Git commands completed successfully.");
} catch (e) {
    console.error("Git command failed:", e.message);
}
