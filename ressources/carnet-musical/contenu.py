# --- contenu ----------------------------------------------------------------
# Le carnet musical du mariage : questionnaire, morceaux par moment, ouverture de bal, listes à passer / à ne pas passer.

def duo2(items, a="On adore", b="À éviter"):
    """Une ligne par style, deux cases : on adore / à éviter."""
    return '<ul class="checks duos">' + "".join(
        f'<li><span>{e(q)}</span><span class="duo"><i></i><em>{e(a)}</em><i></i><em>{e(b)}</em></span></li>' for q in items) + "</ul>"

def morceaux(titre, intro, titres, lignes_libres):
    """Un moment de la journée : morceaux classiques à cocher + lignes pour les vôtres."""
    return block(titre, p(intro) + '<div class="songs">' + checks(titres) + '</div>' +
                 fields(lignes_libres, hint="titre, artiste"))

def grid(entetes, n, premier="N°", lignes=None):
    th = "".join(f"<th>{e(h)}</th>" for h in entetes)
    rows = ""
    for i in range(1, n + 1):
        lab = lignes[i - 1] if lignes else str(i)
        rows += f'<tr><td class="n{" lab" if lignes else ""}">{e(lab)}</td>' + "".join(
            f'<td data-l="{e(h)}"><span class="cl"></span></td>' for h in entetes) + "</tr>"
    return f'<table class="grid keep"><thead><tr><th>{e(premier)}</th>{th}</tr></thead><tbody>{rows}</tbody></table>'

parts = []

parts.append(f'''<section class="cover dark">
{lockup("on-dark")}
<p class="kicker">Carnet gratuit</p>
<h1>Le carnet musical<br><em>du mariage</em></h1>
{SPRIG}
<p class="sub">Le questionnaire, les morceaux par moment et vos listes</p>
<p class="lead">Un carnet à remplir à deux pour préparer la musique de votre journée : ce que vous aimez, ce que vous voulez entendre, et ce qui ne doit jamais passer.</p>
</section>''')

parts.append('__TOC__')
parts.append('<main>')

# 01 ---------------------------------------------------------------------------
parts.append(chapter("01", "Avant de commencer",
    "La musique d'un mariage se prépare à deux, en quelques soirées. Ce carnet vous guide, du premier questionnaire jusqu'à la liste à remettre à votre DJ."))
parts.append(block("Votre mariage en deux lignes", fields([
    "Nos prénoms", "Date du mariage", "Lieu de la réception", "Nombre d'invités à la soirée"], ) ))
parts.append(block("Comment remplir ce carnet", checks([
    "Remplissez le questionnaire chacun de votre côté, puis comparez vos réponses.",
    "Cochez les morceaux qui vous plaisent dans chaque moment de la journée, et ajoutez les vôtres.",
    "Choisissez votre ouverture de bal en dernier, quand vous aurez une idée de l'ambiance voulue.",
    "Notez les morceaux à passer absolument et ceux à ne jamais passer.",
    "Envoyez le tout à votre DJ plusieurs semaines avant la date, pour qu'il puisse poser des questions."])))
parts.append(tip("Les listes de ce carnet sont des suggestions classiques de mariage. Elles ne sont pas une liste imposée : gardez ce qui vous ressemble et ajoutez le reste."))

# 02 ---------------------------------------------------------------------------
parts.append(chapter("02", "Le questionnaire musical",
    "Quelques questions à remplir chacun de votre côté. Vos réponses donneront le ton de toute la journée."))
parts.append(block("Vos goûts, côte à côte",
    grid(["Prénom 1", "Prénom 2"], 7, premier="Question", lignes=[
        "Le style qu'on écoute le plus",
        "Un artiste qu'on adore",
        "La chanson de nos débuts",
        "Le morceau qui nous donne envie de danser",
        "Un morceau qui nous rappelle un voyage ou un concert",
        "Le morceau qu'on ne supporte plus",
        "Une chanson de notre enfance"])))
parts.append(block("Les styles de musique",
    p("Pour chaque style, cochez « On adore » ou « À éviter ». Laissez vide si cela vous est égal.") +
    duo2(["Chanson française", "Pop internationale", "Rock", "Disco et funk", "Années 80", "Années 90", "Années 2000",
          "Hits d'aujourd'hui", "Rock'n'roll et twist", "Soul et R&B", "Hip-hop", "Musiques latines",
          "Musiques basques", "Électro et house", "Slows"])))
parts.append(block("Vos invités", checks([
    "Beaucoup d'enfants et d'adolescents",
    "Beaucoup d'invités de 25 à 40 ans",
    "Beaucoup d'invités de 40 à 60 ans",
    "Beaucoup d'invités de plus de 60 ans",
    "Des invités étrangers, avec des musiques de leur pays à prévoir"]) +
    fields(["Les invités qui adorent danser", "Les invités qui préfèrent discuter"])))
parts.append(block("Votre façon de faire",
    p("Choisissez ce qui vous correspond le mieux.") + checks([
        "On préfère laisser le DJ lire la salle et adapter les morceaux.",
        "On veut une liste de morceaux précis à respecter.",
        "On veut un mélange : quelques morceaux imposés, le reste au feeling du DJ."]) +
    fields(["Ce qui compte le plus pour nous dans la musique ce jour-là"])))

