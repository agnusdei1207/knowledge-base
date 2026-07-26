import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const docs = defineCollection({
  loader: docsLoader(),
  schema: docsSchema({
    extend: z.object({
      author: z.string().optional(),
      date: z.string().optional(),
      tags: z.array(z.string()).optional(),
      weight: z.number().optional(),
      extra: z
        .object({
          question_no: z.string().optional(),
          source_status: z.string().optional(),
          source_history: z.string().optional(),
          reference_status: z.string().optional(),
          priority: z.number().optional(),
          priority_note: z.string().optional(),
        })
        .optional(),
    }),
  }),
});

export const collections = { docs };
