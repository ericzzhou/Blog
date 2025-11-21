// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import rehypeRaw from 'rehype-raw';

// https://astro.build/config
export default defineConfig({
  site: 'https://zhouzk.com',
  integrations: [mdx()],
  markdown: {
    rehypePlugins: [rehypeRaw],
  },
});
