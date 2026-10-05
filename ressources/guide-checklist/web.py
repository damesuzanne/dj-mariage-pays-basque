#!/usr/bin/env python3
"""Version web de la checklist (enregistrement automatique). Lancer après make.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import web_commun
H = pathlib.Path(__file__).resolve().parent
web_commun.convert(H / "guide.html", "checklist-retroplanning-mariage", "richard-checklist-retroplanning-v1",
                   "Checklist et rétroplanning du mariage", "1Uy8_UoHeBf75mBlUfic7MMC2U4LdF2kF",
                   "1bF02mEdGind82uVcvl-0_NcGZgz6Zs3T", "ma-checklist-mariage")
