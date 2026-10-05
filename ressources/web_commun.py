#!/usr/bin/env python3
"""Convertit le HTML d'une ressource (guide.html, livret.html, annuaire) en version web à remplir :
cases et lignes enregistrées automatiquement sur l'appareil (localStorage), sommaire cliquable.
Utilisé par guide-checklist/web.py et livret-jeux/web.py.
"""
import pathlib, re, shutil

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
FONTS = (HERE / "annuaire-lieux/fonts.css").read_text()
FONTS = re.sub(r"(font-family:'Outfit'[^}]*?)font-weight:400", r"\1font-weight:100 900", FONTS)
FONTS = re.sub(r"(font-family:'Playfair Display'[^}]*?)font-weight:(400|500)", r"\1font-weight:400 900", FONTS)

EXTRA = '''
html{scroll-behavior:smooth}
.chapter,.venue,section[id]{scroll-margin-top:16px}
.toc li a:hover .tt{color:var(--gold)}
.toc .tp{transition:transform .15s;font-size:24px;line-height:1}
.toc li a:hover .tp{transform:translateX(3px)}
.screen-tools{margin:18px 0 6px;padding:14px 18px;background:#fff;border:1px solid var(--line,#eadfc8);border-radius:14px;font-size:14px;color:var(--muted)}
.st-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.st-actions a,.st-actions button{font:500 13px var(--sans);color:var(--navy);background:transparent;border:1px solid var(--gold);border-radius:30px;padding:8px 14px;text-decoration:none;cursor:pointer}
.st-actions a:hover,.st-actions button:hover{background:var(--cream2)}
.checks label{display:flex;gap:12px;align-items:flex-start;cursor:pointer;width:100%}
.checks .duo label{display:inline-flex;width:auto;gap:6px;align-items:center}
.checks input{position:absolute;opacity:0;width:1px;height:1px}
.checks input:checked+i{background:var(--gold);box-shadow:inset 0 0 0 3px var(--cream)}
.checks input:focus-visible+i{outline:2px solid var(--navy);outline-offset:2px}
.writing{position:relative;display:block}
.writing textarea,.grid textarea.cell{font:400 16px/1.3 var(--sans);color:var(--navy);background:transparent;border:0;resize:none;overflow:hidden}
.writing textarea{position:absolute;left:0;right:0;top:0;height:30px;padding:3px 2px 6px;outline:0}
.writing textarea:focus,.grid textarea.cell:focus{background:rgba(198,161,91,.1);outline:0}
.grid textarea.cell{position:absolute;left:6px;right:6px;top:3px;bottom:8px;width:calc(100% - 12px);height:calc(100% - 11px);padding:3px 2px}
@media(max-width:640px){.grid textarea.cell{position:static;display:block;width:100%;height:36px;padding:4px 2px 6px}}
.back-top{position:fixed;right:14px;bottom:14px;width:44px;height:44px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;text-decoration:none;font-size:20px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
@media print{.screen-tools,.back-top{display:none}.writing textarea,.grid textarea.cell{color:#000}}
'''

JS = '''(function(){var key='%KEY%',saved={},fs=[].slice.call(document.querySelectorAll('textarea,input[type=checkbox]')),st=document.getElementById('save-status');
try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
fs.forEach(function(f){if(f.id in saved){if(f.type==='checkbox')f.checked=saved[f.id];else f.value=saved[f.id]}
f.addEventListener('input',function(){saved[f.id]=f.type==='checkbox'?f.checked:f.value;
try{localStorage.setItem(key,JSON.stringify(saved));st.textContent='Enregistré sur cet appareil.'}catch(e){st.textContent='Impossible d’enregistrer ici : utilisez « Exporter mes réponses » pour les garder.'}})});
document.getElementById('export').onclick=function(){var b=new Blob([JSON.stringify(saved,null,2)],{type:'application/json'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='%EXPORT%.json';a.click();URL.revokeObjectURL(u)};
})();'''


