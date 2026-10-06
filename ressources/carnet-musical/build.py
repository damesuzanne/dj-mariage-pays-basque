#!/usr/bin/env python3
"""Génère carnet.html (A4) et carnet-mobile.html du carnet musical du mariage."""
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


def fin_tools():
    """Bloc de boutons en fin de PDF : autres versions, version en ligne, envoi à Richard."""
    import urllib.parse as _u
    mail = ("mailto:richarddjevent@gmail.com?subject=" + _u.quote("Notre carnet musical de mariage") + "&body=" +
            _u.quote("Bonjour Richard,\n\nVoici notre carnet musical de mariage, rempli. Je joins le PDF enregistré.\n\nMerci !\n"))
    b = [('PDF A4 à imprimer', 'https://drive.google.com/file/d/1-ajvM4mjD7aQBfl61LHGzb8mbR0yoOyN/view'),
         ('PDF pour téléphone', 'https://drive.google.com/file/d/1RQsN9-3FGWd9LHkSmsq58FwlECIuGA4_/view'),
         ('Remplir en ligne', 'https://djmariagepaysbasque.fr/ressources/carnet-musical-mariage/'),
         ('Envoyer à Richard par e-mail', mail)]
    return ('<section class="fin-tools"><p>Pour que vos réponses restent dans ce PDF, enregistrez le fichier avec « Enregistrer » dans Adobe Acrobat Reader, Aperçu ou Fichiers. '
            'La version en ligne les enregistre toute seule sur votre appareil. Rien n’est envoyé à Richard tant que vous n’utilisez pas le bouton d’envoi, '
            'qui ouvre votre messagerie : joignez-y votre PDF enregistré.</p><div class="pdf-tools">'
            + ''.join(f'<a href="{u}">{t}</a>' for t, u in b) + '</div></section>')

# --- contenu ----------------------------------------------------------------
# Le carnet musical du mariage : questionnaire, morceaux par moment, ouverture de bal, listes à passer / à ne pas passer.

def duo2(items, a="On adore", b="À éviter"):
    """Une ligne par style, deux cases : on adore / à éviter."""
    return '<ul class="checks duos">' + "".join(
        f'<li><span>{e(q)}</span><span class="duo"><i></i><em>{e(a)}</em><i></i><em>{e(b)}</em></span></li>' for q in items) + "</ul>"

def lignes_morceaux(labels, hint="titre, artiste"):
    """Lignes d'écriture hautes, pour noter à la main titres et artistes."""
    return '<div class="songfields">' + fields(labels, hint=hint) + '</div>'

def page_lignes(titre, n):
    """Une page entière de lignes d'écriture pour une réponse libre."""
    lignes = "".join(f'<label><b>Ligne {i}</b><span class="line"></span></label>' for i in range(1, n + 1))
    return f'<section class="block pleine"><h3>{e(titre)}</h3><div class="fields">{lignes}</div></section>'

def puces(items):
    return '<ul class="regles">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"

def morceaux(titre, intro, titres, lignes_libres):
    """Un moment de la journée : morceaux classiques à cocher + lignes pour les vôtres."""
    return block(titre, p(intro) + '<div class="songs">' + checks(titres) + '</div>' +
                 '<p class="vos">Vos morceaux à ajouter</p>' + lignes_morceaux(lignes_libres))

def grid(entetes, n, premier="N°", lignes=None, cls=""):
    th = "".join(f"<th>{e(h)}</th>" for h in entetes)
    rows = ""
    for i in range(1, n + 1):
        lab = lignes[i - 1] if lignes else str(i)
        rows += f'<tr><td class="n{" lab" if lignes else ""}">{e(lab)}</td>' + "".join(
            f'<td data-l="{e(h)}"><span class="cl"></span></td>' for h in entetes) + "</tr>"
    return f'<table class="grid keep {cls}"><thead><tr><th>{e(premier)}</th>{th}</tr></thead><tbody>{rows}</tbody></table>'

import urllib.parse as _up
MAIL = ("mailto:richarddjevent@gmail.com?subject=" + _up.quote("Notre carnet musical de mariage") + "&body=" +
        _up.quote("Bonjour Richard,\n\nVoici notre carnet musical pour notre mariage du [date] à [lieu]. Je joins le PDF rempli.\n\nMerci !\n"))

