#!/usr/bin/env python3
"""Génère annuaire.html (A4) et annuaire-mobile.html de l'annuaire des lieux de mariage au Pays Basque.

Données : content.json (chapitres) et venues.json (fiches des lieux, sources officielles),
photos/ (photos des sites officiels, crédits dans photos/credits.json).
Les PDF sont fabriqués par make.py (Chrome + champs remplissables PyMuPDF).
"""
import html, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
CONTENT = json.loads((HERE / "content.json").read_text())
CREDITS = json.loads((HERE / "photos/credits.json").read_text())
PAGES = json.loads((HERE / "pages.json").read_text()) if (HERE / "pages.json").exists() else {}

COTE = {1, 2, 3, 12, 13, 14}
ZONES = {True: "La côte et ses environs", False: "Les domaines et les villages"}
SITE_TEL, SITE_TEL_HREF, SITE_MAIL = "06 84 33 18 24", "+33684331824", "richarddjevent@gmail.com"


def fr_html(h):
    """Espaces insécables avant : ; ! ? » et après « (jamais un signe seul en début de ligne)."""
    def corr(t):
        t = re.sub(r" ([:;!?»])", " \\1", t)
        return t.replace("« ", "« ")
    return "".join(m if m.startswith("<") else corr(m) for m in re.split(r"(<[^>]*>)", h))


def e(t):
    return html.escape(t, quote=False)


def a(t):
    return html.escape(t, quote=True)


SPRIG = '''<svg class="sprig" viewBox="0 0 220 24" aria-hidden="true"><path d="M2 12 H98 M122 12 H218" stroke="#c6a15b" stroke-width="1" fill="none"/>
<g transform="translate(110 12)"><circle r="3.2" fill="#fff" stroke="#c6a15b" stroke-width=".8"/>
<g fill="#9fb09a"><ellipse cx="-12" cy="-1" rx="6" ry="2.4" transform="rotate(-20 -12 -1)"/><ellipse cx="12" cy="-1" rx="6" ry="2.4" transform="rotate(20 12 -1)"/></g></g></svg>'''

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


# --- composants -------------------------------------------------------------
def checks(items):
    return '<ul class="checks">' + "".join(f"<li><i></i><span>{e(x)}</span></li>" for x in items) + "</ul>"


def fields(labels, cls=""):
    return f'<div class="fields {cls}">' + "".join(
        f'<label><b>{e(l)}</b><span class="line"></span></label>' for l in labels) + "</div>"


def table(cols, rows, first="", cls=""):
    th = (f"<th>{e(first)}</th>" if first is not None else "") + "".join(f"<th>{e(c)}</th>" for c in cols)
    body = "".join(
        f'<tr><td class="crit">{e(r)}</td>' + "".join(f'<td data-l="{a(c)}"><span class="cl"></span></td>' for c in cols) + "</tr>"
        for r in rows)
    return f'<table class="grid {cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def chapter_head(num, title, intro):
    label = num if num.isdigit() and len(num) == 2 else ""
    n = f'<span class="num">{label}</span>' if label else ""
    return (f'<header class="chapter" id="c{num}">{n}<h2>{e(title)}</h2>{SPRIG}'
            + (f'<p class="intro">{e(intro)}</p>' if intro else "") + "</header>")


def page_of(cid, variant):
    return PAGES.get(variant, {}).get(cid, "")


def overview(variant):
    venues = [it[1] for ch in CONTENT if ch["kind"] == "venue" for it in ch["items"]]
    out = ""
    for cote in (True, False):
        rows = ""
        for i, v in enumerate(venues, 1):
            if (i in COTE) != cote:
                continue
            rows += (f'<tr><td class="vn">{i:02d}</td><td><a href="#cL{i:02d}"><b>{e(v["name"])}</b></a>'
                     f'<span>{e(v["style"])}</span></td><td class="vt">{e(v["town"])}</td>'
                     f'<td class="vp">{page_of(f"L{i:02d}", variant)}</td></tr>')
        out += (f'<section class="block zone"><h3>{e(ZONES[cote])}</h3>'
                f'<table class="ov"><thead><tr><th></th><th>Lieu</th><th>Commune</th><th>Page</th></tr></thead>'
                f'<tbody>{rows}</tbody></table></section>')
    return out


