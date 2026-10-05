/**
 * Ressources gratuites Richard DJ Event : enregistrement des leads + envoi du guide.
 *
 * Projet Apps Script lié au Google Sheet « Inbound leads - Ressources gratuites
 * Richard DJ » du Drive de Richard (richarddjevent@gmail.com). Déployé en
 * application Web (exécution en tant que Richard, accès : tout le monde).
 *
 * Circuit : formulaire du blog -> worker.js (Cloudflare, Turnstile + pot de
 * miel) -> POST JSON ici -> ligne dans l'onglet « Leads » -> e-mail envoyé
 * depuis le Gmail de Richard avec les boutons de téléchargement (fichiers du
 * Drive partagés « toute personne disposant du lien »).
 *
 * ⚠️ Ne jamais écrire le vrai jeton dans ce fichier (suivi par git) : il vit
 * dans Secret.gs (ignoré par git, poussé par clasp) et dans le secret
 * LEADS_WEBHOOK_SECRET des deux Workers (copie locale : ../.leads-secret.env).
 */

const NOM_ONGLET = 'Leads';
const EXPEDITEUR = 'Richard DJ Event';
const REPONDRE_A = 'richarddjevent@gmail.com';
// Copie de chaque nouveau lead dans la boîte de Richard (mettre false pour couper).
const NOTIFIER_RICHARD = true;

const COLONNES = [
  'Date',
  'Prénom',
  'E-mail',
  'Ressource',
  'Site',
  "Page d'origine",
  'Consentement',
  'E-mail envoyé',
  'Statut',
  'Notes',
];

// Une entrée par ressource téléchargeable. Les identifiants sont ceux des
// fichiers du Drive de Richard (la partie entre /d/ et /view de leur lien).
const RESSOURCES = {
  'checklist-retroplanning': {
    titre: 'Checklist complète & rétroplanning du mariage',
    accroche: 'Votre guide est prêt : la checklist complète et le rétroplanning, de la date choisie jusqu’au lendemain de la fête.',
    fichiers: [
      { libelle: 'Version téléphone', detail: 'à remplir sur l’écran', id: '1bF02mEdGind82uVcvl-0_NcGZgz6Zs3T' },
      { libelle: 'Version A4 à imprimer', detail: 'ou à remplir sur ordinateur', id: '1Uy8_UoHeBf75mBlUfic7MMC2U4LdF2kF' },
    ],
  },
  'livret-jeux': {
    titre: 'Le livret de jeux de mariage',
    accroche: 'Votre livret est prêt : 12 jeux menés par vos invités et vos témoins, à imprimer ou à remplir sur téléphone.',
    fichiers: [
      { libelle: 'Version téléphone', detail: 'à remplir sur l’écran', id: '1S8_8FPODX6zmxW945hlipmjO-N8r9v9t' },
      { libelle: 'Version A4 à imprimer', detail: 'ou à remplir sur ordinateur', id: '1W0qTzt-ROu0C9khEqvfJSXpL3b6TvzRW' },
    ],
  },
};

// Ouvrir l'URL /exec une fois avec le compte de Richard déclenche l'écran
// d'autorisation Google (plus fiable que l'éditeur avec plusieurs comptes
// connectés) ; on en profite pour partager les PDF et créer l'onglet.
function doGet() {
  partagerLesRessources();
  return HtmlService.createHtmlOutput('<p style="font:16px sans-serif;padding:40px">C’est autorisé : les leads arriveront dans l’onglet « Leads » et le guide partira par e-mail. Vous pouvez fermer cet onglet.</p>');
}

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    if (!WEBHOOK_SECRET || data.secret !== WEBHOOK_SECRET) return json({ success: false, message: 'Jeton invalide.' });

    const ressource = RESSOURCES[data.ressource];
    if (!ressource) return json({ success: false, message: 'Ressource inconnue.' });
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(data.email || ''))) {
      return json({ success: false, message: 'Adresse e-mail invalide.' });
    }

    const feuille = onglet();
    const ligne = feuille.getLastRow() + 1;
    feuille.getRange(ligne, 1, 1, COLONNES.length).setValues([[
      new Date(),
      nettoyer(data.prenom),
      nettoyer(data.email),
      ressource.titre,
      nettoyer(data.site),
      nettoyer(data.page),
      data.consentement ? 'Oui' : 'Non',
      'En cours',
      'NOUVEAU',
      '',
    ]]);

    // Le Sheet est la source de vérité : un échec d'envoi est noté sur la
    // ligne mais ne fait pas perdre le lead.
    let envoye = false;
    try {
      envoyerGuide(data, ressource);
      envoye = true;
    } catch (erreur) {
      feuille.getRange(ligne, COLONNES.indexOf('Notes') + 1).setValue('Envoi échoué : ' + erreur);
    }
    feuille.getRange(ligne, COLONNES.indexOf('E-mail envoyé') + 1).setValue(envoye ? 'Oui' : 'Non');

    if (NOTIFIER_RICHARD) {
      try {
        MailApp.sendEmail(REPONDRE_A, `Nouveau téléchargement : ${ressource.titre}`,
          `${data.prenom || ''} <${data.email}> a téléchargé « ${ressource.titre} »\n` +
          `Site : ${data.site || ''}\nPage : ${data.page || ''}\n\nLe lead est dans le Sheet « Inbound leads ».`);
      } catch (erreur) { /* notification facultative */ }
    }

    return json({ success: envoye });
  } catch (erreur) {
    return json({ success: false, message: String(erreur) });
  }
}

