/**
 * Typographie française : espace insécable avant « : ; ! ? » et à l'intérieur
 * des guillemets, pour qu'un signe ne se retrouve jamais seul en début de ligne.
 */
export function fr(texte: string): string {
  return texte
    .replace(/ ([:;!?»])/g, ' $1')
    .replace(/« /g, '« ');
}

/** Même règle sur tout le texte des articles (plugin rehype pour Markdown/MDX). */
export function rehypeTypoFr() {
  const visiter = (noeud: any) => {
    if (noeud.type === 'text' && typeof noeud.value === 'string') noeud.value = fr(noeud.value);
    if (noeud.type === 'element' && ['code', 'pre', 'script', 'style'].includes(noeud.tagName)) return;
    noeud.children?.forEach(visiter);
  };
  return (arbre: any) => visiter(arbre);
}

/** Applique fr() aux seuls textes visibles d'un document HTML (jamais scripts, styles ni attributs). */
export function frHtml(html: string): string {
  return html
    .split(/(<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<[^>]*>)/)
    .map((morceau) => (morceau.startsWith('<') ? morceau : fr(morceau)))
    .join('');
}