# 03 ---------------------------------------------------------------------------
parts.append(chapter("03", "L'ouverture de bal",
    "C'est le premier moment dansé de la soirée. Elle se prépare un peu à l'avance, mais elle n'a pas besoin d'être parfaite."))
parts.append(block("Pour choisir votre chanson", checks([
    "Elle vous plaît à tous les deux, et vous avez envie de l'entendre en public.",
    "Son rythme vous permet de danser à votre aise, même sans avoir pris de cours.",
    "Vous connaissez les paroles ou vous savez ce qu'elles racontent.",
    "Sa durée vous convient, ou vous avez prévu avec votre DJ de la raccourcir.",
    "Vous avez décidé si vos proches viennent vous rejoindre en cours de chanson."])))
parts.append(block("Quelques idées pour vous inspirer",
    p("Romantiques, joyeuses ou plus originales : cochez celles qui vous tentent.") + '<div class="songs">' + checks([
        "« Perfect », Ed Sheeran", "« All of Me », John Legend", "« At Last », Etta James",
        "« Can't Help Falling in Love », Elvis Presley", "« La Vie en rose », Édith Piaf",
        "« Je l'aime à mourir », Francis Cabrel", "« Pour que tu m'aimes encore », Céline Dion",
        "« A Thousand Years », Christina Perri", "« Marry Me », Train",
        "« (I've Had) The Time of My Life », Bill Medley et Jennifer Warnes",
        "« I Wanna Dance with Somebody », Whitney Houston", "« La Valse d'Amélie », Yann Tiersen"]) + '</div>'))
parts.append(block("Votre choix", fields([
    "Idée 1 (titre, artiste)", "Idée 2 (titre, artiste)", "Idée 3 (titre, artiste)",
    "Notre choix final", "Ce qu'on veut : une chanson entière, ou seulement le début ?"]) +
    checks(["On ouvre le bal avant le gâteau.", "On ouvre le bal après le gâteau.", "On décide avec notre DJ.",
            "Nos proches nous rejoignent pendant la chanson."])))

# 04 ---------------------------------------------------------------------------
parts.append(chapter("04", "Vos morceaux par moment",
    "Cochez les morceaux qui vous plaisent et complétez avec les vôtres. Pas besoin de tout remplir."))
parts.append(morceaux("La cérémonie",
    "Entrée, passage à la signature, sortie : des morceaux calmes ou plus joyeux selon l'ambiance voulue.", [
        "« Canon en ré majeur », Johann Pachelbel", "« Marche nuptiale », Felix Mendelssohn",
        "« Ave Maria », Franz Schubert", "« Hallelujah », Leonard Cohen", "« A Thousand Years », Christina Perri",
        "« Perfect », Ed Sheeran", "« Can't Help Falling in Love », Elvis Presley", "« Marry You », Bruno Mars",
        "« Je te promets », Johnny Hallyday", "« Signed, Sealed, Delivered I'm Yours », Stevie Wonder",
        "« Happy », Pharrell Williams", "« Walking on Sunshine », Katrina and the Waves"],
    ["Entrée des mariés", "Pendant la signature", "Sortie de cérémonie"]))
parts.append(morceaux("Le cocktail",
    "De la musique de fond, conviviale, qui laisse les invités discuter.", [
        "« Fly Me to the Moon », Frank Sinatra", "« What a Wonderful World », Louis Armstrong",
        "« Aux Champs-Élysées », Joe Dassin", "« Don't Know Why », Norah Jones", "« Banana Pancakes », Jack Johnson",
        "« Isn't She Lovely », Stevie Wonder", "« Lovely Day », Bill Withers", "« Here Comes the Sun », The Beatles",
        "« I'm Yours », Jason Mraz", "« Je veux », Zaz", "« La Bohème », Charles Aznavour", "« Je m'en vais », Vianney"],
    ["Nos morceaux pour le cocktail", "Un artiste qu'on veut entendre"]))
parts.append(morceaux("Le repas",
    "Une ambiance douce et chaleureuse, avec quelques classiques pour toutes les générations.", [
        "« La Mer », Charles Trenet", "« Les Copains d'abord », Georges Brassens", "« Quand on n'a que l'amour », Jacques Brel",
        "« Come Away with Me », Norah Jones", "« La Vie en rose », Édith Piaf", "« Les Lacs du Connemara », Michel Sardou",
        "« Sweet Caroline », Neil Diamond", "« Dancing Queen », ABBA"],
    ["Nos morceaux pour le repas", "Un moment spécial à marquer (discours, gâteau)"]))