def bouton_mail():
    return ('<div class="envoi"><a class="btn-mail" href="' + MAIL + '">Envoyer mon carnet à Richard par e-mail</a>'
            '<p>Le message s\'ouvre dans votre messagerie, adresse et objet déjà remplis. Enregistrez d\'abord votre PDF rempli, puis joignez-le au message.</p></div>')

parts = []

parts.append(f'''<section class="cover dark">
{lockup("on-dark")}
<p class="kicker">Carnet gratuit</p>
<h1>Le carnet musical<br><em>du mariage</em></h1>
{SPRIG}
<p class="sub">Le questionnaire, l'ouverture de bal et vos listes</p>
<p class="lead">Un carnet à remplir à deux pour préparer la musique de votre journée : ce que vous aimez, ce que vous voulez entendre, et ce qui ne doit jamais passer.</p>
</section>''')

parts.append('__TOC__')
parts.append('<main>')

# 01 ---------------------------------------------------------------------------
parts.append(chapter("01", "Avant de commencer",
    "La musique d'un mariage se prépare à deux, en quelques soirées. Ce carnet vous guide, du premier questionnaire jusqu'à la liste à remettre à votre DJ."))
parts.append(block("Votre mariage en deux lignes", fields([
    "Nos prénoms", "Date du mariage", "Lieu de la réception", "Nombre d'invités à la soirée"], ) ).replace('class="block', 'class="block compact', 1))
parts.append(block("Comment remplir ce carnet", puces([
    "Remplissez le questionnaire chacun de votre côté, puis comparez vos réponses.",
    "Choisissez votre ouverture de bal en dernier, quand vous aurez une idée de l'ambiance voulue.",
    "Notez les morceaux à passer absolument et ceux à ne jamais passer.",
    "Envoyez le tout à votre DJ plusieurs semaines avant la date, pour qu'il puisse poser des questions."])))

# 02 ---------------------------------------------------------------------------
parts.append(chapter("02", "Le questionnaire musical",
    "Quelques questions à remplir chacun de votre côté. Vos réponses donneront le ton de toute la journée."))
parts.append(block("Vos goûts, côte à côte",
    grid(["Prénom 1", "Prénom 2"], 8, premier="Question", cls="eq", lignes=[
        "",
        "Le style qu'on écoute le plus",
        "Un artiste qu'on adore",
        "La chanson de nos débuts",
        "Le morceau qui nous donne envie de danser",
        "Un morceau qui nous rappelle un voyage ou un concert",
        "Le morceau qu'on ne supporte plus",
        "Une chanson de notre enfance"])))
parts.append(block("Vos invités", checks([
    "Beaucoup d'enfants et d'adolescents",
    "Beaucoup d'invités de 25 à 40 ans",
    "Beaucoup d'invités de 40 à 60 ans",
    "Beaucoup d'invités de plus de 60 ans",
    "Des invités étrangers, avec des musiques de leur pays à prévoir"])))
parts.append(block("Les styles de musique",
    p("Pour chaque style, cochez « On adore » ou « À éviter ». Laissez vide si cela vous est égal.") +
    duo2(["Chanson française", "Pop internationale", "Rock", "Disco et funk", "Années 80", "Années 90", "Années 2000",
          "Hits d'aujourd'hui", "Rock'n'roll et twist", "Soul et R&B", "Hip-hop", "Musiques latines",
          "Musiques basques", "Électro et house", "Slows"])))
parts.append(block("Votre façon de faire",
    p("Choisissez ce qui vous correspond le mieux.") + checks([
        "On préfère laisser le DJ lire la salle et adapter les morceaux.",
        "On veut une liste de morceaux précis à respecter.",
        "On veut un mélange : quelques morceaux imposés, le reste au feeling du DJ."])))
parts.append(page_lignes("Ce qui compte le plus pour nous dans la musique, ce jour-là", 21))

# 03 ---------------------------------------------------------------------------
parts.append(chapter("03", "L'ouverture de bal",
    "C'est le premier moment dansé de la soirée. Elle se prépare un peu à l'avance, mais elle n'a pas besoin d'être parfaite."))
parts.append(block("Votre choix", lignes_morceaux([
    "Idée 1", "Idée 2", "Idée 3", "Notre choix final"]) + fields(["Une chanson entière, ou seulement le début ?"]) +
    checks(["On ouvre le bal après le gâteau.", "On décide avec notre DJ.",
            "Nos proches nous rejoignent pendant la chanson."])))

# 05 ---------------------------------------------------------------------------
parts.append(chapter("04", "À passer, à ne jamais passer",
    "Deux listes courtes, mais précieuses pour votre DJ : ce qui doit absolument passer, et ce qui doit rester dehors."))
