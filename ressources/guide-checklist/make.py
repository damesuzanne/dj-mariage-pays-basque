#!/usr/bin/env python3
"""Fabrique les deux PDF du guide (A4 à imprimer + format téléphone), remplissables et navigables.

1. build.py génère guide.html et guide-mobile.html ;
2. Chrome imprime les PDF, on relève la page de chaque chapitre (pages.json),
   on régénère pour inscrire les numéros dans le sommaire, on réimprime ;
3. PyMuPDF pose un champ case à cocher sur chaque case dorée, un champ texte
   sur chaque ligne pointillée dorée, et les signets (panneau latéral du lecteur).

Usage : python3 make.py
"""
import json, pathlib, subprocess, sys
from collections import defaultdict
import fitz

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
GOLD = (0.78, 0.63, 0.36)
NAVY = (16 / 255, 21 / 255, 34 / 255)
VARIANTS = {
    "a4": ("guide.html", "Checklist-retroplanning-mariage-Richard-DJ-Event.pdf"),
    "mobile": ("guide-mobile.html", "Checklist-retroplanning-mariage-Richard-DJ-Event-MOBILE.pdf"),
}


def build():
    subprocess.run(["python3", str(HERE / "build.py")], check=True)


def render(html, pdf):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={HERE / pdf}",
                    f"file://{HERE / html}"], check=True, capture_output=True)


def chapters():
    sys.path.insert(0, str(HERE))
    src = (HERE / "build.py").read_text()
    import re
    return re.findall(r'chapter\("(\d\d)", "([^"]+)"', src)


def chapter_pages(pdf):
    """Page (1-based) de chaque titre de chapitre, en sautant couverture et sommaire."""
    doc = fitz.open(HERE / pdf)
    found = {}
    for num, title in chapters():
        probe = title[:22]
        for i in range(2, len(doc)):
            if doc[i].search_for(probe):
                found[num] = i + 1
                break
    return found


def close(a, b, tol=0.03):
    return a is not None and all(abs(x - y) < tol for x, y in zip(a, b))


def add_fields(pdf):
    doc = fitz.open(HERE / pdf)
    n_box = n_txt = 0
    for pno, page in enumerate(doc):
        dots = defaultdict(list)
        for d in page.get_drawings():
            r = d["rect"]
            # Case à cocher : carré doré ~14 pt, fond crème
            if 12 <= r.width <= 16 and 12 <= r.height <= 16 and close(d.get("color"), GOLD) and d.get("fill"):
                w = fitz.Widget()
                w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
                w.field_name = f"case_p{pno + 1}_{n_box}"
                w.rect = fitz.Rect(r.x0 + 0.5, r.y0 + 0.5, r.x1 - 0.5, r.y1 - 0.5)
                w.border_width = 0
                w.border_color = None
                w.fill_color = None
                w.text_color = NAVY
                w.field_value = False
                page.add_widget(w)
                n_box += 1
            # Point d'une ligne pointillée dorée
            elif r.width < 2.2 and r.height < 2.2 and close(d.get("fill"), GOLD) and d.get("color") is None:
                dots[round(r.y1, 1)].append((r.x0, r.x1))
        for y, xs in dots.items():
            xs.sort()
            segs, start, end = [], xs[0][0], xs[0][1]
            for x0, x1 in xs[1:]:
                if x0 - end > 8:
                    segs.append((start, end)); start = x0
                end = x1
            segs.append((start, end))
            for x0, x1 in segs:
                if x1 - x0 < 40:
                    continue
                w = fitz.Widget()
                w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
                w.field_name = f"ligne_p{pno + 1}_{n_txt}"
                w.rect = fitz.Rect(x0, y - 17, x1, y - 1.5)
                w.text_font = "Helv"
                w.text_fontsize = 0  # taille auto : le texte reste dans la ligne
                w.text_color = NAVY
                w.border_width = 0
                w.border_color = None
                w.fill_color = None
                page.add_widget(w)
                n_txt += 1
    toc = [[1, "Couverture", 1], [1, "Sommaire", 2]]
    for num, title in chapters():
        p = chapter_pages_cache[pdf].get(num)
        if p:
            toc.append([1, f"{num}. {title}", p])
    toc.append([1, "Contacts Richard DJ Event", len(doc)])
    doc.set_toc(toc)
    doc.set_metadata({"title": "Checklist complète & rétroplanning du mariage", "author": "Richard DJ Event",
                      "subject": "Guide gratuit à remplir, à imprimer ou à consulter sur téléphone",
                      "keywords": "mariage, checklist, rétroplanning, organisation, DJ mariage Pays Basque, Landes"})
    tmp = HERE / ("_" + pdf)
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(HERE / pdf)
    return n_box, n_txt


if __name__ == "__main__":
    if (HERE / "pages.json").exists():
        (HERE / "pages.json").unlink()
    build()
    for html, pdf in VARIANTS.values():
        render(html, pdf)
    pages = {v: chapter_pages(pdf) for v, (_, pdf) in VARIANTS.items()}
    (HERE / "pages.json").write_text(json.dumps(pages, indent=1))
    build()
    for html, pdf in VARIANTS.values():
        render(html, pdf)
    chapter_pages_cache = {pdf: chapter_pages(pdf) for _, pdf in VARIANTS.values()}
    for v, (_, pdf) in VARIANTS.items():
        assert chapter_pages_cache[pdf] == pages[v], f"pagination instable ({v})"
        boxes, lines = add_fields(pdf)
        print(f"{pdf} : {len(fitz.open(HERE / pdf))} pages, {boxes} cases, {lines} lignes, chapitres {pages[v]}")
