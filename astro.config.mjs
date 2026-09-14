import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://djmariagepaysbasque.fr',
  build: {
    // Corrige l'audit PageSpeed du 6 août 2026 : 2 feuilles CSS séparées
    // (index + mentions-legales, ~8,4 Kio) bloquaient le rendu initial
    // (760 ms de retard LCP mesuré). Site mono-page léger : inliner tout
    // le CSS ne coûte rien et supprime la requête bloquante.
    inlineStylesheets: 'always',
  },
  integrations: [
    sitemap({
      // La page /link-tree/ est un hub de liens en noindex : on la garde
      // hors du sitemap pour rester cohérent avec la balise robots.
      filter: (page) => !page.includes('/link-tree'),
    }),
  ],
});
