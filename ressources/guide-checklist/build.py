#!/usr/bin/env python3
"""Génère guide.html (A4 imprimable + lecture mobile) du guide Checklist & rétroplanning."""
import base64, html, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
LOGO = base64.b64encode((HERE.parent.parent / "public/logo-monogram.png").read_bytes()).decode()

def fr_html(h):
    """Espaces insécables avant : ; ! ? » et après « (jamais un signe seul en début de ligne)."""
    def corr(t):
        t = re.sub(r" ([:;!?»])", "\u00a0\\1", t)
        return t.replace("« ", "«\u00a0")
    return "".join(m if m.startswith("<") else corr(m) for m in re.split(r"(<[^>]*>)", h))

def e(t): return html.escape(t, quote=False)

# --- composants -------------------------------------------------------------
def checks(items):
    return '<ul class="checks">' + "".join(f"<li><i></i><span>{e(x)}</span></li>" for x in items) + "</ul>"

def fields(labels, hint=None, inline=False):
    cls = "fields inline" if inline else "fields"
    out = f'<div class="{cls}">'
    for l in labels:
        h = f'<small>{e(hint)}</small>' if hint else ""
        out += f'<label><b>{e(l)}</b>{h}<span class="line"></span></label>'
    return out + "</div>"

def block(title, body, level=3, keep=True):
    k = " keep" if keep else ""
    return f'<section class="block{k}"><h{level}>{e(title)}</h{level}>{body}</section>'

def p(t): return f"<p>{e(t)}</p>"
def tip(t):
    t = t[:1].upper() + t[1:]
    return f'<aside class="tip"><b>Astuce</b><span>{e(t)}</span></aside>'
def note(t): return f'<aside class="note">{e(t)}</aside>'

def stage(when, items, extra=""):
    return f'<section class="stage keep"><div class="when"><span class="dot"></span><h3>{e(when)}</h3></div>{checks(items)}{extra}</section>'

CHAPTERS = []

def chapter(num, title, intro=""):
    CHAPTERS.append((num, title))
    i = f"<p class='intro'>{e(intro)}</p>" if intro else ""
    return f'<header class="chapter" id="c{num}"><span class="num">{num}</span><h2>{e(title)}</h2>{SPRIG}{i}</header>'

SPRIG = '''<svg class="sprig" viewBox="0 0 220 24" aria-hidden="true"><path d="M2 12 H98 M122 12 H218" stroke="#c6a15b" stroke-width="1" fill="none"/>
<g transform="translate(110 12)"><circle r="3.2" fill="#fff" stroke="#c6a15b" stroke-width=".8"/>
<g fill="#9fb09a"><ellipse cx="-12" cy="-1" rx="6" ry="2.4" transform="rotate(-20 -12 -1)"/><ellipse cx="12" cy="-1" rx="6" ry="2.4" transform="rotate(20 12 -1)"/></g></g></svg>'''

