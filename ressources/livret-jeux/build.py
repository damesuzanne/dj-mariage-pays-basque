#!/usr/bin/env python3
"""Génère livret.html (A4) et livret-mobile.html du livret de jeux de mariage."""
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
def tip(t): return f'<aside class="tip"><b>Astuce</b><span>{e(t)}</span></aside>'
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
# Livret de jeux de mariage : 12 jeux menés par les invités et les témoins.

def jeu(num, titre, accroche, regles, corps="", duree=""):
    d = f'<span class="duree">{e(duree)}</span>' if duree else ""
    r = "".join(f"<li>{e(x)}</li>" for x in regles)
    return (f'<section class="block jeu"><div class="jeu-head"><span class="jeu-num">Jeu {num}</span>{d}</div>'
            f'<h3>{e(titre)}</h3><p class="accroche">{e(accroche)}</p>'
            f'<ul class="regles">{r}</ul>{corps}</section>')

def duo(questions):
    return '<ul class="checks duos">' + "".join(
        f'<li><span>{e(q)}</span><span class="duo"><i></i><em>Elle</em><i></i><em>Lui</em></span></li>' for q in questions) + "</ul>"

def liste_lignes(items, hint=None):
    """Consignes courtes, chacune suivie d'une ligne à remplir."""
    return fields(items, hint=hint)

def grid(entetes, n, premier="N°", lignes=None):
    th = "".join(f"<th>{e(h)}</th>" for h in entetes)
    rows = ""
    for i in range(1, n + 1):
        lab = lignes[i - 1] if lignes else str(i)
        rows += f'<tr><td class="n">{e(lab)}</td>' + "".join(
            f'<td data-l="{e(h)}"><span class="cl"></span></td>' for h in entetes) + "</tr>"
    return f'<table class="grid keep"><thead><tr><th>{e(premier)}</th>{th}</tr></thead><tbody>{rows}</tbody></table>'

def cartes(titres):
    return '<div class="cartes">' + "".join(
        f'<div class="carte"><b>{e(t)}</b><span class="line"></span><span class="line"></span></div>' for t in titres) + "</div>"

parts = []

parts.append(f'''<section class="cover">
<div class="fl tl">{FLORAL}</div><div class="fl br">{FLORAL}</div>
{lockup("on-light")}
<p class="kicker">Livret gratuit</p>
<h1>Le livret de jeux<br><em>de</em> mariage</h1>
{SPRIG}
<p class="sub">12 jeux menés par vos invités et vos témoins</p>
<p class="lead">Des jeux simples à imprimer ou à remplir sur téléphone, pour le cocktail, le repas et la fin de soirée. Choisissez ceux qui vous ressemblent, confiez-les à vos proches, et profitez.</p>
</section>''')

parts.append('__TOC__')
parts.append('<main>')

# 01 ---------------------------------------------------------------------------
parts.append(chapter("01", "Avant de commencer",
    "Un jeu réussi tient à peu de choses : un bon moment dans la journée, quelqu'un pour le lancer, et des règles qui tiennent en trois phrases."))
parts.append(block("Les cinq règles d'or", checks([
    "Trois jeux suffisent. Mieux vaut peu de jeux bien menés que beaucoup de jeux survolés.",
    "Chaque jeu dure dix minutes au plus, jamais plus longtemps qu'un plat.",
    "Personne n'est obligé de jouer : tout le monde peut simplement regarder et rire.",
    "Un proche ou un témoin lance le jeu et explique la règle, en une minute.",
    "Un jeu qui ne prend pas s'arrête sans état d'âme, on passe au suivant."])))
