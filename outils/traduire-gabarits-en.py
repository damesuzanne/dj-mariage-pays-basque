#!/usr/bin/env python3
"""
Version anglaise des pages « événements » (07/10/26).

Génère src/templates/events/en/corporate-events.html et bars-restaurants.html à partir
des gabarits français : chaque texte visible, attribut (alt, aria-label, placeholder…)
et chaîne du JSON-LD est remplacé par sa traduction (dictionnaire ci-dessous).
Le script s'arrête si un texte français n'a pas de traduction : après une modification
d'un gabarit français, compléter le dictionnaire puis relancer
    python3 outils/traduire-gabarits-en.py
"""
import json, re, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SITE = 'https://djmariagepaysbasque.fr'
MOIS = {'janvier': 'January', 'février': 'February', 'mars': 'March', 'avril': 'April', 'mai': 'May', 'juin': 'June',
        'juillet': 'July', 'août': 'August', 'septembre': 'September', 'octobre': 'October', 'novembre': 'November', 'décembre': 'December'}

COMMUN = {
    'DJ mariage Pays Basque': 'Wedding DJ Biarritz',
    'R': 'R', '×': '×', '★★★★★': '★★★★★', '.': '.',
    'Prestations & options': 'Services & options',
    'Composez une prestation adaptée à votre lieu et à votre événement.': 'Put together a service that suits your venue and your event.',
    'Cliquez sur une carte pour découvrir les possibilités.': 'Click a card to explore the options.',
    'DJ & ambiance musicale': 'DJ & music',
    'Une sélection musicale préparée avec vous, adaptée au public et au déroulement de la soirée.': 'A music selection prepared with you, tailored to your guests and the flow of the evening.',
    'Voir le détail →': 'See details →',
    'Sonorisation & micros': 'Sound & microphones',
    'Un son adapté au lieu et des micros pour vos interventions et prises de parole.': 'Sound suited to the venue, plus microphones for speeches and announcements.',
    'Éclairage d’ambiance': 'Ambient lighting',
    'Une mise en lumière qui accompagne l’identité de votre lieu et l’énergie de votre soirée.': 'Lighting that matches the character of your venue and the energy of your evening.',
    'Photobooth': 'Photo booth',
    'Vidéoprojection & écran': 'Video projection & screen',
    'Privatisations & soirées spéciales': 'Private hire & special evenings',
    'Un accompagnement musical pour une réception, une inauguration ou une date à célébrer.': 'Music for a reception, a launch or a date worth celebrating.',
    'Fermer': 'Close',
    'À prévoir ensemble': 'What we plan together',
    'Échange sur vos ambiances et vos préférences': 'A chat about the atmosphere and music you like',
    'Préparation des temps forts': 'Planning the key moments',
    'Adaptation musicale en direct': 'Reading the room and adapting live',
    'Configuration et prestations précisées dans votre devis.': 'Set-up and services detailed in your quote.',
    'Demander un devis pour cette prestation': 'Request a quote for this service',
    'Repérage des besoins techniques': 'Checking the technical requirements',
    'Sonorisation selon la configuration retenue': 'Sound system to suit the agreed set-up',
    'Micros pour les discours et annonces': 'Microphones for speeches and announcements',
    'Échange sur l’ambiance visuelle souhaitée': 'Talking through the look you want',
    'Éclairage décoratif selon le lieu': 'Decorative lighting to suit the venue',
    'Lumières pour la partie dansante': 'Lights for the dancing',
    'Borne photo avec impressions': 'Photo booth with prints',
    'Personnalisation du visuel à définir ensemble': 'Custom print design, decided together',
    'Galerie des photos après l’événement': 'Photo gallery after the event',
    'Écran et vidéoprojecteur selon les besoins': 'Screen and projector as needed',
    'Préparation de la diffusion de vos contenus': 'Preparing your content for playback',
    'Coordination avec les temps forts': 'Timed with the key moments',
    'Préparation du déroulement musical': 'Planning the musical running order',
    'Ambiance d’accueil et soirée dansante selon votre format': 'Welcome music and a dance party, depending on your format',
    'Coordination des horaires avec votre équipe': 'Timings coordinated with your team',
    'Plus de 10 ans d’expérience comme DJ': 'Over 10 years of experience as a DJ',
    'Témoignages': 'Kind words',
    'Ils ont fait appel': 'They booked',
    'à Richard': 'Richard',
    '5 étoiles sur 5': '5 out of 5 stars',
    'Responsable événementiel': 'Events manager',
    'Zone d’intervention': 'Where I work',
    'Le Pays Basque,': 'Based in the Basque Country,',
    'et aussi les Landes': 'available worldwide',
    'Exemples de communes': 'Examples of towns',
    'Avant votre soirée': 'Before your event',
    'Vos questions,': 'Your questions,',
    'nos premiers échanges': 'answered',
    'Peut-on choisir les styles musicaux ?': 'Can we choose the music styles?',
    'Oui. Nous échangeons sur les styles souhaités, les titres incontournables et ceux à éviter. La sélection évolue ensuite selon le public et le déroulement de la soirée.':
        'Yes. We talk about the styles you want, the must-plays and the tracks to avoid. The selection then evolves with the crowd and the flow of the evening.',
    'Le matériel est-il compris dans la proposition ?': 'Is the equipment included in the proposal?',
    'Le devis précise le matériel et les options retenus. Nous commençons par vérifier ce dont votre lieu dispose déjà et ce qu’il faut prévoir en complément.':
        'The quote lists the equipment and options agreed. We start by checking what your venue already has and what needs to be added.',
    'Combien coûte une prestation ?': 'How much does it cost?',
    'Le tarif dépend de la date, des horaires, du lieu et de la configuration technique. Transmettez-moi ces informations pour recevoir un devis personnalisé et gratuit.':
        'The price depends on the date, timings, venue and technical set-up. Send me these details to receive a free, tailored quote.',
    'Combien de temps à l’avance faut-il vous contacter ?': 'How far in advance should I get in touch?',
    'Dès que votre date est envisagée, nous pouvons vérifier mes disponibilités. Les besoins techniques et les horaires sont ensuite précisés ensemble.':
        'As soon as you have a date in mind, we can check my availability. Technical needs and timings are then finalised together.',
    'Comment préparez-vous l’installation ?': 'How do you prepare the set-up?',
    'Nous convenons avec votre interlocuteur sur place des accès, de l’espace nécessaire et des horaires d’installation. Les besoins électriques et les contraintes sonores sont vérifiés en amont.':
        'We agree access, the space needed and set-up times with your contact on site. Power requirements and sound restrictions are checked in advance.',
    'Dans quelles villes intervenez-vous ?': 'Where do you work?',
    'Devis gratuit': 'Free quote',
    'Votre date, votre lieu, votre ambiance : présentez-moi votre projet pour recevoir un devis personnalisé et gratuit.':
        'Your date, your venue, the atmosphere you want: tell me about your plans and receive a free, tailored quote. English-speaking support available.',
    'Réponse sous 24h': 'Reply within 24 hours',
    'Sans engagement': 'No commitment',
    'Données confidentielles': 'Your details stay private',
    '06 84 33 18 24': '+33 6 84 33 18 24',
    '7j/7 sur rendez-vous': '7 days a week, by appointment',
    'richarddjevent@gmail.com': 'richarddjevent@gmail.com',
    'Pays basque & Landes': 'French Basque Country · Worldwide',
    'Prénom *': 'First name *', 'Nom *': 'Last name *', 'Email *': 'Email *', 'Téléphone *': 'Phone *',
    'Entreprise / organisation': 'Company / organisation', 'Bar / restaurant': 'Bar / restaurant',
    'Date envisagée': 'Preferred date', 'Lieu / ville *': 'Venue / town *',
    'Nombre de participants': 'Number of guests', 'Horaires souhaités': 'Preferred times', 'Votre projet': 'Your plans',
    'Établissement et ville': 'Venue and town', 'Ex. : de 19 h à minuit': 'E.g. 7 pm to midnight',
    'Format, ambiance musicale, matériel sur place, options souhaitées…': 'Format, music style, equipment on site, options you would like…',
    'Envoyer ma demande': 'Send my request', 'Envoyer via WhatsApp': 'Send via WhatsApp',
    'Les informations transmises servent uniquement à traiter votre demande de devis.': 'Your details are only used to answer your quote request.',
    'Politique de confidentialité': 'Privacy policy',
    'WhatsApp direct': 'WhatsApp',
    '10 ans': '10 years', 'd’expérience': 'of experience',
    'Discuter sur WhatsApp': 'Chat on WhatsApp',
    'Ouvrir le menu': 'Open menu',
    'Navigation principale': 'Main navigation',
    'Richard': 'Richard', 'DJ Event': 'DJ Event',
}
# Menu anglais injecté par le script (déjà en anglais).
for deja in ['Main navigation', 'Weddings', 'Corporate Events', 'Bars & Restaurants', 'Wedding Tips', 'Get a quote']:
    COMMUN[deja] = deja