# Décor floral d'angle (aquarelle stylisée, vectoriel)
FLORAL = '''<svg class="floral" viewBox="0 0 300 300" aria-hidden="true">
<g fill="#9fb09a" opacity=".85"><ellipse cx="70" cy="60" rx="46" ry="13" transform="rotate(35 70 60)"/><ellipse cx="120" cy="40" rx="42" ry="11" transform="rotate(10 120 40)"/><ellipse cx="40" cy="110" rx="40" ry="11" transform="rotate(70 40 110)"/><ellipse cx="150" cy="95" rx="34" ry="9" transform="rotate(30 150 95)"/><ellipse cx="85" cy="135" rx="34" ry="9" transform="rotate(50 85 135)"/></g>
<g fill="#7f9479" opacity=".7"><ellipse cx="95" cy="75" rx="30" ry="8" transform="rotate(45 95 75)"/><ellipse cx="55" cy="85" rx="26" ry="7" transform="rotate(-50 55 85)"/></g>
<g stroke="#e3c98f" stroke-width="1.2" fill="none"><path d="M10 10 C70 40 120 90 180 170"/><path d="M10 10 C40 60 70 120 100 200"/></g>
<g><g transform="translate(60 40)" fill="#fff" stroke="#ead9b4" stroke-width=".8"><circle cx="0" cy="-12" r="11"/><circle cx="11" cy="-4" r="11"/><circle cx="7" cy="10" r="11"/><circle cx="-7" cy="10" r="11"/><circle cx="-11" cy="-4" r="11"/><circle r="6" fill="#e3c98f" stroke="none"/></g>
<g transform="translate(135 95) scale(.8)" fill="#fbf1e6" stroke="#ead9b4" stroke-width=".8"><circle cx="0" cy="-12" r="11"/><circle cx="11" cy="-4" r="11"/><circle cx="7" cy="10" r="11"/><circle cx="-7" cy="10" r="11"/><circle cx="-11" cy="-4" r="11"/><circle r="6" fill="#c6a15b" stroke="none"/></g>
<g transform="translate(30 125) scale(.6)" fill="#fff" stroke="#ead9b4" stroke-width=".8"><circle cx="0" cy="-12" r="11"/><circle cx="11" cy="-4" r="11"/><circle cx="7" cy="10" r="11"/><circle cx="-7" cy="10" r="11"/><circle cx="-11" cy="-4" r="11"/><circle r="6" fill="#e3c98f" stroke="none"/></g>
<circle cx="105" cy="30" r="4" fill="#fff" stroke="#ead9b4"/><circle cx="170" cy="60" r="3" fill="#fff" stroke="#ead9b4"/><circle cx="20" cy="70" r="3.5" fill="#fff" stroke="#ead9b4"/></g></svg>'''

def lockup(cls):
    return (f'<div class="lockup {cls}"><span class="mark">R</span><span class="ltext">'
            '<span class="lname">Richard <em>DJ Event</em></span>'
            '<span class="ltag">DJ mariage Pays Basque &amp; Landes</span></span></div>')

# --- contenu ----------------------------------------------------------------
parts = []

parts.append(f'''<section class="cover">
<div class="fl tl">{FLORAL}</div><div class="fl br">{FLORAL}</div>
{lockup("on-light")}
<p class="kicker">Guide gratuit</p>
<h1>Checklist complète<br><em>&amp;</em> rétroplanning<br>du mariage</h1>
{SPRIG}
<p class="sub">Le guide pratique gratuit de Richard DJ Event</p>
<p class="lead">À consulter facilement sur téléphone ou à imprimer. Prenez les idées qui vous aident, adaptez le calendrier à votre date et avancez à votre rythme.</p>
</section>''')

parts.append('__TOC__')
parts.append('<main>')

# 1. Point de départ
parts.append(chapter("01", "Votre point de départ"))
parts.append(fields(["Prénoms", "Date du mariage", "Lieu"]))
parts.append(block("Votre cap à deux", checks([
    "Choisir ensemble trois priorités (par exemple : profiter de vos proches, une belle fête, un budget maîtrisé).",
    "Décider ce qui compte le plus et ce qui peut rester simple.",
    "Se mettre d'accord sur la manière de trancher en cas d'envies différentes.",
    "Prévoir un court point d'organisation régulier plutôt qu'une longue séance de temps en temps.",
    "Rassembler devis, contrats, reçus, plans et versions finales dans un espace partagé."]) +
    fields(["Nos trois priorités", "Ce que nous voulons absolument préserver", "Personnes de confiance à qui déléguer"])))
parts.append(tip("Commencez par les décisions qui influencent la date, le lieu, le budget et le confort des invités. Le reste peut souvent attendre."))

# 2. Budget
parts.append(chapter("02", "Budget et réservations"))
parts.append(checks(["Notez le prix total, les acomptes, les échéances, le déplacement, les heures supplémentaires et les options. Gardez une réserve pour les ajustements de dernière minute."]))
parts.append(block("Postes à prévoir",
    p("Pour chaque poste, notez votre enveloppe, le montant du devis, l'acompte versé, le solde et la date prévue.") +
    checks(["Lieu, mobilier et nettoyage", "Repas, boissons et éventuel brunch", "Tenues, accessoires, beauté et retouches",
            "Photographie et vidéo", "Musique, sonorisation et éclairage", "Fleurs, décoration, papeterie et signalétique",
            "Cérémonie et animations", "Transport, hébergement et garde d'enfants", "Alliances, cadeaux, frais administratifs et imprévus"]) +
    fields(["Enveloppe totale", "Réserve prévue"], inline=True)))