parts.append(block("Choisir selon le moment", checks([
    "Cocktail : jeux libres, qu'on peut commencer et arrêter quand on veut (jeux 1 et 2).",
    "Repas : jeux de table, entre deux plats, pour faire connaissance (jeux 3, 4 et 5).",
    "Avec les témoins : moments plus théâtraux, à lancer quand l'ambiance est installée (jeux 6, 7 et 8).",
    "Enfants : leurs propres missions, pour qu'ils aient leur place dans la journée (jeux 9 et 10).",
    "Fin de soirée : jeux calmes, quand les invités ont besoin de souffler (jeux 11 et 12)."])))
parts.append(block("Le matériel à prévoir", checks([
    "Des stylos ou crayons (en prévoir plus que nécessaire).",
    "Des cartes de papier épais ou des feuilles imprimées de ce livret.",
    "Un panier, un bocal ou une boîte pour récupérer les réponses.",
    "Un minuteur ou un sablier pour les jeux de mime.",
    "Quelques petites récompenses : chocolats, bouteille, stylo gravé, ce qui vous fait plaisir."])))
parts.append(block("Votre plan de jeu",
    p("Notez ici les jeux retenus, le moment où ils auront lieu et la personne qui les lance. Pensez à prévenir vos prestataires des moments où l'ambiance sera plus calme.") +
    grid(["Moment", "Jeu choisi", "Qui le lance", "Matériel"], 5, premier="N°")))

# 02 ---------------------------------------------------------------------------
parts.append(chapter("02", "Au cocktail",
    "Les invités arrivent, ne se connaissent pas tous, et cherchent une façon de briser la glace. Ces deux jeux s'organisent tout seuls."))
parts.append(jeu(1, "Les défis photo",
    "Dix petites missions à réaliser avec son téléphone. À la fin, on regarde les plus belles photos ensemble.",
    ["Chaque défi réussi se coche.",
     "Les photos s'envoient à un témoin, ou dans un album partagé que vous créez avant le jour J."],
    checks([
        "Un selfie avec les mariés",
        "La photo de groupe la plus drôle",
        "Trois générations différentes sur la même photo",
        "Les mains de plusieurs invités qui trinquent",
        "Le détail de décoration que vous préférez",
        "Un invité qui rit aux éclats",
        "Les plus belles chaussures de la fête",
        "Une photo avec le plus jeune des invités",
        "Deux invités qui imitent une pose de mariage",
        "Un moment de lumière dont vous voulez garder le souvenir"]), duree="Pendant le cocktail"))

parts.append(jeu(2, "La chasse aux signatures",
    "Chaque invité reçoit la liste et part trouver une personne qui correspond à chaque phrase.",
    ["Une personne ne peut signer qu'une seule fois par feuille.",
     "Le premier à remplir sa feuille (ou le plus de cases à la fin du cocktail) gagne une petite récompense.",
     "Imprimez-en une par invité, ou une par table."],
    liste_lignes([
        "Trouvez quelqu'un qui connaît les mariés depuis plus de vingt ans",
        "Trouvez quelqu'un qui est venu de plus de trois cents kilomètres",
        "Trouvez quelqu'un qui parle au moins trois langues",
        "Trouvez quelqu'un qui est né le même mois que l'un des mariés",
        "Trouvez quelqu'un qui a déjà été témoin à un mariage",
        "Trouvez quelqu'un qui sait faire un nœud de cravate sans aide",
        "Trouvez quelqu'un qui a déjà dansé un rock",
        "Trouvez quelqu'un dont le prénom commence par la même lettre que le vôtre",
        "Trouvez quelqu'un qui porte quelque chose de vert",
        "Trouvez quelqu'un qui s'est marié il y a plus de dix ans",
        "Trouvez quelqu'un qui a un mouchoir dans son sac ou sa poche",
        "Trouvez quelqu'un qui n'a encore jamais rencontré les mariés avant aujourd'hui",
    ], hint="signature"), duree="Tout le cocktail"))

# 03 ---------------------------------------------------------------------------
parts.append(chapter("03", "Pendant le repas",
    "Entre deux plats, une table qui joue ensemble est une table qui se détend. Ces trois jeux se lancent depuis la table elle-même."))