def convert(src_html, slug, key, titre, drive_a4, drive_mobile, export_name):
    h = pathlib.Path(src_html).read_text(encoding="utf-8")
    n = {"i": 0}

    def nid():
        n["i"] += 1
        return f"r{n['i']}"

    def plain(t):
        return re.sub("<[^>]+>", "", t).replace('"', "&quot;")

    # duos « Elle / Lui » (deux cases par ligne)
    h = re.sub(r'<span class="duo"><i></i><em>(.*?)</em><i></i><em>(.*?)</em></span>',
               lambda m: (f'<span class="duo"><label><input type="checkbox" id="{nid()}"><i></i><em>{m.group(1)}</em></label>'
                          f'<label><input type="checkbox" id="{nid()}"><i></i><em>{m.group(2)}</em></label></span>'), h)
    # cases simples
    h = re.sub(r"<li><i></i><span>(.*?)</span></li>",
               lambda m: f'<li><label><input type="checkbox" id="{nid()}"><i></i><span>{m.group(1)}</span></label></li>', h)
    # champs (avec ou sans indication)
    h = re.sub(r'<label><b>(.*?)</b>(<small>.*?</small>)?<span class="line"></span></label>',
               lambda m: (f'<label><b>{m.group(1)}</b>{m.group(2) or ""}<span class="writing"><span class="line"></span>'
                          f'<textarea id="{nid()}" rows="1" aria-label="{plain(m.group(1))}"></textarea></span></label>'), h)
    # lignes des cartes (livret)
    h = re.sub(r'(<div class="carte"><b>(.*?)</b>)(<span class="line"></span>)(<span class="line"></span>)</div>',
               lambda m: (f'{m.group(1)}<span class="writing"><span class="line"></span><textarea id="{nid()}" rows="1" aria-label="{plain(m.group(2))}"></textarea></span>'
                          f'<span class="writing"><span class="line"></span><textarea id="{nid()}" rows="1" aria-label="{plain(m.group(2))}"></textarea></span></div>'), h)
    # cellules des tableaux
    h = re.sub(r'<td data-l="([^"]*)"><span class="cl"></span></td>',
               lambda m: (f'<td data-l="{m.group(1)}"><span class="cl"></span>'
                          f'<textarea id="{nid()}" class="cell" rows="1" aria-label="{m.group(1)}"></textarea></td>'), h)
    # sommaire : flèche cliquable à la place des numéros de page
    h = re.sub(r'<span class="tp">[^<]*</span>', '<span class="tp">›</span>', h)
    h = h.replace('<nav class="toc"', '<nav class="toc" id="top"', 1)
    # polices intégrées (pas de dépendance à Google Fonts)
    h = re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>', "", h)
    h = h.replace("<style>", "<style>" + FONTS, 1).replace("</style>", EXTRA + "</style>", 1)
    h = h.replace('<meta name="viewport"', '<meta name="robots" content="noindex"><meta name="viewport"', 1)
    tools = (f'<div class="screen-tools"><p id="save-status" role="status">Vos réponses s’enregistrent automatiquement sur cet appareil, dans ce navigateur. '
             f'Elles ne sont pas envoyées à Richard.</p><div class="st-actions">'
             f'<a href="https://drive.google.com/file/d/{drive_a4}/view" target="_blank" rel="noopener">PDF A4 à imprimer</a>'
             f'<a href="https://drive.google.com/file/d/{drive_mobile}/view" target="_blank" rel="noopener">PDF pour téléphone</a>'
             f'<button id="export" type="button">Exporter mes réponses</button></div></div>')
    h = h.replace("<main>", "<main>" + tools, 1)
    h = h.replace("</body>", '<a class="back-top" href="#top" aria-label="Retour au sommaire">↑</a><script>'
                  + JS.replace("%KEY%", key).replace("%EXPORT%", export_name) + "</script></body>", 1)
    out = SITE / "public/ressources" / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(h, encoding="utf-8")
    print(slug, f"{n['i']} champs enregistrables")
