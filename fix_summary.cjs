const fs = require('fs');
const path = require('path');

function fixSummary(filepath) {
    let content = fs.readFileSync(filepath, 'utf8');

    const conclusionRegex = /(## Ⅶ\. 결론.*?#### 한줄 요약\n- )(.*)/s;
    content = content.replace(conclusionRegex, (match, p1, p2) => {
        let summary = p2;
        
        // Remove trailing " 체계 적용" or " 체계 확립" if it was added
        summary = summary.replace(/ 체계 (적용|확립)$/, '');
        
        // Strip out the broken "한다", "이다" etc.
        summary = summary.replace(/(한다\.|이다\.|함\.|임\.|한다|이다|함|임|\.)+$/g, '').trim();
        
        if (summary.endsWith('검증')) {
            summary += ' 체계 확립';
        } else if (!summary.match(/(적용|준수|필수|설계|구현|검증|확보|통제|체계|방안|기반|지침|강화|수립|방식)$/)) {
            summary += ' 체계 적용';
        }
        return p1 + summary;
    });

    fs.writeFileSync(filepath, content, 'utf8');
}

const folderPath = path.join(__dirname, "src/content/docs/notes/08-latest-tech");
const files = fs.readdirSync(folderPath);
let count = 0;
for (const file of files) {
    if (file.match(/0[0-7][0-9]_.*\.md/)) {
        const num = parseInt(file.split('_')[0], 10);
        if (num >= 1 && num <= 75) {
            fixSummary(path.join(folderPath, file));
            count++;
        }
    }
}
console.log(`Fixed ${count} files.`);