parts.append(jeu(3, "Qui de nous deux ?",
    "Un témoin lit une question. Les invités répondent chacun de leur côté, puis les mariés révèlent la bonne réponse.",
    ["Chaque invité coche sa réponse sur sa feuille, sans la montrer.",
     "Les mariés répondent en même temps, avec une ardoise ou en levant la main.",
     "Un point par bonne réponse, à reporter sur le tableau des scores."],
    duo([
        "Qui a dit « je t'aime » en premier ?",
        "Qui est toujours en retard ?",
        "Qui cuisine le mieux ?",
        "Qui pleure devant un film ?",
        "Qui perd ses clés le plus souvent ?",
        "Qui a le dernier mot quand on n'est pas d'accord ?",
        "Qui danse le mieux ?",
        "Qui est le plus organisé ?",
        "Qui chante le plus faux sous la douche ?",
        "Qui dort le plus longtemps le dimanche ?",
        "Qui a choisi le lieu du mariage ?",
        "Qui a demandé l'autre en mariage ?"]), duree="10 minutes entre deux plats"))
parts.append(jeu(4, "Le quiz des mariés",
    "Les mariés préparent à l'avance dix questions sur leur histoire, avec trois réponses possibles. Chaque table joue en équipe.",
    ["Un témoin lit la question et les trois propositions (A, B ou C).",
     "Chaque table s'accorde sur une réponse et la note sur un papier.",
     "La table qui a le plus de bonnes réponses gagne : elle est servie la première au dessert, par exemple."],
    liste_lignes([
        "Où et comment nous sommes-nous rencontrés ?",
        "Quel a été notre premier voyage ensemble ?",
        "Quel a été notre premier plat cuisiné à deux ?",
        "Quelle est la chanson qui nous rappelle le début de notre histoire ?",
        "Qui a fait le premier pas ?",
        "Quelle est la plus grosse bêtise que nous avons faite ensemble ?",
        "Quel est le surnom que nous nous donnons ?",
        "Quelle est la ville où nous avons failli nous perdre ?",
        "Que s'est-il passé le jour de la demande ?",
        "Quel est notre projet le plus fou ?",
    ], hint="bonne réponse, puis deux fausses propositions"), duree="15 minutes"))
parts.append(jeu(5, "Les mots interdits",
    "Pendant tout le repas, certains mots sont interdits à table. Celui qui en prononce un donne un jeton, et la table avec le moins de jetons gagne.",
    ["Choisissez cinq mots, faciles à prononcer par inadvertance.",
     "Posez un petit bol et des jetons (bonbons, petits cailloux) à chaque table.",
     "Quelqu'un de chaque table tient le compte, discrètement."],
    fields(["Mot interdit 1", "Mot interdit 2", "Mot interdit 3", "Mot interdit 4", "Mot interdit 5"], inline=True) +
    p("Idées de mots : « mariage », « félicitations », « alliance », « robe », « oui ». Le plus drôle reste de choisir des mots de l'histoire du couple."),
    duree="Tout le repas"))
parts.append('<div class="scores">' + block("Le tableau des scores",
    p("À remplir au fil des jeux. La table gagnante est celle qui a le plus de points au dessert.") +
    grid(["Jeu 3", "Jeu 4", "Jeu 5", "Total"], 8, premier="Table")) + '</div>')

# 04 ---------------------------------------------------------------------------
parts.append(chapter("04", "Avec vos témoins",
    "Quand l'ambiance est installée, vos témoins peuvent lancer des moments plus théâtraux. Ces trois jeux conviennent à des proches à l'aise pour parler devant tout le monde."))
