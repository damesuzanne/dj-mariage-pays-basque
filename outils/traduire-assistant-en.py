#!/usr/bin/env python3
"""
Version anglaise de l'assistant Richard DJ (07/10/26) : génère public/assistant-richard-en.js.

Un seul fichier pour toutes les pages anglaises : il reprend le moteur de
public/assistant-richard.js et choisit la configuration (mariage, entreprises ou
bars-restaurants) selon l'adresse de la page. Les textes des trois configurations
françaises sont traduits par le dictionnaire ci-dessous : le script s'arrête si un texte
n'a pas de traduction. L'e-mail reçu par Richard reste en français et précise que le
client vient de la version anglaise. Relancer après toute modification de l'assistant :
    python3 outils/traduire-assistant-en.py
"""
import json, re, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

def config_de(fichier):
    s = (RACINE / fichier).read_text()
    m = re.search(r'configElement\.textContent = (".*?");\n', s)
    return json.loads(json.loads(m.group(1)))

T = {
    # Bandeau de démonstration HTAGS (jamais affiché en mode réel, traduit par cohérence).
    'Et si cet assistant travaillait pour votre activité ?': 'What if this assistant worked for your business?',
    'Une landing page conçue pour convertir, avec votre chatbot IA personnalisé et inclus sur demande.': 'A landing page built to convert, with your own AI chatbot included on request.',
    'Lancez votre projet': 'Start your project',
    'Assistant Richard DJ': 'Richard DJ Assistant',
    # Messages d'accueil
    'Bonjour 👋 Je peux vous aider à préparer votre mariage ou à transmettre une demande de disponibilité à Richard. Que souhaitez-vous faire ?':
        'Hello 👋 I can help you plan your wedding or send Richard an availability request. What would you like to do?',
    'Bonjour ! Je vous aide à préparer votre soirée d’entreprise, séminaire ou événement clients. Quel est votre projet ?':
        'Hello! I can help you plan your company party, seminar or client event. What are you planning?',
    'Bonjour ! Je vous aide à préparer une soirée musicale dans votre bar ou restaurant. Quel est votre projet ?':
        'Hello! I can help you plan a music night at your bar or restaurant. What are you planning?',
    # Mariage
    'Aperçu de votre projet de mariage': 'Your wedding at a glance',
    'Nouvelle demande mariage qualifiée': 'New qualified wedding enquiry',
    'Futurs mariés identifiés': 'Couple identified',
    'Demande de disponibilité': 'Check availability',
    'Préparer mon mariage': 'Plan my wedding',
    'Demande': 'Request', 'Date du mariage': 'Wedding date', 'Secteur': 'Area',
    'Confirmation du projet': 'Plans confirmed', 'Recherche de DJ': 'DJ search', 'Lieu de réception': 'Venue',
    'Nombre d’invités': 'Number of guests', 'Moments à sonoriser': 'Moments to cover',
    'Prestations souhaitées': 'Services requested', 'Ambiance musicale': 'Music', 'Avancement du projet': 'Planning stage',
    'Découvrir les prestations': 'See the services',
    'Être rappelé par Richard': 'Get a call back from Richard',
    'Coordonnées & zone d’intervention': 'Contact details & area covered',
    'À quelle date aura lieu votre mariage ?': 'When is your wedding?',
    'Valider cette date': 'Confirm this date',
    'Dans quel secteur se déroulera le mariage ?': 'Where will the wedding take place?',
    'Bayonne / Anglet': 'Bayonne / Anglet', 'Biarritz': 'Biarritz', 'Saint-Jean-de-Luz / Hendaye': 'Saint-Jean-de-Luz / Hendaye',
    'Pays Basque intérieur': 'Inland Basque Country', 'Landes / Hossegor / Dax': 'Landes / Hossegor / Dax',
    'Autre secteur': 'Elsewhere in France',
    'La date et le lieu de votre mariage sont-ils déjà confirmés ?': 'Are your wedding date and venue already confirmed?',
    'Oui, la date et le lieu sont confirmés': 'Yes, the date and venue are confirmed',
    'La date est confirmée, le lieu reste à choisir': 'The date is set, the venue is still to be chosen',
    'La date est encore flexible': 'The date is still flexible',
    'Commençons par la date prévue pour votre mariage.': 'Let’s start with your wedding date.',
    'Dans quel secteur se déroulera votre mariage ?': 'Where will your wedding take place?',
    'Quel est le nom du lieu de réception ? Si vous ne l’avez pas encore choisi, indiquez simplement « à définir ».':
        'What is the name of your venue? If you have not chosen it yet, just type “to be decided”.',
    'Ex. : Domaine de Bassilour': 'E.g. Domaine de Bassilour',
    'Valider le lieu': 'Confirm the venue',
    'Combien d’invités prévoyez-vous approximativement ?': 'Roughly how many guests are you expecting?',
    'Ex. : 120': 'E.g. 120', ' invités': ' guests', 'Valider': 'Confirm',
    'Quels moments souhaitez-vous confier à Richard ?': 'Which parts of the day would you like Richard to cover?',
    'Cérémonie': 'Ceremony', 'Vin d’honneur': 'Drinks reception', 'Repas': 'Dinner', 'Soirée dansante': 'Dance party',
    'Valider les moments': 'Confirm',
    'Souhaitez-vous ajouter des prestations complémentaires ?': 'Would you like to add any extra services?',
    'Oui, choisir mes options': 'Yes, choose my options', 'Non, pas pour le moment': 'Not for now',
    'Aucune option pour le moment': 'No options for now',
    'Quelles prestations complémentaires vous intéressent ?': 'Which extra services interest you?',
    'Éclairage d’ambiance et piste de danse': 'Ambient and dance floor lighting', 'Photobooth': 'Photo booth',
    'Vidéoprojection et écran': 'Video projection and screen', 'Fumée pour l’ouverture de bal': 'Low fog for the first dance',
    'Stand barbe à papa et pop-corn': 'Candy floss and popcorn stand',
    'Sonorisation mobile complémentaire': 'Additional portable sound system',
    'Valider les prestations': 'Confirm',
    'Avez-vous déjà une idée précise pour la musique de votre mariage ?': 'Do you already have a clear idea for your wedding music?',
    'Oui, préciser mon idée': 'Yes, let me describe it', 'Un mélange totalement personnalisé': 'A fully personalised mix',
    'À définir avec Richard': 'To be decided with Richard',
    'Décrivez librement votre thème, un style musical ou une idée très précise.': 'Describe your theme, a music style or a specific idea.',
    'Votre idée musicale': 'Your music idea',
    'Ex. : une soirée reggae, un thème cinéma, beaucoup de rock…': 'E.g. a reggae night, a movie theme, lots of rock…',
    'Valider mon idée': 'Confirm my idea',
    'Où en est aujourd’hui l’organisation de votre mariage ?': 'Where are you with your wedding planning?',
    'La date et le lieu sont confirmés': 'The date and venue are confirmed',
    'L’organisation est en cours': 'Planning is under way',
    'Je prends simplement des renseignements': 'I am just gathering information',
    'Où en êtes-vous dans votre recherche de DJ ?': 'Where are you in your search for a DJ?',
    'Je commence mes recherches': 'I am just starting to look', 'Je compare plusieurs DJ': 'I am comparing several DJs',
    'J’ai déjà reçu un ou plusieurs devis': 'I have already received one or more quotes',
    'Notre choix est presque arrêté': 'We have almost decided',
    'Nous devons remplacer un DJ devenu indisponible': 'We need to replace a DJ who is no longer available',
    'PRESTATIONS RICHARD DJ EVENT\n\n• Animation musicale personnalisée\n• Sonorisation de la cérémonie et du vin d’honneur\n• Éclairage d’ambiance et piste de danse\n• Photobooth\n• Vidéoprojection et écran\n• Fumée pour l’ouverture de bal\n• Stand barbe à papa et pop-corn':
        'RICHARD DJ EVENT SERVICES\n\n• Personalised DJ entertainment\n• Ceremony and drinks reception sound\n• Ambient and dance floor lighting\n• Photo booth\n• Video projection and screen\n• Low fog for the first dance\n• Candy floss and popcorn stand',
    'Revenir au menu principal': 'Back to main menu',
    'RICHARD DJ EVENT\nBayonne · Pays Basque · Landes\n\n06 84 33 18 24\nricharddjevent@gmail.com\n\nDisponible 7j/7 sur rendez-vous · Réponse sous 24 h.':
        'RICHARD DJ EVENT\nFrench Basque Country · Available worldwide\n\n+33 6 84 33 18 24\nricharddjevent@gmail.com\n\nAvailable 7 days a week by appointment · Reply within 24 hours · English-speaking support available.',
    'Appeler Richard': 'Call Richard', 'Écrire à Richard': 'Email Richard',
    # Entreprises
    'Aperçu de votre événement d’entreprise': 'Your corporate event at a glance',
    'Demande événement d’entreprise': 'Corporate event enquiry',
    'Contact identifié': 'Contact identified',
    'Préparer mon événement': 'Plan my event',
    'Date de votre événement d’entreprise': 'Event date',
    'À quelle date aura lieu votre événement d’entreprise ?': 'When is your corporate event?',
    'Dans quel secteur se déroulera votre événement d’entreprise ?': 'Where will your corporate event take place?',
    'La date et le lieu de votre événement d’entreprise sont-ils déjà confirmés ?': 'Are the date and venue of your event already confirmed?',
    'Commençons par la date prévue pour votre événement d’entreprise.': 'Let’s start with the date of your event.',
    'Ex. : Centre de séminaire': 'E.g. a conference centre',
    'Accueil / cocktail': 'Welcome / cocktail hour', 'Discours / présentation': 'Speeches / presentation',
    'Sonorisation & micros': 'Sound & microphones', 'Éclairage d’ambiance': 'Ambient lighting',
    'Vidéoprojection & écran': 'Video projection & screen',
    'Avez-vous déjà une idée précise pour la musique de votre événement d’entreprise ?': 'Do you already have a clear idea for the music at your event?',
    'Où en est aujourd’hui l’organisation de votre événement d’entreprise ?': 'Where are you with planning your event?',
    'PRESTATIONS POUR LES ENTREPRISES\n\n• DJ & ambiance musicale pour cocktails, séminaires et soirées d’entreprise\n• Sonorisation et micros pour discours et présentations\n• Éclairage d’ambiance et de la piste de danse\n• Photobooth\n• Vidéoprojection et écran\n• Réceptions, inaugurations et soirées spéciales':
        'SERVICES FOR COMPANIES\n\n• DJ & music for cocktail hours, seminars and company parties\n• Sound and microphones for speeches and presentations\n• Ambient and dance floor lighting\n• Photo booth\n• Video projection and screen\n• Receptions, launches and special evenings',
    'RICHARD DJ EVENT\nBasé au Pays basque · Interventions au Pays basque et dans les Landes\n\n06 84 33 18 24\nricharddjevent@gmail.com\n\nDisponible 7j/7 sur rendez-vous · Réponse sous 24 h.':
        'RICHARD DJ EVENT\nBased in the French Basque Country · Available worldwide\n\n+33 6 84 33 18 24\nricharddjevent@gmail.com\n\nAvailable 7 days a week by appointment · Reply within 24 hours · English-speaking support available.',
    # Bars et restaurants
    'Aperçu de votre soirée en établissement': 'Your venue night at a glance',
    'Demande soirée en établissement': 'Venue night enquiry',
    'Date de votre soirée en établissement': 'Date of the night',
    'À quelle date aura lieu votre soirée en établissement ?': 'When is the night at your venue?',
    'Dans quel secteur se déroulera votre soirée en établissement ?': 'Where is your venue?',
    'La date et le lieu de votre soirée en établissement sont-ils déjà confirmés ?': 'Are the date and venue already confirmed?',
    'Commençons par la date prévue pour votre soirée en établissement.': 'Let’s start with the date of your night.',
    'Ex. : Nom du bar ou restaurant': 'E.g. the name of your bar or restaurant',
    'Apéritif / afterwork': 'Aperitif / after-work drinks', 'Dîner musical': 'Dinner with music',
    'Soirée festive': 'Party night', 'Privatisation': 'Private hire',
    'Avez-vous déjà une idée précise pour la musique de votre soirée en établissement ?': 'Do you already have a clear idea for the music on the night?',
    'Où en est aujourd’hui l’organisation de votre soirée en établissement ?': 'Where are you with planning the night?',
    'PRESTATIONS POUR LES BARS & RESTAURANTS\n\n• DJ & ambiance musicale pour apéritifs, dîners et soirées festives\n• Sonorisation adaptée à votre salle ou terrasse et micros\n• Éclairage d’ambiance et de la piste de danse\n• Photobooth\n• Vidéoprojection et écran\n• Privatisations, lancements de saison et soirées spéciales':
        'SERVICES FOR BARS & RESTAURANTS\n\n• DJ & music for aperitif hours, dinners and party nights\n• Sound suited to your room or terrace, plus microphones\n• Ambient and dance floor lighting\n• Photo booth\n• Video projection and screen\n• Private hire, season launches and special nights',
}

