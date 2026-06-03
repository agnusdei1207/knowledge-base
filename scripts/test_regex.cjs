const fs = require('fs');
const src = fs.readFileSync('/home/user/knowledgebase/content/studynote/01_computer_architecture/08_io_storage_systems/339_das.md', 'utf-8');

const calloutLineRegex = /^> *\[!\w+\|?.*?\][+-]?.*$/gm;
let transformed = src.replace(calloutLineRegex, (value) => {
  return value + '\n> ';
});

transformed = transformed.replace(/!?\[\[([^\]]+)\]\]/g, (match, content) => {
  const escapedContent = content.replace(/(?<!\\)\|/g, '\\|');
  const isEmbed = match.startsWith('!');
  return (isEmbed ? '!' : '') + '[[' + escapedContent + ']]';
});

const lines = transformed.split('\n');
const tableLines = lines.filter(l => l.includes('| 항목 |'));
console.log('Table lines found:', tableLines.length);
const index = lines.findIndex(l => l.includes('DAS를 제대로 이해하려면'));
if (index !== -1) {
  console.log('Lines around table:');
  console.log(lines.slice(index, index + 8).join('\n'));
}
