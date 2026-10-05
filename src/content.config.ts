import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Articles du blog : un fichier .mdx par article dans src/content/blog/.
// `ressource` = guide gratuit mis en avant (clé de src/data/ressources.ts).
const blog = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog' }),
  schema: ({ image }) =>
    z.object({
    // Balise <title> (≈ 60 caractères, mot-clé en tête) ; h1 = titre affiché, plus naturel.
    title: z.string(),
    h1: z.string().optional(),
    description: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    ressource: z.enum(['checklist-retroplanning', 'livret-jeux']).default('checklist-retroplanning'),
    categorie: z.string().default('Organisation'),
    tempsLecture: z.number().optional(),
    draft: z.boolean().default(false),
    // Photo de l'article : vignette de la liste + image du haut de l'article.
    image: image().optional(),
    imageAlt: z.string().default(''),
    // Questions fréquentes affichées en fin d'article + balisage FAQPage.
    faq: z.array(z.object({ q: z.string(), r: z.string() })).default([]),
  }),
});

export const collections = { blog };