# Clés techniques, jamais affichées : ne pas traduire.
TECHNIQUES = {'theme', 'start', 'contactEndpoint', 'recipient', 'turnstileSiteKey', 'source', 'match', 'ctaHref',
              'qualificationMode', 'key', 'next', 'type'}
manquants = []

def tr(texte):
    if texte in T:
        return T[texte]
    manquants.append(texte)
    return texte

def est_identifiant(v):
    return bool(re.fullmatch(r'[a-z][a-zA-Z_]*|tel:.*|mailto:.*', v))

def traduire(o, cle=None):
    if isinstance(o, str):
        return o if est_identifiant(o) else tr(o)
    if isinstance(o, list):
        return [traduire(x) for x in o]
    if isinstance(o, dict):
        sortie = {}
        for k, v in o.items():
            if k in TECHNIQUES and k != 'start':
                sortie[k] = v
            elif k == 'start' and isinstance(v, str):
                sortie[k] = v
            elif k == 'fieldsByIntent':
                sortie[k] = {tr(kk): traduire(vv) for kk, vv in v.items()}
            else:
                sortie[k] = traduire(v, k)
        return sortie
    return o

def adapter(conf, page):
    c = traduire(conf)
    c['source'] = 'https://djmariagepaysbasque.fr' + page
    # Clientèle internationale : un choix « hors de France » en plus des secteurs locaux.
    for step in c['steps'].values():
        if step.get('key') == 'location':
            suite = step['choices'][-1][1]
            step['choices'].append(['Outside France', suite])
    return c