parts.append(tip("prévoyez environ 10 % du budget total en marge pour les imprévus. Il y en a toujours, et mieux vaut les avoir anticipés que les subir."))
parts.append(block("Avant de confirmer un prestataire", checks([
    "Vérifier précisément ce qui est inclus : durée, matériel, installation, déplacement, repas et options.",
    "Lire les modalités d'acompte, d'annulation, de report et de règlement.",
    "Faire confirmer par écrit le tarif, les horaires, l'adresse, les contraintes et le contact du jour J.",
    "Inscrire les paiements et dates limites dans un calendrier partagé.",
    "Demander au lieu ses règles de bruit, d'accès, d'installation, d'électricité et de rangement.",
    "Vérifier les accès, l'hébergement et le plan B en cas de météo difficile."]) +
    fields(["Questions à poser / devis à relancer"])))
parts.append(tip("demandez toujours un devis détaillé et signé. Il évite les malentendus et sert de référence si un détail change plus tard."))

# 3. Rétroplanning
parts.append(chapter("03", "Rétroplanning indicatif",
    "Les délais varient selon la saison, le lieu et la taille de la fête. Si vous disposez de moins de temps, gardez l'ordre des priorités et regroupez les étapes."))
parts.append('<div class="timeline">')
parts.append(stage("Dès que la date est envisagée (18 mois ou plus)", [
    "Définir une ou plusieurs dates possibles et le budget maximal.",
    "Évaluer le nombre d'invités et le format de la journée.",
    "Choisir le lieu en vérifiant capacité, accès, hébergement, bruit et solution météo.",
    "Réserver le lieu et noter les heures de remise des clés, de montage et de fin de soirée.",
    "Se renseigner tôt sur les formalités de la cérémonie et les délais de dossier.",
    "Prévenir les proches indispensables et choisir les témoins.",
    "Repérer les besoins d'hébergement et de transport des invités éloignés."],
    tip("pour un mariage en juin ou en septembre, appelez les lieux dès que la date est envisagée : les week-ends se réservent plusieurs mois à l'avance.")))
parts.append(stage("12 à 18 mois avant", [
    "Réserver les prestataires dont l'agenda se remplit tôt : repas, photo, musique, vidéo, cérémonie.",
    "Comparer les offres sur leur contenu et leurs conditions, pas uniquement sur le prix.",
    "Construire un premier budget et un calendrier des paiements.",
    "Décider si une contribution financière familiale est envisagée et la confirmer sans ambiguïté."]))
parts.append(stage("9 à 12 mois avant", [
    "Dessiner les grandes étapes : préparatifs, cérémonie, cocktail, repas, soirée.",
    "Faire une première liste d'invités et confirmer que le lieu peut les accueillir.",
    "Choisir les tenues et prévoir les rendez-vous d'essayage et les retouches.",
    "Réserver les trajets ou hébergements qui conditionnent la venue des proches.",
    "Envoyer une annonce de date aux invités si la période est chargée ou s'ils viennent de loin.",
    "Identifier les personnes qui liront un texte, feront un discours ou aideront pendant la journée."],
    fields(["Notre prochaine décision importante"]) +
    tip("créez dès maintenant un groupe de messagerie ou un album partagé pour les proches qui aident. Tout le monde s'y retrouve, et les informations ne se perdent plus.")))
parts.append(stage("6 à 9 mois avant", [
    "Envoyer les invitations avec une date claire pour répondre.",
    "Choisir repas et boissons; demander allergies et régimes alimentaires.",
    "Définir le style de décoration et distinguer ce qui sera acheté, loué ou emprunté.",
    "Préparer le déroulé de la cérémonie, les textes, les musiques et les interventions.",
    "Commander les alliances et accessoires nécessitant une fabrication ou un délai.",
    "Échanger avec le DJ sur les styles appréciés, les morceaux à éviter et les temps forts.",
    "Transmettre aux invités les informations d'accès, de stationnement et de logement."],
    tip("ajoutez un lien ou un QR code à l'invitation pour répondre en ligne. Les réponses arrivent plus vite et vous les retrouvez au même endroit.")))
