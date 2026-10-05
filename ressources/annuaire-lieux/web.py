#!/usr/bin/env python3
"""Version web de l'annuaire : même mise en page que le PDF, avec cases et lignes qui s'enregistrent
automatiquement sur l'appareil (localStorage). Écrit public/ressources/lieux-mariage-pays-basque/.

Usage : python3 web.py   (après build.py / make.py pour avoir les numéros de page, sans importance ici)
"""
import json, pathlib, re, shutil

import build

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent.parent / "public/ressources/lieux-mariage-pays-basque"
DRIVE = json.loads((HERE / "drive-ids.json").read_text())

fonts = (HERE / "fonts.css").read_text()
# Polices variables : on déclare la plage de graisses pour retrouver les vrais gras.
fonts = re.sub(r"(font-family:'Outfit'[^}]*?)font-weight:400", r"\1font-weight:100 900", fonts)
fonts = re.sub(r"(font-family:'Playfair Display'[^}]*?)font-weight:(400|500)", r"\1font-weight:400 900", fonts)

body = build.document("web")
n = {"i": 0}


def nid():
    n["i"] += 1
    return f"r{n['i']}"


# cases à cocher
body = re.sub(r"<li><i></i><span>(.*?)</span></li>",
              lambda m: f'<li><label><input type="checkbox" id="{nid()}"><i></i><span>{m.group(1)}</span></label></li>', body)
# lignes d'écriture
body = re.sub(r'<label><b>(.*?)</b><span class="line"></span></label>',
              lambda m: f'<label><b>{m.group(1)}</b><span class="writing"><span class="line"></span>'
                        f'<textarea id="{nid()}" rows="1" aria-label="{re.sub("<[^>]+>", "", m.group(1))}"></textarea></span></label>', body)
# cellules des tableaux
body = re.sub(r'<td data-l="([^"]*)"><span class="cl"></span></td>',
              lambda m: f'<td data-l="{m.group(1)}"><span class="cl"></span>'
                        f'<textarea id="{nid()}" class="cell" rows="1" aria-label="{m.group(1)}"></textarea></td>', body)

tools = f'''<div class="screen-tools"><p id="save-status" role="status">Vos réponses s’enregistrent automatiquement sur cet appareil, dans ce navigateur. Elles ne sont pas envoyées à Richard.</p>
<div class="st-actions"><a href="https://drive.google.com/file/d/{DRIVE['a4']}/view" target="_blank" rel="noopener">PDF A4 à imprimer</a>
<a href="https://drive.google.com/file/d/{DRIVE['mobile']}/view" target="_blank" rel="noopener">PDF pour téléphone</a>
<button id="export" type="button">Exporter mes réponses</button></div></div>'''
body = body.replace("<main>", "<main>" + tools, 1)

EXTRA = '''
.screen-tools{margin:18px 0 6px;padding:14px 18px;background:#fff;border:1px solid var(--line);border-radius:14px;font-size:14px;color:var(--muted)}
.st-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.st-actions a,.st-actions button{font:500 13px var(--sans);color:var(--navy);background:transparent;border:1px solid var(--gold);border-radius:30px;padding:8px 14px;text-decoration:none;cursor:pointer}
.st-actions a:hover,.st-actions button:hover{background:var(--cream2)}
.checks label{display:flex;gap:12px;align-items:flex-start;cursor:pointer;width:100%}
.checks input{position:absolute;opacity:0;width:1px;height:1px}
.checks input:checked+i{background:var(--gold);box-shadow:inset 0 0 0 3px var(--cream)}
.checks input:focus-visible+i{outline:2px solid var(--navy);outline-offset:2px}
.checks input:checked~span{color:var(--muted)}
.writing{position:relative;display:block}
.writing textarea,.grid textarea.cell{font:400 16px/1.3 var(--sans);color:var(--navy);background:transparent;border:0;resize:none;overflow:hidden}
.writing textarea{position:absolute;left:0;right:0;top:0;height:30px;padding:3px 2px 6px;outline:0}
.writing textarea:focus,.grid textarea.cell:focus{background:rgba(198,161,91,.1);outline:0}
.grid textarea.cell{position:absolute;left:6px;right:6px;top:3px;bottom:8px;width:calc(100% - 12px);height:calc(100% - 11px);padding:3px 2px}
@media(max-width:640px){.grid textarea.cell{position:static;display:block;width:100%;height:36px;padding:4px 2px 6px}}
@media print{.screen-tools{display:none}.writing textarea,.grid textarea.cell{color:#000}}
'''

JS = '''
(function(){var key='richard-lieux-pays-basque-v3',saved={},fs=[].slice.call(document.querySelectorAll('textarea,input[type=checkbox]')),st=document.getElementById('save-status');
try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
fs.forEach(function(f){if(f.id in saved){if(f.type==='checkbox')f.checked=saved[f.id];else f.value=saved[f.id]}
f.addEventListener('input',function(){saved[f.id]=f.type==='checkbox'?f.checked:f.value;
try{localStorage.setItem(key,JSON.stringify(saved));st.textContent='Enregistré sur cet appareil.'}catch(e){st.textContent='Impossible d’enregistrer ici : utilisez « Exporter mes réponses » pour les garder.'}})});
document.getElementById('export').onclick=function(){var b=new Blob([JSON.stringify(saved,null,2)],{type:'application/json'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='mes-visites-mariage.json';a.click();URL.revokeObjectURL(u)};
})();
'''

html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Votre lieu de mariage au Pays Basque | Richard DJ Event</title>
<style>{fonts}{build.CSS}{EXTRA}</style></head><body class="web">{body}<script>{JS}</script></body></html>'''

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(html, encoding="utf-8")
if (OUT / "photos").exists():
    shutil.rmtree(OUT / "photos")
(OUT / "photos").mkdir()
for f in (HERE / "photos").glob("*.jpg"):
    shutil.copy(f, OUT / "photos" / f.name)
print("version web écrite :", OUT / "index.html", f"({n['i']} champs enregistrables)")