def venue(i, v):
    photo = HERE / f"photos/{i:02d}.jpg"
    from PIL import Image
    w = Image.open(photo).size[0]
    small = w < 1000
    credit = CREDITS.get(v["name"], {})
    cap = credit.get("caption", "")
    quote = (f'<blockquote><p>{e(v["quote"])}</p><a href="{a(v["quote_source"])}">Lire sur le site officiel ↗</a></blockquote>'
             if v.get("quote") else "")
    fig = (f'<figure class="v-photo{" small" if small else ""}"><img src="photos/{i:02d}.jpg" alt="{a(v["name"])}, {a(v["town"])}">'
           f'<figcaption>{e(cap)}</figcaption></figure>')
    top = f'<div class="v-top">{fig}{quote}</div>' if small else fig + quote
    tel = v["phone"]
    tel_html = e(tel) if not re.search(r"\d", tel) else " / ".join(
        f'<a href="tel:+33{re.sub(r"[^0-9]", "", t)[1:]}">{e(t.strip())}</a>' for t in tel.split("/"))
    site_label = re.sub(r"^https?://(www\.)?", "", v["site"]).split("/")[0]
    card = (f'<aside class="v-card"><p class="v-card-t">Coordonnées</p><dl>'
            f'<dt>Adresse</dt><dd>{e(v["address"])}</dd>'
            f'<dt>Téléphone</dt><dd>{tel_html}</dd>'
            f'<dt>E-mail</dt><dd><a href="mailto:{a(v["email"])}">{e(v["email"])}</a></dd>'
            f'<dt>Site internet</dt><dd><a href="{a(v["site"])}">{e(site_label)} ↗</a></dd></dl></aside>')
    sources = " · ".join(f'<a href="{a(u)}">{e(l)}</a>' for l, u in v.get("sources", []))
    body = (f'<div class="v-body"><div class="v-text"><p class="v-sum">{e(v["summary"])}</p>'
            f'<aside class="tip"><b>À faire préciser</b><span>{e(v["focus"])}</span></aside></div>{card}</div>')
    visit = (f'<section class="block v-visit"><h3>Pendant votre visite</h3>{checks(v["questions"])}'
             f'{fields(["Notre impression", "Prochaine action / date"], "inline")}</section>')
    src = f'<p class="v-src">Sources : {sources}</p>' if sources else ""
    zone = ZONES[i in COTE]
    return (f'<article class="venue" id="cL{i:02d}"><header class="v-head"><span class="num">Annuaire · {i:02d} · {e(zone)}</span>'
            f'<h2>{e(v["name"])}</h2><p class="v-meta">{e(v["town"])} <span>·</span> {e(v["style"])}</p></header>'
            f'{top}{body}{visit}{src}</article>')


def items(ch, variant):
    out = ""
    for kind, data in ch["items"]:
        if kind == "fields":
            out += f'<section class="block">{fields(data, "inline" if len(data) > 2 else "")}</section>'
        elif kind == "h":
            out += f'<h3 class="sub-h">{e(data)}</h3>'
        elif kind == "checks":
            out += f'<section class="block">{checks(data)}</section>'
        elif kind == "p":
            out += f'<p class="para">{e(data)}</p>'
        elif kind == "note":
            out += f'<aside class="note">{e(data)}</aside>'
        elif kind == "questions":
            title, qs = data
            out += f'<section class="block"><h3>{e(title)}</h3>{checks(qs)}</section>'
        elif kind == "compare":
            out += table(["Lieu 1", "Lieu 2", "Lieu 3"], data, "Critère", "compare")
        elif kind == "budget":
            out += table(["Montant TTC", "Inclus / à confirmer"], data, "Poste", "budget")
        elif kind == "payments":
            out += table(["Prestataire / objet", "Montant", "Échéance", "Versé le"], data, "", "pay")
        elif kind == "contact":
            out += (f'<div class="contact-card">{lockup("on-dark")}<p><a href="tel:{SITE_TEL_HREF}">{SITE_TEL}</a><br>'
                    f'<a href="mailto:{SITE_MAIL}">{SITE_MAIL}</a></p><p class="sites"><a href="https://djmariagepaysbasque.fr/">djmariagepaysbasque.fr</a> · '
                    '<a href="https://djmariagelandes.fr/">djmariagelandes.fr</a></p></div>')
    return out


def special(ch, variant):
    """Mises en forme dédiées : chapitre 02 en tableau d'ensemble, message à adapter en lettre."""
    if ch["num"] == "02":
        intro_p = ch["items"][0][1]
        note = [d for k, d in ch["items"] if k == "note"][0]
        conseil = ch["items"][-2][1]
        return f'<p class="para">{e(intro_p)}</p>{overview(variant)}<p class="para">{e(conseil)}</p><aside class="note">{e(note)}</aside>'
    if ch["num"] == "08":
        out = ""
        for kind, data in ch["items"]:
            if kind == "p":
                out += f'<blockquote class="letter">{e(data)}</blockquote>'
            elif kind == "h":
                out += f'<h3 class="sub-h">{e(data)}</h3>'
            elif kind == "checks":
                out += f'<section class="block">{checks(data)}</section>'
            elif kind == "fields":
                out += f'<section class="block">{fields(data)}</section>'
        return out
    return None


