import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import { rehypeTypoFr, frHtml } from './src/utils/typo.ts';
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ROUTES, SITE } from './src/i18n/routes.ts';

// Après la construction : espaces insécables avant : ; ! ? sur toutes les pages françaises,
// pour qu'un signe ne se retrouve jamais seul en début de ligne. Le dossier /en/ (version
// anglaise) est exclu : l'anglais ne met pas d'espace avant ces signes.
const typographieFrancaise = {
  name: 'typographie-francaise',
  hooks: {
    'astro:build:done': ({ dir }) => {
      const racine = fileURLToPath(dir);
      const parcourir = (d) => {
        for (const nom of readdirSync(d)) {
          const chemin = join(d, nom);
          if (chemin === join(racine, 'en')) continue;
          if (statSync(chemin).isDirectory()) parcourir(chemin);
          else if (nom.endsWith('.html')) writeFileSync(chemin, frHtml(readFileSync(chemin, 'utf8')));
        }
      };
      parcourir(racine);
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
      filter: (page) => !page.includes('/link-tree') && !page.includes('/404'),
      // Version anglaise : chaque URL traduite porte ses liens hreflang (fr, en, x-default).
      serialize(item) {
        const chemin = new URL(item.url).pathname;
        const paire = ROUTES.find(([fr, en]) => fr === chemin || en === chemin);
        if (paire) {
          item.links = [
            { lang: 'fr', url: SITE + paire[0] },
            { lang: 'en', url: SITE + paire[1] },
            { lang: 'x-default', url: SITE + paire[0] },
          ];
        }
        return item;
      },
    }),
  ],
});
