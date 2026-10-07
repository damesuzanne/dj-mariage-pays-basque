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

/** Version anglaise (/en/tips/) : mêmes publics, appel à l'action vers les pages anglaises. */
export const publicsEn: Record<PublicSlug, { label: string; fin: { surtitre: string; titre: string; texte: string; bouton: string; lien: string } }> = {
  mariage: {
    label: 'Wedding',
    fin: {
      surtitre: 'Your wedding DJ',
      titre: 'And the music, <em>shall we talk?</em>',
      texte: 'More than 200 weddings in the French Basque Country and the Landes, and destination weddings welcome. Tell me your date and venue, I reply within 24 hours.',
      bouton: 'Check my date',
      lien: '/en/#devis',
    },
  },
  entreprises: {
    label: 'Corporate',
    fin: {
      surtitre: 'Your corporate event DJ',
      titre: 'Planning a <em>corporate event?</em>',
      texte: 'Team party, seminar, product launch: tell me about your plans, I reply within 24 hours.',
      bouton: 'See the service',
      lien: '/en/corporate-events/',
    },
  },
  'bars-restaurants': {
    label: 'Bar & restaurant',
    fin: {
      surtitre: 'Your DJ for venues',
      titre: 'A night to host <em>at your venue?</em>',
      texte: 'Bars, restaurants, beach clubs: let’s talk about your nights, I reply within 24 hours.',
      bouton: 'See the service',
      lien: '/en/bars-restaurants/',
    },
  },
};