for ville in ['Bayonne', 'Biarritz', 'Anglet', 'Saint-Jean-de-Luz', 'Hendaye', 'Hossegor', 'Capbreton', 'Dax']:
    COMMUN[ville] = ville

ENTREPRISES = {
    'DJ entreprise à Bayonne, Biarritz et dans les Landes': 'Corporate event DJ in Biarritz',
    'Votre événement rassemble.': 'Your guests come together.',
    'La musique fait le lien.': 'Music brings them closer.',
    'Un cocktail pour accueillir vos invités, une ambiance pour accompagner les échanges, puis une piste de danse pour célébrer ensemble. Richard DJ Event imagine avec vous le rythme musical de votre événement.':
        'A cocktail hour to welcome your guests, background music while people mingle, then a dance floor to celebrate together. Richard DJ Event plans the musical flow of your event with you, in the Basque Country or wherever your event takes place.',
    'Parlons de votre événement': 'Let’s talk about your event',
    'Réponse': 'Reply', 'sous 24h': 'within 24 hours', 'Sans': 'No', 'engagement': 'commitment',
    'Richard DJ Event aux platines lors d’une réception d’entreprise': 'Richard DJ Event behind the decks at a corporate reception',
    'Ambiance de soirée d’entreprise': 'Corporate party atmosphere',
    'Votre DJ pour les événements d’entreprise': 'Your DJ for corporate events',
    'Une soirée qui rassemble,': 'An evening that brings people together,',
    'une préparation qui vous rassure': 'planning you can rely on',
    'Soirée d’équipe, séminaire, inauguration ou réception clients : je prépare avec vous une ambiance musicale adaptée à vos invités et à votre programme. Nous définissons les temps forts et les besoins techniques en amont, pour que vous puissiez profiter de votre événement aux côtés de vos équipes.':
        'Team party, seminar, launch or client reception: I prepare music that suits your guests and your programme with you. We agree on the key moments and technical needs in advance, so you can enjoy the event alongside your team.',
    'Une sélection musicale adaptée à vos invités': 'Music chosen for your guests',
    'Sonorisation et éclairage selon les besoins du lieu': 'Sound and lighting to suit the venue',
    'Un interlocuteur unique pour préparer la prestation': 'One point of contact from planning to the night',
    'Discutons de votre événement': 'Tell me about your event',
    'DJ pour entreprises, séminaires et réceptions professionnelles': 'DJ for corporate events, seminars and business receptions',
    'Une animation photo conviviale pour partager des souvenirs entre collègues ou invités.': 'A fun photo activity for colleagues and guests to share memories.',
    'Présentations, rétrospectives et vidéos trouvent leur place dans votre programme.': 'Presentations, look-back videos and films fit right into your programme.',
    'Sonorisation et éclairage pour vos événements professionnels': 'Sound and lighting for your corporate events',
    'Soirée d’entreprise, cocktail de fin de séminaire, inauguration ou réception de partenaires : le dispositif musical est préparé selon votre programme et votre lieu. Micros pour les discours, éclairage d’ambiance, vidéoprojection et photobooth peuvent compléter la prestation DJ, selon les besoins retenus dans le devis.':
        'Company party, end-of-seminar drinks, launch or partner reception: the music set-up is planned around your programme and your venue. Microphones for speeches, ambient lighting, video projection and a photo booth can complement the DJ service, depending on what is agreed in the quote.',
    'Basé au Pays basque, Richard DJ Event accompagne les projets d’entreprises, de CSE, d’associations professionnelles et d’organismes publics au Pays basque et dans les Landes. Vous préparez une rencontre de réseau ou un événement consulaire ? Présentez votre format, vos horaires et vos contraintes techniques pour obtenir une proposition adaptée.':
        'Based in the French Basque Country, Richard DJ Event works with companies, staff committees, professional associations and public bodies across the Basque Country and the Landes, and welcomes corporate bookings elsewhere in France and abroad. Planning a networking event or a chamber of commerce reception? Share your format, timings and technical constraints to receive a tailored proposal.',
    'Soirées d’entreprise, séminaires et inaugurations : leurs retours après l’événement.': 'Company parties, seminars and launches: their feedback after the event. Reviews translated from French.',
    'Une prestation impeccable pour notre soirée annuelle. Richard a parfaitement compris l’ambiance que nous recherchions et a réussi à faire danser toutes les générations. Très professionnel du début à la fin.':
        'Flawless service for our annual party. Richard understood exactly the atmosphere we were after and got every generation dancing. Very professional from start to finish.',
    'Nous avons fait appel à Richard pour l’animation de notre soirée d’entreprise et tout s’est déroulé à merveille. Une excellente sélection musicale, beaucoup d’élégance et une vraie capacité à s’adapter aux invités.':
        'We booked Richard for our company party and everything went wonderfully. Excellent music, plenty of style and a real ability to adapt to the guests.',
    'Une très belle soirée pour célébrer les 20 ans de notre entreprise. L’ambiance est montée progressivement et la piste de danse n’a pratiquement pas désempli jusqu’à la fin. Nous recommandons sans hésiter.':
        'A wonderful evening to celebrate our company’s 20th anniversary. The atmosphere built up gradually and the dance floor stayed full almost until the very end. We recommend him without hesitation.',
    'Richard a animé notre soirée de fin d’année avec beaucoup de professionnalisme. Installation soignée, musique parfaitement adaptée et très bon contact avec nos équipes. Une prestation vraiment réussie.':
        'Richard played our end-of-year party with great professionalism. A neat set-up, music that suited the room perfectly and a great rapport with our teams. A real success.',
    'Nous souhaitions une ambiance festive mais suffisamment élégante pour recevoir nos collaborateurs et partenaires. Le résultat était exactement celui attendu. Richard a su trouver le bon équilibre tout au long de la soirée.':
        'We wanted a festive atmosphere that was still elegant enough to welcome our staff and partners. The result was exactly what we hoped for. Richard struck the right balance all evening.',
    'Une excellente prestation pour notre séminaire. Richard a su passer d’une ambiance conviviale pendant le cocktail à une vraie soirée dansante quelques heures plus tard. Nos équipes en parlent encore.':
        'An excellent night at our seminar. Richard went from a relaxed vibe during the cocktail hour to a proper dance party a few hours later. Our teams are still talking about it.',
    'Responsable communication': 'Communications manager', 'Directeur commercial': 'Sales director',
    'Assistante de direction': 'Executive assistant', 'Responsable des ressources humaines': 'HR manager',
    'Directeur d’agence': 'Branch manager',
    'Richard DJ Event accompagne les entreprises de tout le Pays Basque et se déplace aussi dans les Landes voisines : côte landaise, Dax, Mont-de-Marsan. Le déplacement éventuel est précisé dans le devis.':
        'Richard DJ Event works with companies across the French Basque Country and the neighbouring Landes, and travels for corporate events elsewhere in France and abroad.',
    'Pouvez-vous intervenir dans un lieu déjà équipé ?': 'Can you work in a venue that already has equipment?',
    'Oui. Nous faisons le point avec votre lieu ou votre équipe technique pour définir le matériel disponible et ce que je dois apporter.':
        'Yes. We check with your venue or technical team what equipment is available and what I need to bring.',
    'Peut-on prévoir une ambiance discrète puis une soirée dansante ?': 'Can the music start low-key and turn into a dance party?',
    'Oui. Nous préparons une progression musicale adaptée au cocktail, aux échanges et à la danse, selon votre programme.':
        'Yes. We plan a musical progression for the cocktail hour, the networking and the dancing, following your programme.',
    'Comment obtenir un devis pour une soirée d’entreprise ?': 'How do I get a quote for a corporate event?',
    'Indiquez-moi la date, le lieu, les horaires, le nombre approximatif de participants et les prestations souhaitées. Ces éléments permettent de préparer une proposition adaptée.':
        'Send me the date, venue, timings, approximate number of guests and the services you would like. That is all I need to prepare a tailored proposal.',
    'Je suis basé au Pays basque et me déplace au Pays basque et dans les Landes, notamment à Biarritz, Anglet, Saint-Jean-de-Luz, Hossegor, Capbreton et Dax. Le déplacement est précisé dans votre devis.':
        'I am based in the French Basque Country and work across the Basque Country and the Landes, including Biarritz, Anglet, Saint-Jean-de-Luz, Hossegor, Capbreton and Dax. Corporate events elsewhere in France or abroad are welcome too.',
    'Donnons vie à': 'Let’s bring', 'votre événement': 'your event to life',
}

