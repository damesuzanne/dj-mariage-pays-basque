export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    // Endpoint du formulaire de contact (POST uniquement)
    if (url.pathname === '/api/contact' && request.method === 'POST') {
      return handleContact(request, env)
    }

    // Tout le reste → fichiers statiques du site
    return env.ASSETS.fetch(request)
  },
}

async function handleContact(request, env) {
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

    // Transmission à Web3Forms — la clé Web3Forms reste côté serveur
    const payload = new FormData()
    payload.append('access_key', env.WEB3FORMS_KEY)
    payload.append('from_name', 'Site DJ Mariage Pays Basque')
    for (const [key, value] of formData.entries()) {
      if (key === 'cf-turnstile-response' || key === 'botcheck') continue
      payload.append(key, value)
    }

    const w3f = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: payload,
    })
    // Web3Forms renvoie du JSON en cas de succès ; en cas d'erreur il peut renvoyer
    // une page HTML → on gère les deux pour ne jamais planter.
    const text = await w3f.text()
    try {
      const result = JSON.parse(text)
      return json(result, w3f.status)
    } catch (_) {
      return json({ success: false, message: 'Envoi refusé par Web3Forms.' }, w3f.status || 400)
    }
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
