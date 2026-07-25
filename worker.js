export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    // Endpoint du formulaire de contact (POST uniquement)
    if (
      (url.pathname === '/api/contact' || url.pathname === '/api/contact/verify') &&
      request.method === 'POST'
    ) {
      return handleCaptchaVerification(request, env)
    }

    // Tout le reste → fichiers statiques du site
    const response = await env.ASSETS.fetch(request)

    // Garantit une vraie réponse HTTP 404 avec la page personnalisée.
    // Le statut 404 est essentiel pour que les moteurs de recherche
    // n'indexent pas une adresse inexistante comme une page valide.
    if (response.status === 404 && request.method === 'GET') {
      const notFoundUrl = new URL('/404.html', url)
      const notFoundResponse = await env.ASSETS.fetch(new Request(notFoundUrl, request))
      const headers = new Headers(notFoundResponse.headers)
      headers.set('Cache-Control', 'public, max-age=300')
      headers.set('X-Robots-Tag', 'noindex, follow')

      return new Response(notFoundResponse.body, {
        status: 404,
        statusText: 'Not Found',
        headers,
      })
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