BARS = {
    'DJ bar et restaurant au Pays basque et dans les Landes': 'Bar & restaurant DJ in Biarritz',
    'Votre lieu a une personnalité.': 'Your venue has a personality.',
    'Donnons-lui le bon rythme.': 'Let’s give it the right rhythm.',
    'Une ambiance qui accompagne les conversations, un dîner qui se prolonge, une soirée qui prend de l’énergie. Richard DJ Event prépare une sélection musicale adaptée à votre établissement et à votre clientèle.':
        'Music that sits under the conversation, a dinner that lingers, an evening that builds in energy. Richard DJ Event prepares a music selection tailored to your venue and your guests.',
    'Préparons votre prochaine soirée': 'Let’s plan your next night',
    'Volume': 'Volume', 'maîtrisé': 'under control', 'Sur mesure': 'Tailored', 'selon votre lieu': 'to your venue',
    'Ambiance musicale en bar-restaurant': 'Music in a bar-restaurant',
    'Illustration d’une soirée musicale dans un bar-restaurant avec un DJ et des clients': 'Illustration of a music night in a bar-restaurant with a DJ and guests',
    'Votre DJ pour les bars et restaurants': 'Your DJ for bars and restaurants',
    'L’esprit de votre lieu,': 'The spirit of your venue,',
    'le rythme de votre soirée': 'the rhythm of your night',
    'Chaque établissement a son identité, sa clientèle et ses habitudes. Je construis avec vous une sélection musicale qui s’intègre à votre lieu : une ambiance pour l’apéritif, une musique qui accompagne le dîner ou une soirée plus festive. Les horaires, le volume et l’installation sont préparés avec votre équipe.':
        'Every venue has its own identity, clientele and habits. I build a music selection with you that fits your venue: background music for aperitif hour, music to accompany dinner, or a livelier party. Timings, volume and set-up are planned with your team.',
    'Une sélection musicale pensée pour votre clientèle': 'Music chosen with your clientele in mind',
    'Un volume adapté au service et aux conversations': 'Volume that suits service and conversation',
    'Une installation préparée selon votre espace': 'A set-up planned around your space',
    'DJ pour bars, restaurants et soirées en établissement': 'DJ for bars, restaurants and venue nights',
    'Une animation photo pour vos privatisations et soirées spéciales, avec des souvenirs à emporter.': 'A photo activity for private hire and special nights, with keepsakes to take home.',
    'Un écran pour les contenus de vos soirées privées et événements au sein de l’établissement.': 'A screen for content at private parties and events in your venue.',
    'Sonorisation et ambiance musicale pour bars et restaurants': 'Sound and music for bars and restaurants',
    'DJ en bar à cocktails, musique pour un dîner au restaurant, afterwork ou soirée en terrasse : la prestation s’adapte à votre clientèle et au rythme du service. Nous vérifions la sonorisation disponible, les branchements, l’espace DJ et le niveau sonore convenu avec votre équipe. Un éclairage complémentaire peut être prévu pour la partie festive.':
        'Cocktail bar DJ, dinner music in a restaurant, after-work drinks or a terrace party: the service adapts to your clientele and the pace of service. We check the available sound system, power, DJ space and the volume agreed with your team. Extra lighting can be added for the party part of the night.',
    'Richard DJ Event intervient à Bayonne, Biarritz, Anglet et Saint-Jean-de-Luz, ainsi qu’à Hossegor, Capbreton et Dax dans les Landes. Une soirée ponctuelle, une privatisation ou plusieurs dates dans votre programmation : le devis précise les horaires, le déplacement et les moyens techniques nécessaires.':
        'Richard DJ Event plays in Bayonne, Biarritz, Anglet and Saint-Jean-de-Luz, as well as Hossegor, Capbreton and Dax in the Landes. A one-off night, private hire or several dates in your calendar: the quote sets out the timings, travel and technical requirements.',
    'Bars, restaurants et établissements de nuit : leurs retours après la soirée.': 'Bars, restaurants and nightlife venues: their feedback after the night. Reviews translated from French.',
    'Richard intervient régulièrement lors de nos soirées musicales et c’est toujours un vrai plaisir. Il sait parfaitement s’adapter à l’ambiance du lieu et au public, avec une programmation élégante et jamais agressive.':
        'Richard plays regularly at our music nights and it is always a real pleasure. He adapts perfectly to the venue and the crowd, with an elegant set that is never overpowering.',
    'Une excellente soirée d’été. Richard a su créer une ambiance festive dès le début du service puis faire monter progressivement l’énergie jusqu’à la fermeture. Nos clients ont adoré.':
        'An excellent summer night. Richard created a festive atmosphere from the start of service, then gradually built the energy until closing time. Our customers loved it.',
    'Très belle prestation pour notre soirée spéciale. Une sélection musicale parfaitement adaptée à notre clientèle et une vraie maîtrise du rythme de la soirée. Nous retravaillerons avec lui avec plaisir.':
        'A great performance for our special night. Music perfectly suited to our clientele and real control over the pace of the evening. We will happily work with him again.',
    'Nous cherchions un DJ capable de conserver l’esprit chic et convivial de notre établissement tout en apportant une vraie ambiance en deuxième partie de soirée. Richard a parfaitement répondu à nos attentes.':
        'We were looking for a DJ who could keep the chic, friendly spirit of our venue while bringing real energy later in the night. Richard met our expectations perfectly.',
    'Une soirée complète du début à la fin. Richard sait lire son public et adapter immédiatement sa programmation. Très professionnel dans son installation comme dans son attitude avec les équipes.':
        'A great night from start to finish. Richard reads his crowd and adapts his set straight away. Very professional, both in his set-up and in how he works with the staff.',
    'Nous avons confié à Richard l’animation de notre soirée de lancement de saison. Très bon choix : une ambiance dynamique, beaucoup de monde sur la piste et d’excellents retours de nos clients.':
        'We trusted Richard with our season launch party. A great choice: a lively atmosphere, a packed dance floor and excellent feedback from our customers.',
    'Gérant de restaurant': 'Restaurant manager', 'Responsable de bar': 'Bar manager', 'Directeur d’établissement': 'Venue director',
    'Manager de bar à cocktails': 'Cocktail bar manager', 'Responsable d’exploitation': 'Operations manager',
    'Richard DJ Event anime des bars et restaurants dans tout le Pays Basque, et aussi dans tout le département des Landes, de la côte à Mont-de-Marsan. Le déplacement éventuel est précisé dans le devis.':
        'Richard DJ Event plays in bars and restaurants across the French Basque Country and the whole of the Landes, from the coast to Mont-de-Marsan.',
    'Proposez-vous une date ponctuelle ou plusieurs soirées ?': 'Do you offer one-off nights or several dates?',
    'Nous pouvons échanger sur une soirée ponctuelle ou plusieurs dates, selon votre calendrier et mes disponibilités.':
        'We can discuss a one-off night or several dates, depending on your calendar and my availability.',
    'La musique peut-elle accompagner le repas sans gêner les conversations ?': 'Can the music accompany dinner without drowning out conversation?',
    'C’est un point que nous définissons en amont. L’ambiance et le volume sont adaptés à votre format, avec des ajustements pendant la prestation.':
        'That is something we agree on in advance. The atmosphere and volume are adapted to your format, with adjustments during the night.',
    'Quelles informations vous transmettre pour une proposition ?': 'What information do you need for a proposal?',
    'Le nom et la ville de votre établissement, la date, les horaires, la clientèle attendue et l’équipement déjà présent. Ajoutez quelques mots sur l’ambiance que vous souhaitez créer.':
        'The name and town of your venue, the date, the timings, the expected clientele and the equipment already in place. Add a few words about the atmosphere you want to create.',
    'Je suis basé au Pays basque et me déplace au Pays basque et dans les Landes, notamment à Biarritz, Anglet, Saint-Jean-de-Luz, Hossegor, Capbreton et Dax. Le déplacement est précisé dans votre devis.':
        'I am based in the French Basque Country and work across the Basque Country and the Landes, including Biarritz, Anglet, Saint-Jean-de-Luz, Hossegor, Capbreton and Dax.',
    'Préparons': 'Let’s plan', 'votre prochaine soirée': 'your next night',
}

