const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, 'src', 'content', 'docs', 'notes', '08-latest-tech');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && f !== 'index.md');

const endings = ['을 의미한다.', '로 정의된다.', '을 말한다.', '이다.'];

function diversifyEndings(text) {
    let lines = text.split('\n');
    let insideTerms = false;
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('<summary>핵심 용어</summary>')) insideTerms = true;
        if (insideTerms && lines[i].includes('</details>')) insideTerms = false;
        
        if (insideTerms && lines[i].trim().startsWith('- **')) {
            if (lines[i].endsWith('이다.\r') || lines[i].endsWith('이다.')) {
                let randomEnding = endings[Math.floor(Math.random() * endings.length)];
                lines[i] = lines[i].replace(/이다\.(\r?)$/, randomEnding + '$1');
            }
        }
    }
    return lines.join('\n');
}

function nounPhraseEndings(text) {
    let lines = text.split('\n');
    let insideTerms = false;
    let insideSummary = false;
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('<summary>핵심 용어</summary>')) insideTerms = true;
        if (insideTerms && lines[i].includes('</details>')) insideTerms = false;
        
        if (lines[i].includes('#### 한줄 요약')) insideSummary = true;
        if (insideSummary && lines[i].startsWith('## ')) insideSummary = false;
        
        if (!insideTerms && !insideSummary) {
            if (lines[i].trim().startsWith('- ') || lines[i].match(/^[0-9]+\. /)) {
                lines[i] = lines[i].replace(/한다\.(\r?)$/, '함.$1');
                lines[i] = lines[i].replace(/이다\.(\r?)$/, '임.$1');
                lines[i] = lines[i].replace(/다\.(\r?)$/, '음.$1');
            }
        }
    }
    return lines.join('\n');
}

function shortenAndEnglish(text) {
    let lines = text.split('\n');
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].trim().startsWith('- ')) {
            let parts = lines[i].split('. ');
            if (parts.length > 2) {
                let end = parts[1].endsWith('.') || parts[1].endsWith('.\r') ? '' : '.';
                let carriage = lines[i].endsWith('\r') ? '\r' : '';
                lines[i] = parts[0] + '. ' + parts[1] + end + carriage;
            }
        }
    }
    return lines.join('\n');
}

for (const file of files) {
    const filePath = path.join(dir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    content = shortenAndEnglish(content);
    content = diversifyEndings(content);
    content = nounPhraseEndings(content);
    
    fs.writeFileSync(filePath, content, 'utf8');
}
console.log(`Processed ${files.length} files successfully.`);
