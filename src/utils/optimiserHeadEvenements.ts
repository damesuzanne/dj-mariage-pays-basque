// Optimisation du <head> des pages « événements » (entreprises, bars-restaurants).
// Ces gabarits chargeaient 9 feuilles CSS séparées : 9 requêtes bloquant l'affichage,
// en cascade, sur mobile 4G (PageSpeed 06/10/26 : LCP 8 s, rendu bloqué 600 à 900 ms).
// Les feuilles sont donc injectées en ligne, dans le même ordre (la cascade est
// inchangée), avec font-display:swap sur les polices et un préchargement des deux
// polices du hero.
import { readFileSync } from "node:fs";
import { join } from "node:path";

const DOSSIER = join(process.cwd(), "public", "evenements-assets");
const LIEN_CSS = /<link rel="stylesheet" href="\/evenements-assets\/([a-z0-9-]+\.css)">/g;

const POLICES_PRECHARGEES = [
  "playfair-display-latin-700-normal.woff2",
  "outfit-latin-400-normal.woff2",
];

function css(nom: string): string {
  return readFileSync(join(DOSSIER, nom), "utf8")
    // les url() relatives pointaient vers le dossier de la feuille : en ligne, il faut des chemins absolus
    .replace(/url\((?!["']?(?:\/|data:|https?:))["']?([^)"']+)["']?\)/g, "url(/evenements-assets/$1)")
    .replace(/@font-face\s*\{/g, "@font-face{font-display:swap;")
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function optimiserHeadEvenements(head: string): string {
  const preload = POLICES_PRECHARGEES
    .map((f) => `<link rel="preload" href="/evenements-assets/${f}" as="font" type="font/woff2" crossorigin>`)
    .join("");
  return head.replace(LIEN_CSS, (_, nom: string) => `<style>${css(nom)}</style>`) + preload;
}
