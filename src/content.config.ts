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
    ressource: z.enum(['checklist-retroplanning', 'livret-jeux', 'annuaire-lieux', 'carnet-musical']).default('checklist-retroplanning'),
    categorie: z.string().default('Organisation'),
    // Public visé : sert aux filtres de /conseils/ et au bloc de fin d'article.
    public: z.enum(['mariage', 'entreprises', 'bars-restaurants']).default('mariage'),
    tempsLecture: z.number().optional(),
    draft: z.boolean().default(false),
    // Photo de l'article : vignette de la liste + image du haut de l'article.
    image: image().optional(),
    imageAlt: z.string().default(''),
    // Questions fréquentes affichées en fin d'article + balisage FAQPage.
    faq: z.array(z.object({ q: z.string(), r: z.string() })).default([]),
  }),
});

// Version anglaise du blog (/en/tips/) : un article adapté par article français (`fr` = son slug).
// Pas de guide à télécharger : les guides PDF n'existent qu'en français.
const blogEn = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/blog-en' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      h1: z.string().optional(),
      description: z.string(),
      date: z.coerce.date(),
      updated: z.coerce.date().optional(),
      fr: z.string(),
      categorie: z.string().default('Planning'),
      public: z.enum(['mariage', 'entreprises', 'bars-restaurants']).default('mariage'),
      tempsLecture: z.number().optional(),
      draft: z.boolean().default(false),
      image: image().optional(),
      imageAlt: z.string().default(''),
      faq: z.array(z.object({ q: z.string(), r: z.string() })).default([]),
    }),
});

export const collections = { blog, blogEn };