PAGES = [
    {
        'source': 'entreprises.html', 'cible': 'corporate-events.html', 'fr': '/entreprises/', 'en': '/en/corporate-events/',
        'dico': ENTREPRISES,
        'title': 'Corporate Event DJ Biarritz & Basque Country | Richard DJ Event',
        'description': 'Corporate event DJ based in the French Basque Country: company parties, seminars and receptions in Biarritz, the Basque Country and beyond. Sound, lighting, free quote.',
        'service': 'Corporate event DJ in Biarritz',
        'serviceType': 'Corporate event DJ',
        'monde': True,
        'categorie': 'a corporate event',
        'wa': 'Hello Richard, I would like some information about our corporate event.',
    },
    {
        'source': 'bars-restaurants.html', 'cible': 'bars-restaurants.html', 'fr': '/bars-restaurants/', 'en': '/en/bars-restaurants/',
        'dico': BARS,
        'title': 'Bar & Restaurant DJ Biarritz & Basque Country | Richard DJ Event',
        'description': 'DJ for bars and restaurants in the French Basque Country and the Landes: aperitif hours, terraces, party nights and private hire. Music tailored to your venue.',
        'service': 'Bar and restaurant DJ in the French Basque Country',
        'serviceType': 'Bar and restaurant DJ',
        'monde': False,
        'categorie': 'a night at our venue',
        'wa': 'Hello Richard, I would like some information about a night at our bar or restaurant.',
    },
]

