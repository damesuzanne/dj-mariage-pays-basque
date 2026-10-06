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
