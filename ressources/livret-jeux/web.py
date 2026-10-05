#!/usr/bin/env python3
"""Version web du livret de jeux (enregistrement automatique). Lancer après make.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import web_commun
H = pathlib.Path(__file__).resolve().parent
web_commun.convert(H / "livret.html", "livret-jeux-mariage", "richard-livret-jeux-v1",
                   "Le livret de jeux de mariage", "1W0qTzt-ROu0C9khEqvfJSXpL3b6TvzRW",
                   "1S8_8FPODX6zmxW945hlipmjO-N8r9v9t", "mon-livret-jeux")
