import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import rehypeKatex from 'rehype-katex';
import remarkCjkFriendly from 'remark-cjk-friendly/parseOnly';
import remarkCjkFriendlyGfmStrikethrough from 'remark-cjk-friendly-gfm-strikethrough/parseOnly';
import remarkMath from 'remark-math';
import mermaid from 'astro-mermaid';

export default defineConfig({
  site: 'https://agnusdei1207.github.io',
  base: '/study',
  integrations: [
    mermaid({
      theme: 'neutral',
      autoTheme: true,
    }),
    starlight({
      title: 'CS Notes',
      description: '컴퓨터 사이언스 핵심 주제를 영역별로 정리한 학습 노트',
      defaultLocale: 'root',
      locales: {
        root: {
          label: '한국어',
          lang: 'ko',
        },
      },
      sidebar: [
        {
          label: '흔들릴 때 다시 읽는 글',
          link: '/encouragement/',
        },
        {
          label: '컴퓨터 사이언스',
          collapsed: true,
          items: [
            {
              autogenerate: {
                directory: 'notes',
                collapsed: true,
              },
            },
          ],
        },
      ],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/agnusdei1207/study',
        },
      ],
      customCss: ['./src/styles/custom.css'],
      components: {
        PageTitle: './src/components/PageTitle.astro',
        Sidebar: './src/components/Sidebar.astro',
      },
      lastUpdated: true,
      pagefind: false,
      head: [
        { tag: 'script', attrs: { src: '/palette-app.js', defer: true } },
      ],
    }),
  ],
  markdown: {
    remarkPlugins: [remarkMath, remarkCjkFriendly, remarkCjkFriendlyGfmStrikethrough],
    rehypePlugins: [rehypeKatex],
  },
});
