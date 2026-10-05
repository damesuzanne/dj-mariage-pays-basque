#!/usr/bin/env python3
"""Assemble build.py = socle commun (guide-checklist) + contenu.py (texte du livret).

À lancer après chaque modification de contenu.py, puis `python3 make.py`.
"""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
build = (HERE / "build.py").read_text()
debut = build.index("# --- contenu")
fin = build.index("CSS = (HERE")
contenu = (HERE / "contenu.py").read_text()
(HERE / "build.py").write_text(build[:debut] + contenu + "\n" + build[fin:])
print("build.py ré-assemblé")