parts.append(jeu(6, "Le grand mime",
    "Une table contre une autre : un joueur tire un mot et le fait deviner à son équipe, sans parler.",
    ["Découpez les quarante mots ci-dessous (ou lisez-les à voix basse au joueur).",
     "Une minute par joueur. Un point par mot trouvé.",
     "Les témoins arbitrent et tiennent le score."],
    '<div class="mots">' +
    "".join(f"<span>{e(m)}</span>" for m in [
        "Lancer le bouquet", "Couper le gâteau", "Dire oui", "Perdre les alliances", "Danser un slow",
        "Faire un discours trop long", "Chercher sa table", "Faire la queue au buffet", "Poser pour la photo de groupe",
        "Arriver en retard à la cérémonie", "Marcher avec des talons trop hauts", "Essuyer une larme discrète",
        "La belle-mère émue", "Le cousin qui danse trop", "Le témoin qui oublie son discours", "Le petit qui court partout",
        "Un talon coincé dans l'herbe", "Le toast qui n'en finit pas", "Le premier baiser", "L'ouverture de bal",
        "Un fou rire à table", "Chercher ses chaussures à la fin", "Le photographe qui demande de sourire",
        "Une demande en mariage", "Un enterrement de vie de garçon", "Un enterrement de vie de jeune fille",
        "Le lancer de riz", "La jarretière", "Un voyage de noces", "Écrire les cartons de table",
        "Choisir la robe", "Essayer le costume", "Porter la mariée", "Un selfie à vingt",
        "Un invité qui s'endort à table", "La danse du canard", "Un câlin de famille", "Une chorégraphie improvisée",
        "Un discours en pleurs", "Le dernier slow"]) + "</div>", duree="20 minutes"))
parts.append(jeu(7, "Le discours en trois mots",
    "Chaque invité écrit trois mots pour décrire les mariés. Un témoin pioche et lit les plus drôles ou les plus touchants.",
    ["Distribuez les cartes au début du repas et récupérez-les dans un panier.",
     "Le témoin lit une dizaine de cartes, sans nommer leurs auteurs.",
     "Les mariés devinent qui a écrit quoi, ou se contentent d'en rire."],
    cartes(["Trois mots pour décrire les mariés", "Trois mots pour décrire leur histoire", "Trois mots pour leur vie à venir"]), duree="10 minutes"))
parts.append(jeu(8, "Le portrait chinois des mariés",
    "Les invités complètent « Si elle ou il était… » pour chacun des mariés. Les témoins comparent avec les vraies réponses.",
    ["Un témoin lit chaque ligne à voix haute, puis révèle la réponse des mariés.",
     "Plus la réponse est surprenante, plus le moment est drôle."],
    liste_lignes([
        "Si l'un de nous était un animal",
        "Si l'un de nous était un plat",
        "Si l'un de nous était une chanson",
        "Si l'un de nous était un pays",
        "Si l'un de nous était un film",
        "Si l'un de nous était un super-pouvoir",
        "Si l'un de nous était un objet de la cuisine",
        "Si l'un de nous était un métier",
        "Si l'un de nous était une saison",
        "Si l'un de nous était une destination de voyage",
    ], hint="réponse des mariés"), duree="10 minutes"))

# 05 ---------------------------------------------------------------------------
parts.append(chapter("05", "Pour les enfants",
    "Les enfants s'ennuient vite à table. Ces deux jeux leur donnent un rôle et les occupent sans qu'un adulte ait besoin d'intervenir."))
parts.append(jeu(9, "Les missions des petits invités",
    "Une feuille de huit missions à réaliser pendant la journée. Une petite récompense attend celui qui les a toutes cochées.",
    ["Remettez la feuille à chaque enfant dès son arrivée.",
     "Les missions se font à son rythme, pendant le cocktail et le repas."],
    checks([
        "Compter les bougies de ma table",
        "Dire bonjour à cinq invités que je ne connais pas",
        "Repérer le gâteau sans y toucher",
        "Poser pour une photo avec les mariés",
        "Trouver quelque chose de bleu dans la salle",
        "Demander un conseil de mariage à un adulte",
        "Dessiner les mariés",
        "Danser une chanson entière avec un adulte"]), duree="Toute la journée"))
