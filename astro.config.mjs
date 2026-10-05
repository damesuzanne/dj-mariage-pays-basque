import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import { rehypeTypoFr, frHtml } from './src/utils/typo.ts';
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// Après la construction : espaces insécables avant : ; ! ? sur TOUTES les pages,
// pour qu'un signe ne se retrouve jamais seul en début de ligne.
const typographieFrancaise = {
  name: 'typographie-francaise',
  hooks: {
    'astro:build:done': ({ dir }) => {
      const parcourir = (d) => {
        for (const nom of readdirSync(d)) {
          const chemin = join(d, nom);
          if (statSync(chemin).isDirectory()) parcourir(chemin);
          else if (nom.endsWith('.html')) writeFileSync(chemin, frHtml(readFileSync(chemin, 'utf8')));
        }
      };
      parcourir(fileURLToPath(dir));
    },
  },
};

export default defineConfig({
  markdown: {
    // Espaces insécables avant : ; ! ? dans les articles (jamais de « : » en début de ligne).
    rehypePlugins: [rehypeTypoFr],
  },
  site: 'https://djmariagepaysbasque.fr',
  build: {
    // Corrige l'audit PageSpeed du 6 août 2026 : 2 feuilles CSS séparées
    // (index + mentions-legales, ~8,4 Kio) bloquaient le rendu initial
    // (760 ms de retard LCP mesuré). Site mono-page léger : inliner tout
    // le CSS ne coûte rien et supprime la requête bloquante.
    inlineStylesheets: 'always',
  },
  integrations: [
    mdx(),
    typographieFrancaise,
    sitemap({
      // La page /link-tree/ est un hub de liens en noindex : on la garde
      // hors du sitemap pour rester cohérent avec la balise robots.
      filter: (page) => !page.includes('/link-tree'),
    }),
  ],
});