parts.append(stage("4 à 6 mois avant", [
    "Faire le point sur les réponses et relancer les personnes indispensables.",
    "Confirmer les horaires d'arrivée, d'installation et de rangement avec chaque prestataire.",
    "Commander les éléments personnalisés ou imprimés avec délais de fabrication.",
    "Commencer le plan de table en tenant compte des enfants, aînés et situations familiales.",
    "Prévoir la liste des photos de groupe et une personne pour réunir les proches.",
    "Nommer la personne qui gardera alliances, enveloppes, cadeaux et objets précieux.",
    "Déterminer qui décide du plan B en cas de pluie, de vent ou de forte chaleur."],
    fields(["À commander / réserver maintenant", "Invités ou prestataires à relancer"])))
parts.append(stage("Un mois avant", [
    "Relancer les réponses manquantes et convenir d'une dernière date de retour.",
    "Transmettre au traiteur un effectif provisoire, les besoins alimentaires et les contraintes d'accès.",
    "Reconfirmer adresses, horaires, montage, matériel et contacts utiles avec tous les prestataires.",
    "Finaliser plan de table, menus, marque-places et signalétique.",
    "Valider les musiques, annonces, discours et surprises avec les personnes concernées.",
    "Écrire une feuille de route d'une page pour la personne référente.",
    "Étiqueter les caisses de décoration par zone et préciser qui installe et qui récupère.",
    "Garder de la marge dans le programme et simplifier les transitions trop serrées."],
    tip("imprimez la feuille de route sur une seule page. C'est le document que votre personne référente sortira en premier en cas de question.")))
parts.append(stage("Deux semaines avant", [
    "Confirmer le nombre final d'invités et les heures de livraison.",
    "Faire le dernier essayage et réunir tenue, chaussures, accessoires et vêtements de rechange.",
    "Imprimer ou partager le déroulé, le plan de table, les contacts et les adresses.",
    "Prévoir une copie de secours des musiques et documents importants.",
    "Préparer les règlements uniquement s'ils ont été convenus avec les prestataires."]))
parts.append(stage("La semaine du mariage", [
    "Reconfirmer les rendez-vous, livraisons et horaires de chaque intervenant.",
    "Préparer une trousse : pansements, épingles, ciseaux, mouchoirs, détachant, chargeur et eau.",
    "Confier les appels et questions pratiques à une personne qui n'est pas l'un des mariés.",
    "Regrouper les tenues complètes et noter les trajets, stationnements et heures de départ.",
    "Prévoir de quoi manger, boire et souffler pour les mariés et les proches qui aident."],
    tip("glissez chaque règlement dans une enveloppe au nom du prestataire, avec le montant écrit dessus, et confiez-les à la personne qui les remettra. Un souci de moins le jour J.")))
parts.append('</div>')

# 4. Jour J
parts.append(chapter("04", "La veille, le jour J et après"))
parts.append('<div class="timeline">')
parts.append(stage("La veille", [
    "Déposer le matériel sur place si le lieu l'autorise et demander confirmation.",
    "Vérifier alliances, documents, chaussures, tenues, accessoires et chargeurs.",
    "Faire un point rapide avec les référents et transmettre les numéros utiles.",
    "Consulter la météo et rappeler qui décide du plan B, à quelle heure et selon quel critère.",
    "Éviter les changements tardifs qui n'améliorent ni le confort ni le déroulé."]))
parts.append(stage("Le jour même", [
    "Garder des marges pour les trajets, les photos et les changements de lieu.",
    "Avoir de l'eau et de quoi grignoter à portée de main.",
    "Confier les alliances et les objets importants à une personne nommée.",
    "Indiquer aux prestataires un contact d'urgence autre que les mariés.",
    "Désigner une personne pour relayer toute modification aux invités.",
    "Se servir du programme comme repère, pas comme chronomètre.",
    "S'accorder quelques minutes à deux, loin des sollicitations."],
    tip("mangez vraiment quelque chose le matin et gardez une bouteille d'eau à portée de main. La journée est longue, et on oublie vite de s'arrêter.")))