parts.append(jeu(10, "Mon carnet de petit invité",
    "Une page à remplir pour garder le souvenir de la journée, avec un dessin des mariés.",
    ["Prévoyez des crayons de couleur sur chaque table d'enfants.",
     "Les enfants peuvent remplir la page seuls ou avec l'aide d'un adulte."],
    fields(["Mon prénom", "Mon âge", "Ce que portent les mariés aujourd'hui", "Mon plat préféré du repas", "Ce que j'ai préféré aujourd'hui"]) +
    '<div class="drawbox"><span>Le dessin des mariés</span></div>', duree="Pendant le repas"))

# 06 ---------------------------------------------------------------------------
parts.append(chapter("06", "En fin de soirée",
    "Quand les corps sont fatigués mais que personne ne veut partir, ces deux moments laissent un joli souvenir."))
parts.append(jeu(11, "Le vote des tables",
    "Chaque table remplit un bulletin pour désigner ses coups de cœur de la soirée. Les résultats sont lus par un témoin avant la fin de la fête.",
    ["Un bulletin par table, posé au centre en début de soirée.",
     "Un témoin récupère les bulletins et fait le décompte.",
     "Annoncez les résultats avant la dernière heure, pour que chacun puisse en profiter."],
    liste_lignes([
        "La table avec la meilleure ambiance",
        "Le meilleur danseur ou la meilleure danseuse",
        "La plus belle tenue",
        "Le meilleur fou rire de la soirée",
        "L'invité le plus venu de loin",
    ], hint="je vote pour"), duree="Toute la soirée"))
parts.append(jeu(12, "Le bocal des souvenirs",
    "Chaque invité écrit un message aux mariés, glissé dans un bocal. Il se lit un an plus tard, ou le soir du premier anniversaire.",
    ["Posez un bocal à l'entrée de la salle, avec des cartes et des stylos.",
     "Choisissez la personne qui le gardera jusqu'au bon moment."],
    cartes(["Un souvenir avec les mariés", "Un conseil pour la vie à deux", "Un vœu pour l'année qui vient"]), duree="Toute la soirée"))

parts.append('</main>')
parts.append(f'''<footer class="end">
<div class="fl tl">{FLORAL}</div>
{lockup("on-dark")}
{SPRIG}
<p class="merci">Que la fête soit belle.</p>
<p>Ce livret est gratuit et offert par Richard DJ Event. Il rassemble des idées simples pour animer votre mariage entre proches : adaptez-les librement à votre célébration.</p>
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
    return (f'<nav class="toc" aria-label="Sommaire"><p class="kicker">Sommaire</p><h2>Au fil du livret</h2>{SPRIG}'
            f'<ol>{items}</ol>'
            '<aside class="mode"><b>Mode d’emploi</b><span>Ce livret se remplit directement à l’écran : cochez les cases '
            'et écrivez dans les lignes depuis votre ordinateur ou votre téléphone (Adobe Acrobat Reader, Aperçu sur Mac, '
            'Fichiers sur iPhone), puis enregistrez. Vous préférez le papier ? Il s’imprime en A4. '
            'Touchez un chapitre du sommaire pour y aller directement.</span></aside></nav>')

def page(variant, css_extra):
    body = fr_html("".join(parts).replace("__TOC__", toc(variant)))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Livret de jeux de mariage | Richard DJ Event</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<style>{CSS}{css_extra}</style></head><body>{body}</body></html>'''

(HERE / "livret.html").write_text(page("a4", ""), encoding="utf-8")
(HERE / "livret-mobile.html").write_text(page("mobile", MOBILE_PRINT), encoding="utf-8")
print("livret.html + livret-mobile.html générés", "(numéros de page :", "oui)" if PAGES else "non)")
