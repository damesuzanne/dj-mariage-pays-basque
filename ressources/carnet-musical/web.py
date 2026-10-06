#!/usr/bin/env python3
"""Version web du carnet musical (enregistrement automatique). Lancer après make.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import web_commun
H = pathlib.Path(__file__).resolve().parent
web_commun.convert(H / "carnet.html", "carnet-musical-mariage", "richard-carnet-musical-v1",
                   "Le carnet musical du mariage", "1-ajvM4mjD7aQBfl61LHGzb8mbR0yoOyN",
                   "1RQsN9-3FGWd9LHkSmsq58FwlECIuGA4_", "mon-carnet-musical",
                   mail={"to": "richarddjevent@gmail.com", "subject": "Notre carnet musical de mariage"})