configs = {
    'wedding': adapter(config_de('public/assistant-richard.js'), '/en/'),
    'corporate': adapter(config_de('public/evenements-assets/assistant-entreprises.js'), '/en/corporate-events/'),
    'bars': adapter(config_de('public/evenements-assets/assistant-bars-restaurants.js'), '/en/bars-restaurants/'),
}

if manquants:
    print('Textes de configuration sans traduction :')
    for m in dict.fromkeys(manquants):
        print('  -', repr(m))
    sys.exit(1)

source = (RACINE / 'public/assistant-richard.js').read_text()
choix = (
    'var configsEn = ' + json.dumps(configs, ensure_ascii=False) + ';\n'
    '      var cheminEn = window.location.pathname;\n'
    '      var cleEn = cheminEn.indexOf("/en/corporate-events") === 0 ? "corporate" : cheminEn.indexOf("/en/bars-restaurants") === 0 ? "bars" : "wedding";\n'
    '      configElement.textContent = JSON.stringify(configsEn[cleEn]);\n'
)
source, n = re.subn(r'configElement\.textContent = ".*?";\n', lambda m: choix, source, count=1)
assert n == 1

# Textes de l'interface (moteur commun). Chaque remplacement doit trouver sa cible.
CODE = [
    ('var launcherStatus = isRealAssistant ? "Réponse immédiate" : "Réponse immédiate · Démo";', 'var launcherStatus = isRealAssistant ? "Instant reply" : "Instant reply · Demo";'),
    ('var headerStatus = isRealAssistant ? "En ligne · Réponse immédiate" : "En ligne · Simulation interactive";', 'var headerStatus = isRealAssistant ? "Online · Instant reply" : "Online · Interactive demo";'),
    ('"Vos informations sont sécurisées et transmises uniquement à Richard DJ." : "Démonstration : aucune donnée n’est collectée."', '"Your details are secure and only shared with Richard DJ." : "Demo: no data is collected."'),
    ('"Ouvrir l’assistant Richard DJ" : "Ouvrir la démonstration"', '"Open the Richard DJ assistant" : "Open the demo"'),
    ('(isRealAssistant ? "Assistant Richard DJ" : "Démonstration de l’assistant")', '(isRealAssistant ? "Richard DJ Assistant" : "Assistant demo")'),
    ("<button class='home' type='button'>Menu principal</button><button class='close' type='button' aria-label='Fermer'>", "<button class='home' type='button'>Main menu</button><button class='close' type='button' aria-label='Close'>"),
    ('"L’appel vers " + destination + " va s’ouvrir sur votre appareil."', '"Your device will now call " + destination + "."'),
    ('"Votre messagerie va s’ouvrir avec l’adresse " + destination + " préremplie."', '"Your email app will open with " + destination + " already filled in."'),
    ("<p class='form-note'><strong>Plusieurs réponses possibles.</strong><br>Vous pouvez également tout sélectionner en un clic.</p>", "<p class='form-note'><strong>Several answers possible.</strong><br>You can also select everything in one click.</p>"),
    ('"Valider mes choix"', '"Confirm my choices"'),
    ("<button class='select-all' type='button'>Tout sélectionner</button>", "<button class='select-all' type='button'>Select all</button>"),
    ('shouldSelect ? "Tout désélectionner" : "Tout sélectionner"', 'shouldSelect ? "Deselect all" : "Select all"'),
    ('step.label || "Date souhaitée"', 'step.label || "Preferred date"'),
    ('"Pour que Richard puisse vous rappeler, indiquez vos coordonnées."', '"So that Richard can call you back, please enter your details."'),
    ('"Dernière étape : indiquez vos coordonnées pour transmettre votre demande à Richard."', '"Last step: enter your details to send your request to Richard."'),
    ("<p class='form-note'><strong>Vos coordonnées</strong><br>Les champs marqués d’un astérisque sont obligatoires.</p>", "<p class='form-note'><strong>Your details</strong><br>Fields marked with an asterisk are required.</p>"),
    ("<label>Prénom *<input name='firstName'", "<label>First name *<input name='firstName'"),
    ("<label>Nom *<input name='lastName'", "<label>Last name *<input name='lastName'"),
    ("<label>E-mail *<input name='email'", "<label>Email *<input name='email'"),
    ("<label>Téléphone *<input name='phone'", "<label>Phone *<input name='phone'"),
    ('<span>J’accepte que mes informations soient utilisées par Richard DJ Event pour répondre à ma demande.</span>', '<span>I agree that Richard DJ Event may use my details to reply to my request.</span>'),
    ("<p class='secure-note'>🔒 Protection antispam Cloudflare Turnstile.</p>", "<p class='secure-note'>🔒 Anti-spam protection by Cloudflare Turnstile.</p>"),
    ("<p class='form-error'>Vérifiez vos coordonnées et acceptez l’utilisation de vos informations.</p>", "<p class='form-error'>Please check your details and accept the use of your information.</p>"),
    ('"Veuillez valider la protection antispam avant l’envoi."', '"Please complete the anti-spam check before sending."'),
    ('"Envoi en cours…"', '"Sending…"'),
    ('"Nouvelle demande depuis l’assistant Richard DJ",', '"Nouvelle demande depuis l’assistant Richard DJ, version ANGLAISE du site (client anglophone)",'),
    ('payload.append("Site d’origine", "Pays Basque — https://djmariagepaysbasque.fr");', 'payload.append("Site d’origine", "Pays Basque, version anglaise : " + window.location.href);\n              payload.append("Langue", "Anglais (demande envoyée depuis la version anglaise du site)");'),
    ('" · Coordonnées transmises"', '" · Details sent"'),
    ('"L’envoi n’a pas abouti. Réessayez ou contactez Richard directement."', '"Your request could not be sent. Please try again or contact Richard directly."'),
    ('language: "fr",', 'language: "en",'),
    ('"La protection antispam n’a pas pu se charger. Rechargez la page."', '"The anti-spam check could not load. Please reload the page."'),
    ('"<strong>Votre demande a bien été envoyée</strong>" +', '"<strong>Your request has been sent</strong>" +'),
    ('"<p>Merci " + escapeHtml(answers.firstName) + ". Richard a reçu votre " +', '"<p>Thank you " + escapeHtml(answers.firstName) + ". Richard has received your " +'),
    ('(mode === "callback" ? "demande de rappel" : "projet de mariage") +\n        " et vous répondra sous 24 h.</p>" +', '(mode === "callback" ? "call-back request" : "request") +\n        " and will reply within 24 hours.</p>" +'),
    ("<div class='badges'><span>✓ Envoi sécurisé</span><span>✓ Richard prévenu</span><span>✓ Réponse sous 24 h</span></div>", "<div class='badges'><span>✓ Sent securely</span><span>✓ Richard notified</span><span>✓ Reply within 24 hours</span></div>"),
    # Qualification (calcul interne, résultat envoyé à Richard en français) : clés = réponses anglaises.
    ('"Oui, la date et le lieu sont confirmés": 2,', '"Yes, the date and venue are confirmed": 2,'),
    ('"La date et le lieu sont confirmés": 4,', '"The date and venue are confirmed": 4,'),
    ('"La date est confirmée, le lieu reste à choisir": 3,', '"The date is set, the venue is still to be chosen": 3,'),
    ('"La date est encore flexible": 0,', '"The date is still flexible": 0,'),
    ('"L’organisation est en cours": 1,', '"Planning is under way": 1,'),
    ('"Je prends simplement des renseignements": 0\n', '"I am just gathering information": 0\n'),
    ('"Je commence mes recherches": 0,', '"I am just starting to look": 0,'),
    ('"Je compare plusieurs DJ": 1,', '"I am comparing several DJs": 1,'),
    ('"J’ai déjà reçu un ou plusieurs devis": 2,', '"I have already received one or more quotes": 2,'),
    ('"Notre choix est presque arrêté": 3,', '"We have almost decided": 3,'),
    ('"Nous devons remplacer un DJ devenu indisponible": 4\n', '"We need to replace a DJ who is no longer available": 4\n'),
    ('answers.intent !== "Demande de disponibilité"', 'answers.intent !== "Check availability"'),
    ('answers.moments.indexOf("Soirée dansante")', 'answers.moments.indexOf("Dance party")'),
    ('answers.djSearchStatus === "Nous devons remplacer un DJ devenu indisponible"', 'answers.djSearchStatus === "We need to replace a DJ who is no longer available"'),
    ('reason = answers.intent === "Demande de disponibilité"', 'reason = answers.intent === "Check availability"'),
]
for avant, apres in CODE:
    assert source.count(avant) >= 1, avant
    source = source.replace(avant, apres)
# Textes répétés à plusieurs endroits du moteur.
for avant, apres in [
    ('"Revenir au menu principal"', '"Back to main menu"'),
    ('"Terminer la démonstration"', '"End the demo"'),
    ('"Valider cette date"', '"Confirm this date"'),
    ('"Demander à être rappelé"', '"Request a call back"'),
    ('"Envoyer ma demande"', '"Send my request"'),
    ('"Appeler Richard"', '"Call Richard"'),
    ('"À préciser"', '"Not specified"'),
    ('new Intl.DateTimeFormat("fr-FR"', 'new Intl.DateTimeFormat("en-GB"'),
]:
    assert avant in source, avant
    source = source.replace(avant, apres)

entete = '// Version anglaise générée par outils/traduire-assistant-en.py (ne pas modifier à la main).\n'
(RACINE / 'public/assistant-richard-en.js').write_text(entete + source)
print('OK public/assistant-richard-en.js')