parts.append(block("Les morceaux à passer absolument", lignes_morceaux([
    "Morceau 1", "Morceau 2", "Morceau 3", "Morceau 4", "Morceau 5"])).replace('class="block', 'class="block keepp', 1))
parts.append(block("Les morceaux à ne jamais passer", lignes_morceaux([
    "Morceau 1", "Morceau 2", "Morceau 3", "Morceau 4", "Morceau 5"])).replace('class="block', 'class="block keepp', 1))


# 05 ---------------------------------------------------------------------------
parts.append(chapter("05", "Envoyer votre carnet à Richard",
    "Quand votre carnet est rempli, envoyez-le à Richard, bien avant la date, pour qu'il puisse vous poser ses questions."))
parts.append(block("Envoyer votre carnet à Richard", bouton_mail()))

parts.append(fin_tools())
parts.append('</main>')
parts.append(f'''<footer class="end">
{lockup("on-dark")}
{SPRIG}
<p class="merci">Que la musique soit belle.</p>
<p>Ce carnet est gratuit et offert par Richard DJ Event.</p>
<p class="cta">Parlons de la musique de votre mariage</p>
<p><a href="tel:+33684331824">06 84 33 18 24</a> · <a href="mailto:richarddjevent@gmail.com">richarddjevent@gmail.com</a></p>
<p class="sites">djmariagepaysbasque.fr<br>djmariagelandes.fr</p>
</footer>''')

CSS = (HERE / "style.css").read_text()
MOBILE_PRINT = (HERE / "mobile-print.css").read_text()
PAGES = json.loads((HERE / "pages.json").read_text()) if (HERE / "pages.json").exists() else {}


def pdf_tools():
    """Boutons cliquables du sommaire : l'autre version du PDF et la version en ligne."""
    b = [('PDF A4 à imprimer', 'https://drive.google.com/file/d/1-ajvM4mjD7aQBfl61LHGzb8mbR0yoOyN/view'),
         ('PDF pour téléphone', 'https://drive.google.com/file/d/1RQsN9-3FGWd9LHkSmsq58FwlECIuGA4_/view'),
         ('Remplir en ligne', 'https://djmariagepaysbasque.fr/ressources/carnet-musical-mariage/')]
    b.append(('Envoyer à Richard par e-mail', MAIL))
    return '<div class="pdf-tools">' + ''.join(f'<a href="{u}">{t}</a>' for t, u in b) + '</div>'

def toc(variant):
    nums = PAGES.get(variant, {})
    items = "".join(
        f'<li><a href="#c{n}"><span class="tn">{n}</span><span class="tt">{e(t)}</span>'
        f'<span class="tl"></span><span class="tp">{nums.get(n, "")}</span></a></li>' for n, t in CHAPTERS)
    return (f'<nav class="toc" aria-label="Sommaire"><p class="kicker">Sommaire</p><h2>Au fil du carnet</h2>{SPRIG}'
            f'<ol>{items}</ol>'
            '<aside class="mode"><b>Mode d’emploi</b><span>Ce carnet se remplit directement à l’écran : cochez les cases '
            'et écrivez dans les lignes depuis votre ordinateur ou votre téléphone (Adobe Acrobat Reader, Aperçu sur Mac, '
            'Fichiers sur iPhone), puis choisissez « Enregistrer » pour que vos réponses restent dans le fichier (dans un navigateur ou l’aperçu d’une messagerie, elles ne sont pas gardées). '
            'Plus simple : la <a href="https://djmariagepaysbasque.fr/ressources/carnet-musical-mariage/">version en ligne</a> enregistre toute seule. Vous préférez le papier ? Il s’imprime en A4. '
            'Touchez un chapitre du sommaire pour y aller directement.</span></aside>' + pdf_tools() + '</nav>')

def page(variant, css_extra):
    body = fr_html("".join(parts).replace("__TOC__", toc(variant)))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Le carnet musical du mariage | Richard DJ Event</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<style>{CSS}{css_extra}</style></head><body>{body}</body></html>'''

(HERE / "carnet.html").write_text(page("a4", ""), encoding="utf-8")
(HERE / "carnet-mobile.html").write_text(page("mobile", MOBILE_PRINT), encoding="utf-8")
print("carnet.html + carnet-mobile.html générés", "(numéros de page :", "oui)" if PAGES else "non)")