parts.append(morceaux("La soirée dansante",
    "Des morceaux qui font danser plusieurs générations. Cochez ceux que vous voulez, laissez votre DJ lire la salle pour le reste.", [
        "« Dancing Queen », ABBA", "« Stayin' Alive », Bee Gees", "« September », Earth, Wind and Fire",
        "« I Will Survive », Gloria Gaynor", "« Billie Jean », Michael Jackson", "« Girls Just Want to Have Fun », Cyndi Lauper",
        "« Don't Stop Me Now », Queen", "« Y.M.C.A. », Village People", "« L'Aventurier », Indochine",
        "« Alexandrie Alexandra », Claude François", "« Voyage voyage », Desireless", "« Les Démons de minuit », Images",
        "« Alors on danse », Stromae", "« Papaoutai », Stromae", "« Femme Like U », K-Maro",
        "« Dragostea Din Tei », O-Zone", "« Lady (Hear Me Tonight) », Modjo", "« Macarena », Los del Río",
        "« Mr. Brightside », The Killers", "« Wonderwall », Oasis", "« Livin' on a Prayer », Bon Jovi",
        "« Sweet Child o' Mine », Guns N' Roses", "« Johnny B. Goode », Chuck Berry", "« Twist and Shout », The Beatles",
        "« Uptown Funk », Mark Ronson et Bruno Mars", "« Shut Up and Dance », Walk the Moon", "« Levitating », Dua Lipa",
        "« Blinding Lights », The Weeknd", "« Can't Stop the Feeling! », Justin Timberlake"],
    ["Nos morceaux pour danser", "Pour les années 80 et 90", "Pour les plus jeunes", "Pour les plus âgés"]))
parts.append(morceaux("La fin de soirée",
    "Les derniers morceaux, ceux que tout le monde chante ensemble.", [
        "« Bohemian Rhapsody », Queen", "« Tous les cris les SOS », Daniel Balavoine",
        "« Quand la musique est bonne », Jean-Jacques Goldman", "« Je te donne », Jean-Jacques Goldman et Michael Jones",
        "« Les Lacs du Connemara », Michel Sardou", "« Sweet Caroline », Neil Diamond"],
    ["Notre dernier morceau", "Un morceau qui nous ressemble"]))

# 05 ---------------------------------------------------------------------------
parts.append(chapter("05", "À passer, à ne jamais passer",
    "Deux listes courtes, mais précieuses pour votre DJ : ce qui doit absolument passer, et ce qui doit rester dehors."))
parts.append(block("Les morceaux à passer absolument",
    p("Des morceaux qui comptent pour vous, quelle que soit l'ambiance du moment.") + fields([
        "Morceau 1", "Morceau 2", "Morceau 3", "Morceau 4", "Morceau 5"], hint="titre, artiste")))
parts.append(block("Les morceaux à ne jamais passer",
    p("Pour des raisons de goût, de souvenir ou de famille, chacun a ses morceaux à éviter.") + fields([
        "Morceau 1", "Morceau 2", "Morceau 3", "Morceau 4", "Morceau 5"], hint="titre, artiste")))
parts.append(block("Les points de vigilance", checks([
    "Des morceaux liés à d'anciennes relations ou à des souvenirs difficiles.",
    "Des paroles que vous préférez éviter devant les enfants ou les grands-parents.",
    "Des styles que certains invités supportent mal, ou à volume plus bas.",
    "Des chansons déjà trop entendues dans la saison."]) +
    fields(["Autre chose à savoir sur la musique ou les invités"])))

# 06 ---------------------------------------------------------------------------
parts.append(chapter("06", "Avant de remettre votre liste",
    "Quelques vérifications pour que votre DJ ait tout ce qu'il lui faut, bien avant la date."))
parts.append(block("Votre liste de contrôle", checks([
    "Le questionnaire est rempli par les deux mariés.",
    "L'ouverture de bal est choisie, avec la durée souhaitée.",
    "Les morceaux à passer absolument sont notés.",
    "Les morceaux à ne jamais passer sont notés.",
    "Les moments particuliers sont prévenus : entrée, discours, gâteau, surprise des proches.",
    "Les horaires de fin de musique du lieu sont demandés au lieu et transmis au DJ.",
    "La liste est envoyée au DJ plusieurs semaines avant la date."])))
parts.append(block("Votre message au DJ",
    p("Un petit mot pour accompagner ce carnet, que vous pouvez recopier.") +
    '<blockquote class="mot">Bonjour, voici notre carnet musical pour le mariage du [date] à [lieu]. Vous y trouverez nos goûts, notre ouverture de bal, les morceaux à passer absolument et ceux à éviter. N\'hésitez pas à nous poser vos questions. Merci !</blockquote>' +
    fields(["Dernier point à préciser", "Date d'envoi prévue"])))

parts.append('</main>')
parts.append(f'''<footer class="end">
{lockup("on-dark")}
{SPRIG}
<p class="merci">Que la musique soit belle.</p>
<p>Ce carnet est gratuit et offert par Richard DJ Event. Les morceaux proposés sont des suggestions classiques de mariage : choisissez ceux qui vous ressemblent.</p>
<p class="cta">Parlons de la musique de votre mariage</p>
<p><a href="tel:+33684331824">06 84 33 18 24</a> · <a href="mailto:richarddjevent@gmail.com">richarddjevent@gmail.com</a></p>
<p class="sites">djmariagepaysbasque.fr<br>djmariagelandes.fr</p>
</footer>''')