# Sommaire : chapitres principaux (les suites sont regroupées)
TOC = [("01", "c01", "Choisir ce qui vous ressemble"), ("02", "c02", "Votre annuaire : 14 lieux"),
       ("03", "c03", "Les questions à poser"), ("04", "c04", "La checklist de la visite"),
       ("05", "c051", "Vos trois fiches de visite"), ("06", "c06", "Comparer vos trois favoris"),
       ("07", "c07", "Le budget et les règlements"), ("08", "c08", "Après la visite"),
       ("09", "c09", "Et pour la musique ?")]


def toc(variant):
    lis = "".join(
        f'<li><a href="#{cid}"><span class="tn">{n}</span><span class="tt">{e(t)}</span><span class="tl"></span>'
        f'<span class="tp">{page_of(cid[1:], variant)}</span></a></li>' for n, cid, t in TOC)
    return (f'<nav class="toc" aria-label="Sommaire"><p class="kicker">Votre carnet</p><h2>Sommaire</h2>{SPRIG}<ol>{lis}</ol>'
            '<aside class="mode"><b>Mode d’emploi</b><span>Ce carnet se remplit à l’écran : cochez les cases et écrivez '
            'dans les lignes depuis votre ordinateur ou votre téléphone (Adobe Acrobat Reader, Aperçu sur Mac, Fichiers sur iPhone), '
            'puis enregistrez. Il s’imprime aussi en A4. Touchez un titre du sommaire ou un lieu de l’annuaire pour y aller directement.</span></aside></nav>')


def cover():
    return f'''<section class="cover">
<figure class="cover-photo"><img src="photos/ambiance.jpg" alt="Tables de réception de mariage dressées sous des guirlandes lumineuses"></figure>
<div class="cover-text">
<div class="fl br">{FLORAL}</div>
<p class="kicker">Guide gratuit · Édition octobre 2026</p>
<h1>Votre lieu de mariage<br><em>au Pays Basque</em></h1>
{SPRIG}
<p class="sub">L’annuaire &amp; le carnet de vos visites</p>
<p class="lead">14 adresses de la côte aux collines, les questions à poser, la checklist de visite, le comparatif de vos favoris et la fiche budget.</p>
{lockup("on-light small")}
</div>
<p class="cover-cap">Photographie d’ambiance, hors annuaire</p>
</section>'''


def end():
    return f'''<footer class="end">
<div class="fl tl">{FLORAL}</div>
{lockup("on-dark")}
{SPRIG}
<p class="merci">Un lieu qui vous ressemble,<br>une fête qui vous rassemble.</p>
<p>Annuaire gratuit offert par Richard DJ Event. Les informations proviennent des sites officiels des lieux (octobre 2026) : confirmez toujours disponibilités, tarifs et conditions directement auprès de chaque lieu.</p>
<p class="cta">Parlons de votre mariage</p>
<p><a href="tel:{SITE_TEL_HREF}">{SITE_TEL}</a> · <a href="mailto:{SITE_MAIL}">{SITE_MAIL}</a></p>
<p class="sites">djmariagepaysbasque.fr<br>djmariagelandes.fr</p>
</footer>'''


def document(variant):
    parts = [cover(), toc(variant), "<main>"]
    vi = 0
    for ch in CONTENT:
        if ch["kind"] == "venue":
            vi += 1
            parts.append(venue(vi, ch["items"][0][1]))
            continue
        cls = "chap" + (" cont" if not (ch["num"].isdigit() and len(ch["num"]) == 2) else "")
        body = special(ch, variant)
        if body is None:
            body = items(ch, variant)
        parts.append(f'<section class="{cls}">{chapter_head(ch["num"], ch["title"], ch.get("intro", ""))}{body}</section>')
    parts += ["</main>", end()]
    return fr_html("".join(parts))


CSS = (HERE / "style.css").read_text()
MOBILE = (HERE / "mobile-print.css").read_text()


def page(variant, extra):
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Votre lieu de mariage au Pays Basque | Richard DJ Event</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<style>{CSS}{extra}</style></head><body class="{variant}">{document(variant)}</body></html>'''


# Ordre des chapitres pour la pagination (make.py)
ORDER = []
_vi = 0
for _ch in CONTENT:
    if _ch["kind"] == "venue":
        _vi += 1
        ORDER.append((f"L{_vi:02d}", _ch["items"][0][1]["name"]))
    else:
        ORDER.append((_ch["num"], _ch["title"]))

if __name__ == "__main__":
    (HERE / "annuaire.html").write_text(page("a4", ""), encoding="utf-8")
    (HERE / "annuaire-mobile.html").write_text(page("mobile", MOBILE), encoding="utf-8")
    (HERE / "chapters.json").write_text(json.dumps(ORDER, ensure_ascii=False, indent=1), encoding="utf-8")
    print("annuaire.html + annuaire-mobile.html générés", "(pages : oui)" if PAGES else "(pages : non)")