parts.append(stage("Après la fête", [
    "Organiser le rangement, le tri des objets et le retour des locations.",
    "Vérifier les affaires confiées aux témoins et les objets oubliés sur place.",
    "Régler les soldes prévus et classer les factures.",
    "Remercier les personnes qui ont aidé et les prestataires.",
    "Sauvegarder les photos reçues et archiver les documents utiles."]))
parts.append('</div>')
parts.append(note("En cas d'imprévu, la personne référente consulte la feuille de route et contacte le bon interlocuteur. Les mariés peuvent rester avec leurs invités."))

# 5. Déroulé
parts.append('<div class="keep">')
parts.append(chapter("05", "Déroulé de la journée",
    "Prévoyez du temps pour circuler, accueillir, manger et respirer. Remplissez ces repères avec le lieu et les prestataires."))
rows = "".join(f'<tr><td class="n">{i}</td>' + "".join(f'<td data-l="{l}"><span class="cl"></span></td>' for l in ("Heure", "Moment et endroit", "Personne référente", "Matériel ou remarque")) + '</tr>' for i in range(1, 9))
parts.append(f'<table class="grid keep"><thead><tr><th></th><th>Heure</th><th>Moment et endroit</th><th>Personne référente</th><th>Matériel ou remarque</th></tr></thead><tbody>{rows}</tbody></table></div>')
parts.append(tip("prévoyez deux fois plus de temps que prévu pour les photos de groupe. Rassemblez les proches à l'avance et gardez la liste des groupes sous la main."))
parts.append(block("À faire confirmer avec le lieu", checks([
    "Horaires d'accès, remise des clés, fin de musique et fermeture.",
    "Niveau sonore autorisé, notamment dehors, et éventuelles consignes du voisinage.",
    "Puissance électrique, prises, cheminement des câbles et zone d'installation.",
    "Livraisons, stationnement, accès sans marche, espace enfants et emplacement de la piste.",
    "Personne responsable de l'ouverture, des clés, de l'alarme et de la fermeture.",
    "Emplacement de repli si la cérémonie ou le cocktail est prévu dehors."])))
parts.append(block("Contacts utiles le jour J",
    fields(["Témoin référent", "Lieu / réception", "Traiteur", "Photo / vidéo", "DJ / son"], hint="nom et téléphone")))

# 6. Invités, cérémonie, déco
parts.append(chapter("06", "Invités, cérémonie et décoration"))
parts.append(block("Invités", checks([
    "Donner une date limite de réponse et un moyen simple de confirmer leur présence.",
    "Recueillir allergies et besoins d'accessibilité; partager uniquement les informations utiles aux prestataires.",
    "Prévoir un accueil clair et des indications vers la cérémonie et la réception.",
    "Communiquer horaires, adresse, stationnement et options d'hébergement.",
    "Organiser les retours si le lieu est isolé ou si la soirée finit tard."])))
parts.append(block("Cérémonie", checks([
    "Confirmer l'ordre d'entrée, les places et les rôles de chaque participant.",
    "Rassembler textes, musiques, alliances et exemplaires de secours.",
    "Tester le micro et l'audibilité depuis les derniers rangs.",
    "Nommer une personne pour coordonner les textes et petits imprévus.",
    "Prévoir assises, eau et ombre en cas de cérémonie extérieure."])))
parts.append(block("Décoration : prévoir chaque zone",
    p("Pour chaque espace, écrivez les éléments nécessaires, la personne chargée de l'installation, l'heure d'arrivée, les consignes du lieu et la personne qui range.") +
    fields(["Cérémonie", "Cocktail", "Tables et repas", "Accueil et signalétique", "Piste et soirée"], hint="éléments / installation / rangement")))
