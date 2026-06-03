const unified = require('unified');
const remarkParse = require('remark-parse');
const remarkObsidian = require('/home/user/knowledgebase/.quartz/plugins/obsidian-flavored-markdown/node_modules/@quartz-community/remark-obsidian/dist/index.js').default;

const parser = unified().use(remarkParse).use(remarkObsidian, { wikilinks: true });
const tree = parser.parse('[[176_direct_addressing\\|Direct]]');
console.log(JSON.stringify(tree, null, 2));
