import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    lang: z.enum(['zh', 'en']).default('zh'),
    readingTime: z.string().optional(),
    tags: z.array(z.string()).default([]),
    heroEyebrow: z.string().optional(),
    heroSnippet: z.string().optional(),
    heroCtaLabel: z.string().optional(),
    heroCtaHref: z.string().optional(),
    heroCtaPill: z.string().optional(),
    heroImage: z.string().optional(),
    sidebarHighlights: z.array(z.string()).optional(),
    faq: z
      .array(
        z.object({
          question: z.string(),
          answer: z.string(),
        }),
      )
      .optional(),
  }),
});

export const collections = { articles };

