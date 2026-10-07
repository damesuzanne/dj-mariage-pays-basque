export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    // Adresse unique : www.djmariagepaysbasque.fr redirige vers
    // djmariagepaysbasque.fr (01/10/26 : le www pointait encore vers
    // l'ancien hébergement WordPress et renvoyait une erreur 522).
    if (url.hostname === 'www.djmariagepaysbasque.fr') {
      url.hostname = 'djmariagepaysbasque.fr'
      return Response.redirect(url.toString(), 301)
    }

    // Ancienne adresse du blog (05/10/26) : /preparer-son-mariage/* -> /conseils/*
    if (url.pathname.startsWith('/preparer-son-mariage')) {
      url.pathname = url.pathname.replace('/preparer-son-mariage', '/conseils')
      return Response.redirect(url.toString(), 301)
    }

    // Endpoint du formulaire de contact (POST uniquement)
    if (
      (url.pathname === '/api/contact' || url.pathname === '/api/contact/verify') &&
      request.method === 'POST'
    ) {
      return handleCaptchaVerification(request, env)
    }

    // Ressources gratuites du blog (prénom + e-mail -> guide envoyé par e-mail)
    if (url.pathname === '/api/ressource' && request.method === 'POST') {
      return handleRessource(request, env)
    }

    // Tout le reste → fichiers statiques du site
    const response = await env.ASSETS.fetch(request)

    // robots.txt/llms.txt servis en text/plain sans charset par défaut : sur
    // certains user-agents (constaté en dev), l'absence de charset fait
    // deviner un mauvais encodage et casse les accents. Forcé en UTF-8.
    if (url.pathname === '/llms.txt' || url.pathname === '/robots.txt') {
      const headers = new Headers(response.headers)
      headers.set('Content-Type', 'text/plain; charset=utf-8')
      return new Response(response.body, { status: response.status, statusText: response.statusText, headers })
    }

    // Fiche contact vCard : type MIME explicite + UTF-8 (accents lus
    // correctement à l'import). Servie « inline » : c'est ce qui permet à
    // Safari iOS d'ouvrir directement la fiche « Ajouter aux contacts ».
    // Une Content-Disposition « attachment » casse ce comportement sur iOS
    // (le fichier part dans Fichiers sans rien afficher). Sur ordinateur,
    // le navigateur télécharge quand même le .vcf (aucun visualiseur natif)
    // et l'attribut download du lien fournit le nom de fichier.
    if (url.pathname === '/richard-dj-event.vcf') {
      const headers = new Headers(response.headers)
      headers.set('Content-Type', 'text/vcard; charset=utf-8')
      headers.set('Content-Disposition', 'inline; filename="richard-dj-event.vcf"')
      headers.set('Cache-Control', 'public, max-age=3600')
      return new Response(response.body, { status: response.status, statusText: response.statusText, headers })
    }

    // Redirige les adresses inexistantes vers la page 404 personnalisée.
    // La page d'arrivée porte une directive noindex afin de rester exclue
    // des résultats de recherche tout en étant visible dans tous les navigateurs.
    // Version anglaise : une adresse inconnue sous /en/ mène à la 404 en anglais.
    if (response.status === 404 && request.method === 'GET') {
      const enAnglais = url.pathname === '/en' || url.pathname.startsWith('/en/')
      const notFoundUrl = new URL(enAnglais ? '/en/404' : '/404', url)
      return Response.redirect(notFoundUrl.toString(), 302)
    }

    return response
  },
}

async function handleCaptchaVerification(request, env) {
  try {
    const formData = await request.formData()

    // Honeypot — un bot qui remplit botcheck est rejeté silencieusement
    const botcheck = formData.get('botcheck')
    if (botcheck === 'on' || botcheck === 'true' || botcheck === '1') {
      return json({ success: true })
    }

    // Vérification Turnstile côté serveur (uniquement si le secret est configuré).
    // La clé secrète ne quitte jamais le Worker.
    if (env.TURNSTILE_SECRET) {
      const token = formData.get('cf-turnstile-response')
      if (!token) {
        return json({ success: false, message: 'Captcha requis.' }, 400)
      }
      const ip = request.headers.get('CF-Connecting-IP') ?? ''
      const ok = await verifyTurnstile(token, ip, env.TURNSTILE_SECRET)
      if (!ok) {
        return json({ success: false, message: 'Captcha invalide, veuillez réessayer.' }, 400)
      }
    }

    // L’offre gratuite Web3Forms refuse les appels provenant d’un serveur.
    // Le Worker valide donc uniquement Turnstile ; le navigateur transmet
    // ensuite le formulaire directement à Web3Forms avec sa clé publique.
    return json({ success: true })
  } catch (_) {
    return json({ success: false, message: 'Erreur serveur.' }, 500)
  }
}

// /api/ressource : formulaire « Recevoir le guide » des articles du blog.
// Vérifie le pot de miel et Turnstile, puis transmet au programme Apps Script
// du Drive de Richard (ressources/apps-script/Code.gs) qui enregistre le lead
// dans le Sheet « Inbound leads » et envoie le guide depuis son Gmail.
// Secrets Cloudflare : LEADS_WEBHOOK_URL (URL /exec) et LEADS_WEBHOOK_SECRET.
const RESSOURCES_AUTORISEES = ['checklist-retroplanning', 'livret-jeux', 'annuaire-lieux', 'carnet-musical']

async function handleRessource(request, env) {
  let data
  try {
    data = await request.json()
  } catch (_) {
    return json({ success: false, message: 'Requête invalide.' }, 400)
  }

  if (data.botcheck) return json({ success: true })

  const prenom = String(data.prenom ?? '').trim().slice(0, 60)
  const email = String(data.email ?? '').trim().slice(0, 120)
  if (!prenom || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ success: false, message: 'Prénom ou e-mail invalide.' }, 400)
  }
  if (data.consentement !== true) {
    return json({ success: false, message: 'Le consentement est requis.' }, 400)
  }
  if (!RESSOURCES_AUTORISEES.includes(data.ressource)) {
    return json({ success: false, message: 'Ressource inconnue.' }, 400)
  }

  if (env.TURNSTILE_SECRET) {
    const ip = request.headers.get('CF-Connecting-IP') ?? ''
    if (!data.token || !(await verifyTurnstile(data.token, ip, env.TURNSTILE_SECRET))) {
      return json({ success: false, message: 'Captcha invalide, veuillez réessayer.' }, 400)
    }
  }

  if (!env.LEADS_WEBHOOK_URL || !env.LEADS_WEBHOOK_SECRET) {
    return json({ success: false, message: 'Service indisponible.' }, 503)
  }

  try {
    // Apps Script répond par une redirection 302 vers googleusercontent.com :
    // fetch la suit en GET, ce qui renvoie bien la réponse JSON du script.
    const res = await fetch(env.LEADS_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: env.LEADS_WEBHOOK_SECRET,
        prenom,
        email,
        ressource: data.ressource,
        consentement: true,
        site: new URL(request.url).hostname,
        page: String(data.page ?? '').slice(0, 200),
      }),
    })
    const out = await res.json().catch(() => ({}))
    return json({ success: out.success === true }, out.success === true ? 200 : 502)
  } catch (_) {
    return json({ success: false, message: 'Erreur serveur.' }, 502)
  }
}

async function verifyTurnstile(token, ip, secret) {
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret, response: token, remoteip: ip }),
  })
  const data = await res.json()
  return data.success === true
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}