parts.append(block("Petits kits à prévoir", checks([
    "Cérémonie : alliances, textes, stylos, mouchoirs, musique et chargeur.",
    "Accueil : listes d'invités, plan, marque-places de secours et signalétique.",
    "Installation : ciseaux, ruban autorisé par le lieu, ficelle, piles et consignes de montage.",
    "Rangement : boîtes, sacs, étiquettes et responsable pour les objets à récupérer."])))

# 7. Ambiance
# Plan de table
parts.append(chapter("07", "Le plan de table sans prise de tête",
    "C'est souvent la partie de l'organisation qui donne le plus de maux de tête. Avec une méthode simple, on s'en sort en une soirée."))
parts.append(block("Avant de placer qui que ce soit", checks([
    "Fixer le nombre de places par table : huit à dix invités permettent à tout le monde de se parler.",
    "Décider de la table des mariés, face aux invités ou au milieu d'eux.",
    "Noter les places à réserver : grands-parents, personnes à mobilité réduite, familles avec enfants en bas âge.",
    "Repérer les tensions familiales et les amitiés fortes, pour ne rien laisser au hasard sur ces points.",
    "Prévoir quelques places de secours par table, car il y a toujours un changement de dernière minute."]) +
    fields(["Nombre de tables", "Invités par table"], inline=True)))
parts.append(block("La méthode simple en quatre étapes", checks([
    "Faire des groupes : famille proche, amis d'enfance, collègues, amis du couple.",
    "Écrire chaque invité sur un petit papier de couleur, une couleur par groupe.",
    "Poser les papiers sur une grande feuille ou une table, et déplacer les groupes jusqu'à ce que tout s'équilibre.",
    "Mélanger un ou deux invités de chaque groupe pour favoriser les rencontres, puis relire avec une personne de confiance."])))
parts.append(tip("placez d'abord les groupes évidents (amis d'enfance, collègues, famille proche). Il ne reste ensuite que quelques personnes à répartir, et les ajustements de dernière minute se font en deux minutes."))
parts.append(block("L'option tirage au sort", p("Pour un mariage à taille humaine, ou si le plan de table vous donne des sueurs froides, laissez le hasard décider. C'est drôle, et ça vous épargne des heures de réflexion.") + checks([
    "Numéroter les tables et préparer autant de jetons, de cartes ou de petits papiers numérotés qu'il y a de places.",
    "Réserver à l'avance la table des mariés, celle des grands-parents et les places à mobilité réduite : tout le monde ne peut pas piocher.",
    "Poser un bocal ou un panier à l'accueil, et inviter chacun à piocher son numéro en arrivant.",
    "Afficher la liste des tables avec un nom original (villes, chansons, voyages) pour que chacun retrouve la sienne.",
    "Annoncer le principe dans l'invitation ou pendant le cocktail, pour que ce soit un jeu et non une surprise.",
    "Garder quelques places libres par table pour les couples et les familles qui préfèrent rester ensemble."])))
parts.append(tip("le tirage au sort fonctionne très bien jusqu'à environ soixante invités : on fait des rencontres, on rit au moment de piocher, et personne n'est vexé de sa place. Pour un mariage plus grand, réservez les tables de famille et tirez au sort les autres."))
parts.append(block("Votre plan de table en quelques mots", fields(["Notre méthode (classique ou tirage au sort)", "Tables à réserver", "Contraintes à ne pas oublier", "Noms de tables choisis"])))

parts.append(chapter("08", "Ambiance, musique et prestataires"))
parts.append(block("Les repères musicaux",
    p("Indiquez les choix indispensables, puis laissez de la place aux échanges et à l'énergie des invités.") +
    fields(["Arrivée des invités", "Entrée des mariés", "Moment symbolique", "Ouverture de bal", "Dernier morceau"], hint="titre / interprète / remarque") +
    fields(["Morceaux à éviter"], hint="titre / raison éventuelle")))
