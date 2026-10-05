import couvertureChecklist from '../assets/ressources/checklist-retroplanning-couverture.png';
import pageChecklist from '../assets/ressources/checklist-retroplanning-page.png';
import mobileChecklist from '../assets/ressources/checklist-retroplanning-mobile.png';
import couvertureJeux from '../assets/ressources/livret-jeux-couverture.png';
import pageJeux from '../assets/ressources/livret-jeux-page.png';
import mobileJeux from '../assets/ressources/livret-jeux-mobile.png';

/**
 * Ressources gratuites proposées en échange d'un prénom + e-mail.
 * Le `slug` doit exister à l'identique dans RESSOURCES de
 * ressources/apps-script/Code.gs (c'est lui qui connaît les fichiers du Drive).
 */
export const ressources = {
  'checklist-retroplanning': {
    type: 'Guide gratuit',
    titre: 'Checklist complète & rétroplanning du mariage',
    accroche: 'Le guide à remplir, de la date choisie au lendemain de la fête',
    points: [
      'Version A4 à imprimer et version téléphone à remplir',
      'Le calendrier détaillé, étape par étape, de 18 mois au jour J',
      'Budget, prestataires, plan de table, déroulé de la journée, musique',
    ],
    couverture: couvertureChecklist,
    apercu: pageChecklist,
    // Page de la version téléphone (cases cochées) pour le visuel smartphone.
    mobile: mobileChecklist,
  },
  'livret-jeux': {
    type: 'Livret gratuit',
    titre: 'Le livret de jeux de mariage',
    accroche: '12 jeux menés par vos invités et vos témoins, du cocktail à la fin de soirée',
    points: [
      'Version A4 à imprimer et version téléphone à remplir',
      'Quiz des mariés, grand mime, chasse aux signatures, jeux pour les enfants',
      'Règles en trois lignes, listes prêtes à l’emploi et tableau des scores',
    ],
    couverture: couvertureJeux,
    apercu: pageJeux,
    mobile: mobileJeux,
  },
} as const;

export type RessourceSlug = keyof typeof ressources;
