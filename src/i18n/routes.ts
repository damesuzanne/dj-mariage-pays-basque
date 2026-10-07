/**
 * Version anglaise du site (07/10/26) : correspondance des pages FR ↔ EN.
 *
 * Cette table unique alimente les balises hreflang, le sélecteur de langue,
 * le fil d'Ariane et le sitemap. Toute nouvelle page traduite (article du blog
 * compris) s'ajoute ici, sinon elle n'aura ni hreflang ni lien vers sa traduction.
 * Pas de redirection automatique selon la langue du navigateur : l'internaute choisit.
 */
export type Lang = 'fr' | 'en';

export const SITE = 'https://djmariagepaysbasque.fr';

/** [page française, page anglaise] : chemins avec la barre finale, comme les URL canoniques. */
export const ROUTES: [string, string][] = [
  ['/', '/en/'],
  ['/entreprises/', '/en/corporate-events/'],
  ['/bars-restaurants/', '/en/bars-restaurants/'],
  ['/contact/', '/en/contact/'],
  ['/conseils/', '/en/tips/'],
  ['/conseils/retroplanning-mariage/', '/en/tips/wedding-planning-timeline/'],
  ['/conseils/jeux-de-mariage/', '/en/tips/wedding-games/'],
  ['/conseils/lieux-mariage-pays-basque/', '/en/tips/wedding-venues-basque-country/'],
  ['/conseils/ouverture-de-bal-mariage/', '/en/tips/first-dance/'],
  ['/mentions-legales/', '/en/legal-notice/'],
  ['/politique-de-confidentialite/', '/en/privacy-policy/'],
  ['/link-tree/', '/en/link-tree/'],
];

const avecBarre = (chemin: string) => (chemin.endsWith('/') ? chemin : `${chemin}/`);

export function langFromPath(chemin: string): Lang {
  return chemin === '/en' || chemin.startsWith('/en/') ? 'en' : 'fr';
}

/** Les deux versions d'une page, ou null si la page n'a pas de traduction. */
export function alternates(chemin: string): { fr: string; en: string } | null {
  const c = avecBarre(chemin);
  const paire = ROUTES.find(([fr, en]) => fr === c || en === c);
  return paire ? { fr: paire[0], en: paire[1] } : null;
}

/** Balises hreflang à placer dans le <head> (fr, en et x-default = version française). */
export function hreflangLinks(chemin: string): { hreflang: string; href: string }[] {
  const alt = alternates(chemin);
  if (!alt) return [];
  return [
    { hreflang: 'fr', href: SITE + alt.fr },
    { hreflang: 'en', href: SITE + alt.en },
    { hreflang: 'x-default', href: SITE + alt.fr },
  ];
}

/** Même chose en HTML brut, pour les gabarits entreprises et bars-restaurants. */
export function hreflangHtml(chemin: string): string {
  return hreflangLinks(chemin)
    .map(({ hreflang, href }) => `<link rel="alternate" hreflang="${hreflang}" href="${href}">`)
    .join('');
}

/** Lien du sélecteur de langue : la page équivalente, sinon l'accueil de l'autre langue (404, link-tree…). */
export function switchHref(chemin: string, vers: Lang): string {
  const alt = alternates(chemin);
  if (alt) return alt[vers];
  return vers === 'en' ? '/en/' : '/';
}

/** Chemin d'une page française dans la langue demandée (liens internes des composants). */
export function localize(cheminFr: string, lang: Lang): string {
  if (lang === 'fr') return cheminFr;
  const [chemin, ancre] = cheminFr.split('#');
  const alt = alternates(chemin || '/');
  const base = alt ? alt.en : '/en/';
  return ancre ? `${base}#${ancre}` : base;
}