parts.append(block("Informations à transmettre au DJ", checks([
    "Styles que vous aimez, styles que vous évitez et place souhaitée aux demandes des invités.",
    "Prononciation des noms, annonces, surprises confidentielles et personnes à présenter.",
    "Configuration de la salle, place de la piste, limites sonores et heure de fin.",
    "Horaires des moments clés et contact du référent présent sur place.",
    "Besoins de micros et de sonorisation pour cérémonie, discours ou animations."]) +
    fields(["Ambiance souhaitée en quelques mots"])))
parts.append(tip("notez trois ou quatre morceaux indispensables et deux ou trois à éviter, puis laissez votre DJ lire la salle. C'est ce qui donne les soirées où la piste ne désemplit pas."))
parts.append(block("Suivi des prestataires",
    p("Pour chacun, gardez le contact, ce qui a été convenu et la prochaine action avec son échéance.") +
    fields(["Lieu", "Repas / boissons", "Photo / vidéo", "DJ / son / lumière", "Fleurs / décoration", "Transport / hébergement"], hint="contact / prochaine action")))
parts.append(block("Documents à conserver au même endroit", checks([
    "Contrats, devis acceptés, modalités de report et justificatifs de paiement.",
    "Factures, acomptes réglés et soldes restants.",
    "Plan du lieu, consignes, autorisations et adresses d'accès.",
    "Plan de table, besoins alimentaires, liste de contacts et déroulé final."]) +
    p("Une copie accessible hors ligne à la personne qui coordonne la journée.") +
    fields(["Notes et questions à traiter"])))
parts.append(tip("photographiez chaque contrat et chaque reçu avec votre téléphone. Toute la paperasse tient alors dans votre poche, accessible le jour J."))

parts.append('</main>')
parts.append(f'''<footer class="end">
<div class="fl tl">{FLORAL}</div>
{lockup("on-dark")}
{SPRIG}
<p class="merci">Belle préparation à vous deux.</p>
<p>Cette ressource est gratuite et offerte par Richard DJ Event. Elle rassemble des repères pratiques à adapter librement à votre célébration.</p>
<p class="cta">Envie d'une soirée inoubliable ? Parlons de votre mariage.</p>
<p class="sites">djmariagepaysbasque.fr<br>djmariagelandes.fr</p>
</footer>''')

CSS = (HERE / "style.css").read_text()
MOBILE_PRINT = (HERE / "mobile-print.css").read_text()
PAGES = json.loads((HERE / "pages.json").read_text()) if (HERE / "pages.json").exists() else {}

def toc(variant):
    nums = PAGES.get(variant, {})
    items = "".join(
        f'<li><a href="#c{n}"><span class="tn">{n}</span><span class="tt">{e(t)}</span>'
        f'<span class="tl"></span><span class="tp">{nums.get(n, "")}</span></a></li>' for n, t in CHAPTERS)
    return (f'<nav class="toc" aria-label="Sommaire"><p class="kicker">Sommaire</p><h2>Au fil du guide</h2>{SPRIG}'
            f'<ol>{items}</ol>'
            '<aside class="mode"><b>Mode d’emploi</b><span>Ce guide se remplit directement à l’écran : cochez les cases '
            'et écrivez dans les lignes depuis votre ordinateur ou votre téléphone (Adobe Acrobat Reader, Aperçu sur Mac, '
            'Fichiers sur iPhone), puis choisissez « Enregistrer » pour que vos réponses restent dans le fichier (dans un navigateur ou l’aperçu d’une messagerie, elles ne sont pas gardées). '
            'Plus simple : la version en ligne enregistre toute seule (lien dans l’e-mail). Vous préférez le papier ? Il s’imprime en A4. '
            'Touchez un chapitre du sommaire pour y aller directement.</span></aside></nav>')

def page(variant, css_extra):
    body = fr_html("".join(parts).replace("__TOC__", toc(variant)))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Checklist complète et rétroplanning du mariage | Richard DJ Event</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<style>{CSS}{css_extra}</style></head><body>{body}</body></html>'''

(HERE / "guide.html").write_text(page("a4", ""), encoding="utf-8")
(HERE / "guide-mobile.html").write_text(page("mobile", MOBILE_PRINT), encoding="utf-8")
print("guide.html + guide-mobile.html générés", "(numéros de page :", "oui)" if PAGES else "non)")
