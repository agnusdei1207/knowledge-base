const fs = require('fs');
const path = require('path');

const dir = __dirname;
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md') && f !== 'index.md');

const endings = ['을 의미한다.', '로 정의된다.', '을 말한다.', '이다.'];

function diversifyEndings(text) {
    let lines = text.split('\n');
    let insideTerms = false;
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('<summary>핵심 용어</summary>')) {
            insideTerms = true;
        }
        if (insideTerms && lines[i].includes('</details>')) {
            insideTerms = false;
        }
        
        if (insideTerms && lines[i].trim().startsWith('- **')) {
            if (lines[i].endsWith('이다.')) {
                let randomEnding = endings[Math.floor(Math.random() * endings.length)];
                // Make sure to match the grammatical structure loosely
                lines[i] = lines[i].replace(/이다\.$/, randomEnding);
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
        
        // Also skip YAML frontmatter
        if (i < 20 && lines[i] === '---') {
            // Very simple frontmatter skip
        }
        
        if (!insideTerms && !insideSummary) {
            // Change line endings to noun phrases
            if (lines[i].trim().startsWith('- ') || lines[i].match(/^[0-9]+\. /)) {
                if (lines[i].endsWith('한다.')) {
                    lines[i] = lines[i].replace(/한다\.$/, '함.');
                } else if (lines[i].endsWith('이다.')) {
                    lines[i] = lines[i].replace(/이다\.$/, '임.');
                } else if (lines[i].endsWith('다.')) {
                    lines[i] = lines[i].replace(/다\.$/, '음.');
                }
            }
        }
    }
    return lines.join('\n');
}

function shortenAndEnglish(text) {
    // Basic shortening: remove text after second sentence in bullet points
    let lines = text.split('\n');
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].trim().startsWith('- ')) {
            let sentences = lines[i].split('. ');
            if (sentences.length > 2) {
                lines[i] = sentences[0] + '. ' + sentences[1] + (sentences[1].endsWith('.') ? '' : '.');
            }
            
            // English check inside terms
            if (lines[i].includes('**') && lines[i].includes(':')) {
                let match = lines[i].match(/\*\*(.*?)\*\*/);
                if (match && !match[1].includes('(') && !match[1].includes('English')) {
                    // Add a placeholder or try to infer, but safest is to just leave it if we can't translate
                    // We'll just leave it to not break terminology, assuming most have it or we manually edit.
                }
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

console.log(`Processed ${files.length} files.`);