function envoyerGuide(data, ressource) {
  const prenom = nettoyer(data.prenom) || '';
  const liens = ressource.fichiers.map((f) => ({
    libelle: f.libelle,
    detail: f.detail || '',
    url: 'https://drive.google.com/uc?export=download&id=' + f.id,
  }));
  const site = data.site === 'djmariagelandes.fr' ? 'djmariagelandes.fr' : 'djmariagepaysbasque.fr';

  const texte = [
    `Bonjour ${prenom},`,
    '',
    ressource.accroche,
    '',
    ...liens.map((l) => `${l.libelle} (${l.detail}) : ${l.url}`),
    '',
    'Le PDF se remplit directement à l’écran : cochez les cases et écrivez dans les lignes, puis enregistrez.',
    '',
    'Belle préparation à vous deux,',
    'Richard',
    'Richard DJ Event · DJ mariage Pays Basque & Landes',
    `https://${site}`,
  ].join('\n');

  // Deux boutons de même poids : l'un pour le téléphone, l'autre pour l'A4.
  const boutons = liens.map((l) =>
    `<a href="${l.url}" style="display:block;background:#c6a15b;color:#101522;text-decoration:none;font-weight:600;font-size:16px;padding:14px 20px;border-radius:999px;margin:0 auto 12px;max-width:320px;text-align:center">` +
    `Télécharger · ${l.libelle}<br><span style="font-weight:400;font-size:13px">${l.detail}</span></a>`).join('');

  const html = `<!doctype html><html lang="fr"><body style="margin:0;background:#faf7f1;font-family:Helvetica,Arial,sans-serif;color:#23283a">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#faf7f1"><tr><td align="center" style="padding:32px 16px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#ffffff;border:1px solid #eadfc8;border-radius:16px">
<tr><td align="center" style="padding:32px 28px 8px">
<div style="width:56px;height:56px;line-height:56px;border:1px solid #c6a15b;border-radius:50%;font-family:Georgia,serif;font-size:28px;color:#c6a15b;text-align:center">R</div>
<div style="margin-top:10px;font-weight:600;font-size:18px;color:#101522">Richard <span style="font-weight:400;color:#c6a15b">DJ Event</span></div>
<div style="font-size:10px;letter-spacing:2px;color:#5a6072;text-transform:uppercase">DJ mariage Pays Basque &amp; Landes</div>
</td></tr>
<tr><td style="padding:20px 28px 8px;font-size:16px;line-height:1.6">
<p style="margin:0 0 14px">Bonjour ${echapper(prenom)},</p>
<p style="margin:0 0 20px">${echapper(ressource.accroche)}</p>
<div style="margin:0 0 20px">${boutons}</div>
<p style="margin:0 0 14px;font-size:14px;color:#5a6072">Le PDF se remplit directement à l’écran : cochez les cases et écrivez dans les lignes, puis enregistrez. Il s’imprime aussi très bien.</p>
<p style="margin:24px 0 0">Belle préparation à vous deux,<br><strong>Richard</strong></p>
</td></tr>
<tr><td style="padding:20px 28px 28px;font-size:12px;color:#5a6072;border-top:1px solid #f1e8d4">
Vous recevez cet e-mail car vous avez demandé cette ressource sur <a href="https://${site}" style="color:#c6a15b">${site}</a>.
Pour ne plus rien recevoir, répondez simplement « stop ».
</td></tr></table></td></tr></table></body></html>`;

  MailApp.sendEmail(String(data.email).trim(), `Votre guide : ${ressource.titre}`, texte, {
    htmlBody: html,
    name: EXPEDITEUR,
    replyTo: REPONDRE_A,
  });
}

// À lancer une fois depuis l'éditeur (et à chaque nouvelle ressource) : rend
// les PDF téléchargeables par lien, sans les rendre visibles dans les recherches.
function partagerLesRessources() {
  Object.values(RESSOURCES).forEach((r) => r.fichiers.forEach((f) => {
    DriveApp.getFileById(f.id).setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  }));
  onglet();
}

function onglet() {
  const classeur = SpreadsheetApp.getActiveSpreadsheet();
  let feuille = classeur.getSheetByName(NOM_ONGLET);
  if (!feuille) feuille = classeur.insertSheet(NOM_ONGLET, 0);
  const entete = feuille.getRange(1, 1, 1, COLONNES.length).getValues()[0];
  if (!COLONNES.every((c, i) => entete[i] === c)) {
    feuille.getRange(1, 1, 1, COLONNES.length).setValues([COLONNES]).setFontWeight('bold');
    feuille.setFrozenRows(1);
  }
  return feuille;
}

function nettoyer(v) {
  // Neutralise les formules (=, +, -, @) qu'un visiteur pourrait glisser dans le Sheet.
  const s = String(v == null ? '' : v).trim().slice(0, 200);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function echapper(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
}

function json(objet) {
  return ContentService.createTextOutput(JSON.stringify(objet)).setMimeType(ContentService.MimeType.JSON);
}
