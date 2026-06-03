import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkObsidian from '/home/user/knowledgebase/.quartz/plugins/obsidian-flavored-markdown/node_modules/@quartz-community/remark-obsidian/dist/index.js';

const parser = unified().use(remarkParse).use(remarkObsidian.default || remarkObsidian, { wikilinks: true });
const tree = parser.parse('[[176_direct_addressing\\|Direct]]');
console.log(JSON.stringify(tree, null, 2));
