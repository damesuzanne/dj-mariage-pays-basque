import couvertureChecklist from '../assets/ressources/checklist-retroplanning-couverture.png';
import pageChecklist from '../assets/ressources/checklist-retroplanning-page.png';
import mobileChecklist from '../assets/ressources/checklist-retroplanning-mobile.png';

/**
 * Ressources gratuites proposées en échange d'un prénom + e-mail.
 * Le `slug` doit exister à l'identique dans RESSOURCES de
 * ressources/apps-script/Code.gs (c'est lui qui connaît les fichiers du Drive).
 */
export const ressources = {
  'checklist-retroplanning': {
    titre: 'Checklist complète & rétroplanning du mariage',
    accroche: 'Le guide à remplir, de la date choisie au lendemain de la fête',
    points: [
      'Version A4 à imprimer et version téléphone à remplir',
      'Le calendrier détaillé, étape par étape, de 18 mois au jour J',
      'Budget, prestataires, déroulé de la journée, musique',
    ],
    couverture: couvertureChecklist,
    apercu: pageChecklist,
    // Page de la version téléphone (cases cochées) pour le visuel smartphone.
    mobile: mobileChecklist,
  },
} as const;

export type RessourceSlug = keyof typeof ressources;
