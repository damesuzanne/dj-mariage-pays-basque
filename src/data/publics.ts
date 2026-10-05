/** Les trois publics de « Conseils & ressources » et l'appel à l'action de fin d'article. */
export const publics = {
  mariage: {
    label: 'Mariage',
    fin: {
      surtitre: 'Votre DJ mariage',
      titre: 'Et pour la musique, <em>on en parle&nbsp;?</em>',
      texte: 'Plus de 200 mariages animés au Pays Basque et dans les Landes. Dites-moi votre date et votre lieu, je vous réponds sous 24h.',
      bouton: 'Vérifier ma date',
      lien: '/#devis',
    },
  },
  entreprises: {
    label: 'Entreprise',
    fin: {
      surtitre: 'Votre DJ pour l’entreprise',
      titre: 'Un événement d’entreprise <em>à préparer&nbsp;?</em>',
      texte: 'Soirée d’équipe, séminaire, inauguration : parlons de votre projet, je vous réponds sous 24h.',
      bouton: 'Découvrir la prestation',
      lien: '/entreprises/',
    },
  },
  'bars-restaurants': {
    label: 'Bar & restaurant',
    fin: {
      surtitre: 'Votre DJ en établissement',
      titre: 'Une soirée à animer <em>dans votre établissement&nbsp;?</em>',
      texte: 'Bars, restaurants, beach clubs : parlons de vos soirées, je vous réponds sous 24h.',
      bouton: 'Découvrir la prestation',
      lien: '/bars-restaurants/',
    },
  },
} as const;

export type PublicSlug = keyof typeof publics;