def normaliser(t):
    return t.replace(' ', ' ').replace(' ', ' ')

def traduire_page(conf):
    dico = {**COMMUN, **conf['dico']}
    manquants = []

    def tr(texte):
        brut = normaliser(texte)
        cle = re.sub(r'\s+', ' ', brut).strip()
        if not cle:
            return texte
        m = re.fullmatch(r'(\d{1,2}) (\w+) (\d{4})', cle)
        if m and m.group(2) in MOIS:
            return f'{m.group(1)} {MOIS[m.group(2)]} {m.group(3)}'
        if cle in dico:
            debut = brut[: len(brut) - len(brut.lstrip())]
            fin = brut[len(brut.rstrip()):]
            return debut + dico[cle] + fin
        if re.fullmatch(r'[A-ZÉ]{2}|[A-ZÉ][a-zé]+ [A-Z]\.', cle):  # initiales et prénoms « Sophie M. »
            return texte
        manquants.append(cle)
        return texte

    html = (RACINE / 'src/templates/events' / conf['source']).read_text()
    tete, corps = html[: html.index('</head>')], html[html.index('</head>'):]

    # 1. JSON-LD : textes traduits, URL et langue de la page anglaise.
    def jsonld(m):
        data = json.loads(m.group(1))
        for noeud in data['@graph']:
            for cle in ('@id', 'url'):
                if cle in noeud:
                    noeud[cle] = noeud[cle].replace(SITE + conf['fr'], SITE + conf['en'])
            for cle in ('about', 'breadcrumb'):
                if cle in noeud and '@id' in noeud[cle]:
                    noeud[cle]['@id'] = noeud[cle]['@id'].replace(SITE + conf['fr'], SITE + conf['en'])
            if noeud['@type'] == 'WebPage':
                noeud.update(name=conf['title'], description=conf['description'], inLanguage='en')
                noeud.pop('breadcrumb', None)
            elif noeud['@type'] == 'Service':
                zones = [{'@type': 'AdministrativeArea', 'name': 'French Basque Country'}, {'@type': 'AdministrativeArea', 'name': 'Landes'}]
                if conf['monde']:
                    zones += [{'@type': 'Country', 'name': 'France'}, 'Worldwide']
                noeud.update(name=conf['service'], serviceType=conf['serviceType'], description=conf['description'], areaServed=zones)
            elif noeud['@type'] == 'FAQPage':
                for q in noeud['mainEntity']:
                    q['name'] = tr(q['name'])
                    q['acceptedAnswer']['text'] = tr(q['acceptedAnswer']['text'])
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    tete = re.sub(r'<script type="application/ld\+json">(.*?)</script>', jsonld, tete, flags=re.S)

    # 2. Balises meta du <head>.
    titre = conf['title'].replace('&', '&amp;')
    tete = re.sub(r'<title>.*?</title>', f'<title>{titre}</title>', tete)
    for motif, valeur in [
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{conf["description"]}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}{conf["en"]}">'),
        (r'<meta property="og:locale" content="[^"]*">', '<meta property="og:locale" content="en_GB"><meta property="og:locale:alternate" content="fr_FR">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}{conf["en"]}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titre}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{conf["description"]}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{titre}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{conf["description"]}">'),
    ]:
        assert re.search(motif, tete), motif
        tete = re.sub(motif, valeur, tete)
    tete = tete.replace('<html lang="fr">', '<html lang="en">')

    # 3. Menu du gabarit : liens vers les pages anglaises.
    liens = [('/en/', 'Weddings'), ('/en/corporate-events/', 'Corporate Events'), ('/en/bars-restaurants/', 'Bars & Restaurants'), ('/en/tips/', 'Wedding Tips')]
    courant = ' aria-current="page"'
    nav = '<nav class="nav" id="main-nav" aria-label="Main navigation">' + ''.join(
        f'<a href="{href}"{courant if href == conf["en"] else ""}>{label}</a>' for href, label in liens
    ) + '<a href="#devis" class="btn btn-gold nav-cta">Get a quote</a></nav>'
    corps, n = re.subn(r'<nav class="nav" id="main-nav".*?</nav>', nav, corps, count=1, flags=re.S)
    assert n == 1
    corps = corps.replace('<div class="brand">\n      <a href="/">', '<div class="brand">\n      <a href="/en/">', 1)

    # 4. Scripts : formulaire, assistant et catégorie en anglais ; liens WhatsApp et confidentialité.
    corps = re.sub(r"<script>const eventCategory='[^']*';</script>", f"<script>const eventCategory='{conf['categorie']}';</script>", corps)
    corps = corps.replace('/evenements-assets/expanded.js', '/evenements-assets/expanded-en.js')
    corps = re.sub(r'/evenements-assets/assistant-[a-z-]+\.js', '/assistant-richard-en.js?v=1', corps)
    from urllib.parse import quote
    corps = re.sub(r'https://wa\.me/33684331824\?text=[^"]+', 'https://wa.me/33684331824?text=' + quote(conf['wa']), corps)
    corps = corps.replace('https://djmariagepaysbasque.fr/politique-de-confidentialite/', '/en/privacy-policy/')
    corps = corps.replace('data-language="fr"', 'data-language="en"')

    # 5. Textes visibles et attributs (hors scripts, styles et pied de page, remplacé par Footer.astro).
    debut_footer, fin_footer = corps.index('<footer'), corps.index('</footer>') + len('</footer>')
    footer = corps[debut_footer:fin_footer]
    corps = corps[:debut_footer] + '<!--FOOTER-->' + corps[fin_footer:]
    morceaux = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<[^>]*>)', corps)
    sortie = []
    for morceau in morceaux:
        if morceau.startswith('<script') or morceau.startswith('<style') or morceau.startswith('<svg'):
            sortie.append(morceau)
        elif morceau.startswith('<'):
            sortie.append(re.sub(r'\b(alt|aria-label|placeholder|data-option|title)="([^"]*)"',
                                 lambda m: f'{m.group(1)}="{tr(m.group(2))}"', morceau))
        else:
            sortie.append(tr(morceau) if morceau.strip() else morceau)
    corps = ''.join(sortie).replace('<!--FOOTER-->', footer)

    if manquants:
        print(f"\n{conf['source']} : {len(manquants)} texte(s) sans traduction :")
        for m in dict.fromkeys(manquants):
            print('  -', m)
        sys.exit(1)
    (RACINE / 'src/templates/events/en' / conf['cible']).write_text(tete + corps)
    print(f"OK {conf['cible']}")

for conf in PAGES:
    traduire_page(conf)
