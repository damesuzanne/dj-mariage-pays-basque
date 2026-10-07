import fs from 'fs';
const icons = {
 cal:'<rect x="14" y="20" width="52" height="46" rx="8"/><path d="M14 36h52M28 12v14M52 12v14"/><path d="M30 50l7 7 13-14"/>',
 rain:'<path d="M26 46a14 14 0 1 1 4-27 18 18 0 0 1 33 8 11 11 0 0 1-2 19H26z"/><path d="M30 56l-5 10M44 56l-5 10M58 56l-5 10"/>',
 sound:'<path d="M14 32h14l20-16v48L28 48H14z"/><path d="M58 30a14 14 0 0 1 0 20M66 22a26 26 0 0 1 0 36"/>',
 clock:'<circle cx="40" cy="40" r="28"/><path d="M40 22v19l13 8"/>',
 list:'<rect x="16" y="12" width="48" height="58" rx="8"/><path d="M26 30l5 5 9-10M26 52l5 5 9-10M48 32h8M48 54h8"/>',
};
const slides = [
 {k:'hook'},
 {n:'01', q:1, t:'Ton mariage approche.<br><em>Tu as oublié quoi ?</em>', s:'Un rétroplanning mois par mois. Tu sais toujours ce qui vient ensuite.'},
 {n:'02', q:1, t:'Ton budget est bouclé.<br><em>Les suppléments aussi ?</em>', s:'La liste complète des dépenses à prévoir, pour réserver l’esprit tranquille.'},
 {n:'03', q:1, t:'Ton Jour J<br><em>en un coup d’œil</em>', s:'Le déroulé heure par heure et tous tes contacts utiles, réunis au même endroit.'},
 {n:'04', q:1, t:'Le plan de table<br><em>devient un jeu</em>', s:'Une méthode simple pour le boucler, et une idée qui va faire rire tes invités.'},
 {n:'05', q:1, t:'Des astuces<br><em>à chaque étape</em>', s:'Paperasse, prestataires, musique : de quoi alléger ton organisation, sans y passer tes soirées.'},
 {k:'transition'},
 {k:'cta'},
];
const leaf=(x,y,r,rot,c='#a8b898')=>`<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r*.38}" transform="rotate(${rot} ${x} ${y})" fill="${c}"/>`;
const flower=(x,y,s=1)=>`<g transform="translate(${x} ${y}) scale(${s})">${[0,72,144,216,288].map(a=>`<ellipse cx="0" cy="-15" rx="11" ry="16" transform="rotate(${a})" fill="#fffaf0" stroke="#ecdcb8" stroke-width="1.5"/>`).join('')}<circle r="7" fill="#c6a15b"/></g>`;
const botanical=()=>`<img class="art tl" src="art-tl-01.png"><img class="art br" src="art-br-01.png">`;
const css = `
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=Outfit:wght@300;400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{--night:#101522;--cream:#faf7f1;--deep:#f2ecdf;--gold:#c6a15b;--ink:#23283a;--soft:#5a6072;--sage:#9db08c}
body{font-variant-numeric:lining-nums;width:1080px;height:1350px;background:radial-gradient(circle at 85% 8%,#f6ecd6 0,#faf7f1 45%),var(--cream);color:var(--ink);font-family:'Outfit',sans-serif;position:relative;overflow:hidden}
.frame{position:absolute;inset:44px;border:1.5px solid var(--gold);opacity:.5;border-radius:4px}
.art{position:absolute;width:290px;}
.art.tl{top:0;left:0}
.art.br{bottom:0;right:0}
.top{position:absolute;top:104px;left:0;right:0;text-align:center;font-family:'Playfair Display',serif;font-size:36px;font-style:italic;color:var(--gold);font-weight:500}
.foot{position:absolute;bottom:92px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:20px;font-size:24px;letter-spacing:.14em;color:var(--soft)}
.dots{display:flex;gap:12px}.dots i{width:12px;height:12px;border-radius:50%;background:#d9d1bd}.dots i.on{background:var(--gold);width:34px;border-radius:8px}
.c{position:absolute;left:120px;right:120px;top:190px;bottom:200px;display:flex;flex-direction:column;justify-content:center}
h1,h2{font-family:'Playfair Display',serif;font-weight:600;line-height:1.08;color:var(--night)}
.hook .c{align-items:center;text-align:center}
.hook .l1{font-family:'Playfair Display',serif;font-size:88px;font-weight:600;color:var(--night);line-height:1.1}
.hook .big{font-family:'Playfair Display',serif;font-size:400px;line-height:.95;font-weight:600;font-variant-numeric:lining-nums;background:linear-gradient(135deg,#b88f45,#e8cf94 55%,#c6a15b);-webkit-background-clip:text;color:transparent;margin:6px 0 4px;letter-spacing:-.02em}
.hook .l3{font-family:'Playfair Display',serif;font-size:88px;font-weight:600;color:var(--night);line-height:1.1}
.pill{margin-top:56px;background:var(--night);color:#e3c98f;font-size:32px;letter-spacing:.06em;padding:20px 44px;border-radius:60px}
.row{margin-bottom:20px}
.num{font-family:'Playfair Display',serif;font-variant-numeric:lining-nums;font-size:220px;line-height:1;color:var(--gold);font-weight:500}
.ic{width:190px;height:190px;border-radius:50%;background:var(--night);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 10px #faf7f1,0 0 0 12px var(--gold)}
.ic svg{width:104px;height:104px;fill:none;stroke:#e3c98f;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}
h2.q{font-size:76px;line-height:1.12;white-space:nowrap}
h2.q em{font-style:italic;font-weight:500;color:var(--gold)}
h2{font-size:118px;line-height:1.02;letter-spacing:-.01em}
.rule{width:110px;height:3px;background:var(--gold);margin:50px 0}
.txt{font-size:46px;font-weight:300;line-height:1.4;color:var(--ink);max-width:820px}
.tr-c{top:185px;bottom:auto;right:120px}
.big7{font-family:'Playfair Display',serif;font-size:56px;line-height:1.2;color:var(--night);font-weight:500}
.big7 b{color:var(--gold);font-weight:700}
.l2{font-size:31px;font-weight:300;color:var(--soft);line-height:1.38;margin-top:30px}
.l2 b{font-weight:500;color:var(--ink)}
.mock{position:absolute;left:0;right:0;bottom:200px;height:400px}
.pg{position:absolute;width:265px;border-radius:10px;box-shadow:0 30px 60px -20px rgba(16,21,34,.45),0 0 0 1px #e8dcc0}
.pg.a{left:240px;top:45px;transform:rotate(-7deg)}
.pg.b{left:515px;top:10px;transform:rotate(5deg)}
.badges{position:absolute;left:0;right:0;bottom:84px;display:flex;justify-content:center;gap:14px}
.cta .c{align-items:center;text-align:center}
.cta .c img{width:200px;height:200px;margin-bottom:34px}
.brand{font-family:'Playfair Display',serif;font-size:46px;color:var(--night);font-weight:600}
.tag{font-family:'Playfair Display',serif;font-style:italic;font-size:32px;color:var(--gold);margin-top:10px}
.cta h2{font-size:96px;margin:70px 0 0;line-height:1.1}
.cta h2 .l2b{font-size:72px;font-weight:500}
.cta h2 em{font-style:italic;color:var(--gold);font-weight:500}
.inc{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:16px 30px;margin-top:34px}
.inc li{font-size:31px;color:var(--ink);display:flex;align-items:center;gap:16px;line-height:1.2}
.inc li::before{content:'';flex:none;width:26px;height:26px;border:2.5px solid var(--gold);border-radius:6px;background:linear-gradient(transparent 0,transparent 100%)}
body.cta{background:radial-gradient(circle at 50% 30%,#1d2638 0,#101522 60%)}
.cta .brand,.cta h2{color:#faf7f1}
.cta .tag,.cta h2 em{color:#e3c98f}
.cta .bio{color:#c9ccd6}
.cta .foot{color:#c9ccd6}
.cta .dots i{background:#3a4358}.cta .dots i.on{background:#c6a15b}
.cta .c img{border-radius:50%;box-shadow:0 0 0 2px #c6a15b,0 0 0 14px #101522,0 0 0 15px rgba(198,161,91,.5)}
.cta .frame{opacity:.6}
.bio{font-size:38px;font-weight:300;color:var(--soft);margin-top:50px;line-height:1.4;max-width:800px}
`;
const dots=i=>`<div class="dots">${slides.map((_,j)=>`<i class="${j===i?'on':''}"></i>`).join('')}</div>`;
slides.forEach((s,i)=>{
 let b='';
 if(s.k==='hook') b=`<div class="top">Mariage · Pays Basque · 2026 et 2027</div><div class="c"><div class="l1">La checklist que</div><div class="big">90%</div><div class="l3">des mariées oublient</div><div class="pill">Et qui coûte cher le Jour J</div></div>`;
 else if(s.k==='transition') b=`<div class="top">Ce que tu reçois</div><div class="c tr-c"><p class="big7">Tout ce qu’il faut faire, <b>mois par mois</b>, dans un seul guide.</p><ul class="inc"><li>Rétroplanning 18 mois</li><li>Budget poste par poste</li><li>Déroulé heure par heure</li><li>Plan de table en 4 étapes</li><li>Repères musicaux</li><li>Feuille de route Jour J</li></ul><p class="l2">Tu coches <b>directement sur ton téléphone</b> ou tu l’imprimes en A4.</p></div><div class="mock"><img class="pg a" src="pg-cover-01.png"><img class="pg b" src="pg-retro-06.png"></div>`;
 else if(s.k==='cta') b=`<div class="c"><img src="logo-monogram.png"><div class="brand">Richard DJ Event</div><div class="tag">DJ Mariages Pays Basque &amp; Landes</div><h2>Commente <em>CHECKLIST</em><br><span class="l2b">je t’envoie le lien</span></h2></div>`;
 else b=`<div class="c"><div class="row"><div class="num">${s.n}</div></div><h2${s.q?' class="q"':''}>${s.t}</h2><div class="rule"></div><p class="txt">${s.s}</p></div>`;
 fs.writeFileSync(`src/s${i+1}.html`,`<!doctype html><html lang="fr"><meta charset="utf-8"><style>${css}</style><body class="${s.k||''}"><div class="frame"></div>${b}<div class="foot"><span>@richard.dj.event</span>${dots(i)}</div></body></html>`);
});
