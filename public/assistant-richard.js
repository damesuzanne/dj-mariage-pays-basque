
    (function () {
      if (document.getElementById("htags-demo-assistant-host")) return;
      var configElement = document.createElement("script");
      configElement.id = "htags-demo-assistant-config";
      configElement.type = "application/json";
      configElement.textContent = "{\"ctaTitle\":\"Et si cet assistant travaillait pour votre activité ?\",\"ctaText\":\"Une landing page conçue pour convertir, avec votre chatbot IA personnalisé et inclus sur demande.\",\"ctaLabel\":\"Lancez votre projet\",\"ctaHref\":\"https://www.htags.fr/contact/\",\"source\":\"https://djmariagepaysbasque.fr/\",\"match\":\"/__richard-dj__/\",\"name\":\"Assistant Richard DJ\",\"launcher\":\"Assistant Richard DJ\",\"qualify\":true,\"qualificationMode\":\"dj\",\"theme\":{\"accent\":\"#c6a15b\",\"accentDark\":\"#101522\",\"header\":\"#101522\",\"ink\":\"#23283a\",\"soft\":\"#faf7f1\",\"bodyFont\":\"Outfit, 'Helvetica Neue', Arial, sans-serif\",\"controlFont\":\"Outfit, 'Helvetica Neue', Arial, sans-serif\",\"headingFont\":\"'Playfair Display', Georgia, serif\"},\"summaryTitle\":\"Aperçu de votre projet de mariage\",\"mailSubject\":\"Nouvelle demande mariage qualifiée\",\"identityBadge\":\"Futurs mariés identifiés\",\"fieldsByIntent\":{\"Demande de disponibilité\":[[\"Demande\",\"intent\"],[\"Date du mariage\",\"date\"],[\"Secteur\",\"location\"],[\"Confirmation du projet\",\"projectStage\"],[\"Recherche de DJ\",\"djSearchStatus\"]],\"Préparer mon mariage\":[[\"Demande\",\"intent\"],[\"Date du mariage\",\"date\"],[\"Secteur\",\"location\"],[\"Lieu de réception\",\"venue\"],[\"Nombre d’invités\",\"guests\"],[\"Moments à sonoriser\",\"moments\"],[\"Prestations souhaitées\",\"services\"],[\"Ambiance musicale\",\"music\"],[\"Avancement du projet\",\"projectStage\"],[\"Recherche de DJ\",\"djSearchStatus\"]]},\"start\":\"start\",\"steps\":{\"start\":{\"key\":\"intent\",\"message\":\"Bonjour 👋 Je peux vous aider à préparer votre mariage ou à transmettre une demande de disponibilité à Richard. Que souhaitez-vous faire ?\",\"choices\":[[\"Demande de disponibilité\",\"dj_availability_date\"],[\"Préparer mon mariage\",\"dj_project_date\"],[\"Découvrir les prestations\",\"dj_services_info\"],[\"Être rappelé par Richard\",\"callback\"],[\"Coordonnées & zone d’intervention\",\"contact_info\"]]},\"dj_availability_date\":{\"dateInput\":true,\"key\":\"date\",\"message\":\"À quelle date aura lieu votre mariage ?\",\"label\":\"Date du mariage\",\"buttonLabel\":\"Valider cette date\",\"next\":\"dj_availability_location\"},\"dj_availability_location\":{\"key\":\"location\",\"message\":\"Dans quel secteur se déroulera le mariage ?\",\"choices\":[[\"Bayonne / Anglet\",\"dj_availability_stage\"],[\"Biarritz\",\"dj_availability_stage\"],[\"Saint-Jean-de-Luz / Hendaye\",\"dj_availability_stage\"],[\"Pays Basque intérieur\",\"dj_availability_stage\"],[\"Landes / Hossegor / Dax\",\"dj_availability_stage\"],[\"Autre secteur\",\"dj_availability_stage\"]]},\"dj_availability_stage\":{\"key\":\"projectStage\",\"message\":\"La date et le lieu de votre mariage sont-ils déjà confirmés ?\",\"choices\":[[\"Oui, la date et le lieu sont confirmés\",\"dj_search_status\"],[\"La date est confirmée, le lieu reste à choisir\",\"dj_search_status\"],[\"La date est encore flexible\",\"dj_search_status\"]]},\"dj_project_date\":{\"dateInput\":true,\"key\":\"date\",\"message\":\"Commençons par la date prévue pour votre mariage.\",\"label\":\"Date du mariage\",\"buttonLabel\":\"Valider cette date\",\"next\":\"dj_project_location\"},\"dj_project_location\":{\"key\":\"location\",\"message\":\"Dans quel secteur se déroulera votre mariage ?\",\"choices\":[[\"Bayonne / Anglet\",\"dj_venue\"],[\"Biarritz\",\"dj_venue\"],[\"Saint-Jean-de-Luz / Hendaye\",\"dj_venue\"],[\"Pays Basque intérieur\",\"dj_venue\"],[\"Landes / Hossegor / Dax\",\"dj_venue\"],[\"Autre secteur\",\"dj_venue\"]]},\"dj_venue\":{\"key\":\"venue\",\"message\":\"Quel est le nom du lieu de réception ? Si vous ne l’avez pas encore choisi, indiquez simplement « à définir ».\",\"input\":{\"type\":\"text\",\"label\":\"Lieu de réception\",\"placeholder\":\"Ex. : Domaine de Bassilour\",\"maxlength\":100,\"buttonLabel\":\"Valider le lieu\"},\"next\":\"dj_guests\"},\"dj_guests\":{\"key\":\"guests\",\"message\":\"Combien d’invités prévoyez-vous approximativement ?\",\"input\":{\"type\":\"number\",\"label\":\"Nombre d’invités\",\"placeholder\":\"Ex. : 120\",\"min\":10,\"max\":500,\"suffix\":\" invités\",\"buttonLabel\":\"Valider\"},\"next\":\"dj_moments\"},\"dj_moments\":{\"multi\":true,\"key\":\"moments\",\"message\":\"Quels moments souhaitez-vous confier à Richard ?\",\"choices\":[\"Cérémonie\",\"Vin d’honneur\",\"Repas\",\"Soirée dansante\"],\"buttonLabel\":\"Valider les moments\",\"next\":\"dj_options_choice\"},\"dj_options_choice\":{\"message\":\"Souhaitez-vous ajouter des prestations complémentaires ?\",\"choices\":[[\"Oui, choisir mes options\",\"dj_options\"],[\"Non, pas pour le moment\",\"dj_music\",\"Aucune option pour le moment\",\"services\"]]},\"dj_options\":{\"multi\":true,\"key\":\"services\",\"message\":\"Quelles prestations complémentaires vous intéressent ?\",\"choices\":[\"Éclairage d’ambiance et piste de danse\",\"Photobooth\",\"Vidéoprojection et écran\",\"Fumée pour l’ouverture de bal\",\"Stand barbe à papa et pop-corn\",\"Sonorisation mobile complémentaire\"],\"buttonLabel\":\"Valider les prestations\",\"next\":\"dj_music\"},\"dj_music\":{\"key\":\"music\",\"message\":\"Avez-vous déjà une idée précise pour la musique de votre mariage ?\",\"choices\":[[\"Oui, préciser mon idée\",\"dj_music_custom\"],[\"Un mélange totalement personnalisé\",\"dj_stage\"],[\"À définir avec Richard\",\"dj_stage\"]]},\"dj_music_custom\":{\"key\":\"music\",\"message\":\"Décrivez librement votre thème, un style musical ou une idée très précise.\",\"input\":{\"type\":\"text\",\"label\":\"Votre idée musicale\",\"placeholder\":\"Ex. : une soirée reggae, un thème cinéma, beaucoup de rock…\",\"maxlength\":180,\"buttonLabel\":\"Valider mon idée\"},\"next\":\"dj_stage\"},\"dj_stage\":{\"key\":\"projectStage\",\"message\":\"Où en est aujourd’hui l’organisation de votre mariage ?\",\"choices\":[[\"La date et le lieu sont confirmés\",\"dj_search_status\"],[\"La date est confirmée, le lieu reste à choisir\",\"dj_search_status\"],[\"L’organisation est en cours\",\"dj_search_status\"],[\"Je prends simplement des renseignements\",\"dj_search_status\"]]},\"dj_search_status\":{\"key\":\"djSearchStatus\",\"message\":\"Où en êtes-vous dans votre recherche de DJ ?\",\"choices\":[[\"Je commence mes recherches\",\"contact\"],[\"Je compare plusieurs DJ\",\"contact\"],[\"J’ai déjà reçu un ou plusieurs devis\",\"contact\"],[\"Notre choix est presque arrêté\",\"contact\"],[\"Nous devons remplacer un DJ devenu indisponible\",\"contact\"]]},\"dj_services_info\":{\"info\":true,\"message\":\"PRESTATIONS RICHARD DJ EVENT\\n\\n• Animation musicale personnalisée\\n• Sonorisation de la cérémonie et du vin d’honneur\\n• Éclairage d’ambiance et piste de danse\\n• Photobooth\\n• Vidéoprojection et écran\\n• Fumée pour l’ouverture de bal\\n• Stand barbe à papa et pop-corn\",\"choices\":[[\"Préparer mon mariage\",\"dj_project_date\",\"Préparer mon mariage\",\"intent\"],[\"Demande de disponibilité\",\"dj_availability_date\",\"Demande de disponibilité\",\"intent\"],[\"Revenir au menu principal\",\"start\"]]},\"contact_info\":{\"info\":true,\"message\":\"RICHARD DJ EVENT\\nBayonne · Pays Basque · Landes\\n\\n06 84 33 18 24\\nricharddjevent@gmail.com\\n\\nDisponible 7j/7 sur rendez-vous · Réponse sous 24 h.\",\"choices\":[[\"Être rappelé par Richard\",\"callback\"],[\"Appeler Richard\",\"tel:+33684331824\"],[\"Écrire à Richard\",\"mailto:richarddjevent@gmail.com\"],[\"Préparer mon mariage\",\"dj_project_date\",\"Préparer mon mariage\",\"intent\"],[\"Revenir au menu principal\",\"start\"]]}},\"realLive\":true,\"realPreview\":false,\"autoOpen\":false,\"contactEndpoint\":\"/api/contact\",\"recipient\":\"richarddjevent@gmail.com\",\"turnstileSiteKey\":\"0x4AAAAAADxOwNEZbVFGF9_e\"}";
      document.body.appendChild(configElement);
      
(function () {
  "use strict";

  if (document.getElementById("htags-demo-assistant-host")) return;
  var configElement = document.getElementById("htags-demo-assistant-config");
  if (!configElement) return;

  var config = JSON.parse(configElement.textContent);
  var answers = {};
  var host = document.createElement("div");
  host.id = "htags-demo-assistant-host";
  document.body.appendChild(host);

  var root = host.attachShadow({ mode: "open" });
  var css = [
    ":host{all:initial;--accent:", config.theme.accent, ";--accent-dark:", config.theme.accentDark,
    ";--header:", config.theme.header || config.theme.accentDark,
    ";--ink:", config.theme.ink, ";--soft:", config.theme.soft, ";--control-font:", config.theme.controlFont || config.theme.bodyFont,
    ";font-family:", config.theme.bodyFont, ";}",
    "*,*:before,*:after{box-sizing:border-box}",
    "button,a,input{font:inherit}",
    "button{cursor:pointer}",
    ".launcher{position:fixed;left:24px;bottom:24px;z-index:2147483000;display:flex;align-items:center;gap:10px;border:0;border-radius:999px;padding:10px 15px 10px 10px;color:white;background:var(--accent);box-shadow:0 20px 55px rgba(0,0,0,.25)}",
    ".launcher-icon,.avatar{display:grid;place-items:center;width:39px;height:39px;border-radius:50%;color:var(--accent);background:white}",
    ".bubble{position:relative;width:18px;height:14px;border:2px solid currentColor;border-radius:5px}",
    ".bubble:after{content:'';position:absolute;left:3px;bottom:-5px;width:6px;height:6px;border-left:2px solid currentColor;border-bottom:2px solid currentColor;background:white;transform:skewY(-35deg)}",
    ".launcher{max-width:calc(100dvw - 48px);font-family:var(--control-font)}.launcher strong{display:block;overflow:hidden;font-size:14px;text-overflow:ellipsis;white-space:nowrap}.launcher small{display:block;margin-top:2px;font-size:11px;opacity:.82}",
    ".panel{position:fixed;left:24px;bottom:24px;z-index:2147483001;display:none;width:min(420px,calc(100dvw - 48px));height:min(700px,calc(100dvh - 48px));max-height:calc(100dvh - 48px);overflow:hidden;border:1px solid rgba(0,0,0,.08);border-radius:24px;background:white;box-shadow:0 24px 70px rgba(0,0,0,.25)}",
    ".panel.open{display:grid;grid-template-rows:auto 1fr auto}",
    ".head{display:flex;align-items:center;justify-content:space-between;gap:10px;border-bottom:3px solid var(--accent);padding:14px 15px;color:white;background:var(--header);font-family:var(--control-font)}",
    ".identity{display:flex;flex:1 1 auto;align-items:center;gap:10px;width:0;min-width:0;overflow:hidden}.identity>span:last-child{min-width:0}.identity strong{display:block;overflow:hidden;font-size:15px;text-overflow:ellipsis;white-space:nowrap}.identity small{display:block;overflow:hidden;margin-top:2px;font-size:11px;opacity:.82;text-overflow:ellipsis;white-space:nowrap}",
    ".head-actions{display:flex;flex:0 0 auto;gap:6px}.head button{border:1px solid rgba(255,255,255,.25);border-radius:999px;color:white;background:rgba(255,255,255,.1)}",
    ".home{padding:8px 11px;font-size:12px;font-weight:800}.close{width:36px;height:36px;font-size:19px}",
    ".conversation{overflow-y:auto;padding:15px;background:#faf9f7}",
    ".message{max-width:89%;margin:0 0 11px;border-radius:16px;padding:12px 14px;color:var(--ink);background:white;box-shadow:0 6px 18px rgba(0,0,0,.06);font-size:14.5px;line-height:1.52;white-space:pre-line}",
    ".message.user{margin-left:auto;border-bottom-right-radius:5px;color:white;background:var(--accent)}",
    ".choices{display:flex;flex-wrap:wrap;gap:7px;margin:3px 0 14px}",
    ".choice{display:inline-flex;align-items:center;border:1px solid color-mix(in srgb,var(--accent) 30%,white);border-radius:999px;padding:10px 12px;color:var(--accent-dark);background:white;font-family:var(--control-font);font-size:13.5px;font-weight:750;line-height:1.3;text-decoration:none}",
    ".choice:hover{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 7%,white)}",
    ".form{margin:4px 0 14px;border:1px solid #e4e0d8;border-radius:16px;padding:12px;background:white;box-shadow:0 6px 18px rgba(0,0,0,.05)}",
    ".form-note{margin:0 0 10px;color:#6b7280;font-size:12.5px;line-height:1.45}.form-note strong{color:var(--ink)}",
    ".grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.form label{display:block;color:var(--ink);font-family:var(--control-font);font-size:11.5px;font-weight:800}",
    ".form input{display:block;width:100%;margin-top:4px;border:1px solid #d8d3ca;border-radius:10px;padding:11px;color:var(--ink);background:#fffdf9;font-size:14px}",
    ".form button{width:100%;margin-top:9px;border:0;border-radius:10px;padding:12px;color:white;background:var(--accent);font-family:var(--control-font);font-size:13.5px;font-weight:850}",
    ".consent{display:flex!important;align-items:flex-start;gap:9px;margin-top:10px!important;font-family:var(--control-font);font-size:11.5px!important;font-weight:600!important;line-height:1.45}.consent input{flex:0 0 18px;width:18px;height:18px;margin:1px 0 0;accent-color:var(--accent)}.form-error{display:none;margin:9px 0 0;color:#a32620;font-size:12px;font-weight:700}.secure-note{display:flex;align-items:center;gap:6px;margin:9px 0 0;color:#667085;font-size:11px;line-height:1.4}.turnstile-slot{min-height:65px;margin-top:9px;overflow:hidden}.live-success{border:1px solid color-mix(in srgb,var(--accent) 35%,white);border-radius:16px;padding:15px;color:var(--ink);background:var(--soft);font-size:13px;line-height:1.55}.live-success>strong{display:block;margin-bottom:7px;font-family:var(--control-font);font-size:17px}.live-success p{margin:7px 0}",
    ".multi-list{display:grid;gap:7px;margin:10px 0}.form label.multi-option{display:flex;align-items:center;gap:10px;border:1px solid #e4e0d8;border-radius:11px;padding:11px;color:var(--ink);background:#fffdf9;font-family:var(--control-font);font-size:14px;font-weight:700;line-height:1.35}.multi-option input{flex:0 0 18px;width:18px;height:18px;margin:0;accent-color:var(--accent)}.multi-option span{display:block;flex:1;font-size:14px}.multi-actions{display:grid;grid-template-columns:1fr 1fr;gap:7px}.multi-actions button{margin-top:0}.multi-actions .select-all{border:1px solid color-mix(in srgb,var(--accent) 35%,white);color:var(--accent-dark);background:white}",
    ".break{margin:14px 0;border:2px solid #17181a;border-radius:18px;padding:15px;color:#f7f7f7;background:#303236;box-shadow:0 12px 28px rgba(0,0,0,.2);text-align:center}",
    ".break strong{display:inline-block;margin-top:-28px;border:1px solid #45484d;border-radius:999px;padding:6px 11px;color:white;background:#111214;font-size:11px;letter-spacing:.04em;text-transform:uppercase}.break p{margin:10px 0 0;color:#e4e5e7;font-size:12.5px;line-height:1.5}",
    ".mail-heading{display:flex;justify-content:center;margin:-1px 0 12px}.mail-heading strong{display:inline-flex;align-items:center;justify-content:center;border:1px solid #45484d;border-radius:999px;padding:8px 13px;color:white;background:#111214;font-family:var(--control-font);font-size:11px;font-weight:850;letter-spacing:.04em;line-height:1.2;text-align:center;text-transform:uppercase}",
    ".summary,.delivery{margin:0 0 12px;border:1px solid color-mix(in srgb,var(--accent-dark) 40%,white);border-radius:16px;padding:13px;color:var(--ink);background:var(--soft);font-size:12.5px;line-height:1.6}",
    ".summary>strong,.delivery>strong{display:block;margin-bottom:7px;font-family:", config.theme.headingFont, ";font-size:17px}",
    ".mail{margin-top:10px;border:1px solid rgba(0,0,0,.1);border-radius:12px;padding:11px;background:white}.mail b{display:block;margin-bottom:5px}",
    ".badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}.badges span{border-radius:999px;padding:5px 7px;background:white;font-size:10px;font-weight:800}",
    ".score{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:9px;border-radius:11px;padding:9px;background:white}.score b{display:inline-flex;min-height:28px;align-items:center;justify-content:center;border-radius:999px;padding:6px 11px;color:white;font-size:10px;line-height:1;letter-spacing:.03em;text-align:center;text-transform:uppercase;white-space:nowrap}.score b.score-hot{background:#c7352d}.score b.score-warm{background:#dc7a16}.score b.score-cold{background:#2563a9}",
    ".htags{position:relative;overflow:hidden;margin:14px 0;border-radius:18px;padding:16px;color:white;background:#283270;box-shadow:0 14px 34px rgba(40,50,112,.24)}",
    ".htags:after{content:'#';position:absolute;right:-8px;top:-34px;color:rgba(255,255,255,.07);font:110px Impact,sans-serif;transform:rotate(8deg)}",
    ".htags h3{position:relative;z-index:1;margin:0;font:700 19px/1.08 Kanit,Arial,sans-serif;text-transform:uppercase}.htags p{position:relative;z-index:1;margin:9px 0 12px;color:rgba(255,255,255,.84);font:12.5px/1.5 Arial,sans-serif}",
    ".cta,.restart{position:relative;z-index:1;display:block;width:100%;border-radius:11px;padding:12px;text-align:center;text-decoration:none;font:700 13.5px Kanit,Arial,sans-serif;text-transform:uppercase}",
    ".cta{border:0;color:white;background:#e94a60}.restart{margin-top:7px;border:1px solid rgba(255,255,255,.28);color:white;background:transparent}",
    ".foot{border-top:1px solid #ece8e1;padding:10px;color:#667085;background:white;text-align:center;font-size:10.5px}",
    "@media(max-width:900px){.panel{height:min(680px,calc(100dvh - 32px));max-height:calc(100dvh - 32px);bottom:16px}.message{font-size:15px}.choice{font-size:14px}}",
    "@media(max-width:620px){.launcher{left:max(12px,env(safe-area-inset-left));right:max(12px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));width:max-content;max-width:calc(100dvw - 24px);padding-right:13px}.panel{inset:max(8px,env(safe-area-inset-top)) max(8px,env(safe-area-inset-right)) max(8px,env(safe-area-inset-bottom)) max(8px,env(safe-area-inset-left));width:auto;height:auto;max-width:none;max-height:none;border-radius:18px}.head{padding:12px}.avatar{width:35px;height:35px}.identity strong{font-size:14px}.identity small{font-size:10.5px}.head-actions{gap:4px}.home{padding:7px 9px}.close{width:34px;height:34px}.conversation{padding:12px}.message{max-width:94%;font-size:15px}.choice{font-size:14px}.form input{font-size:16px}.grid{grid-template-columns:1fr}}"
  ].join("");

  var isRealAssistant = Boolean(config.realLive);
  var launcherStatus = isRealAssistant ? "Réponse immédiate" : "Réponse immédiate · Démo";
  var headerStatus = isRealAssistant ? "En ligne" : "En ligne · Simulation interactive";
  var footerText = isRealAssistant ? "Vos informations sont sécurisées et transmises uniquement à Richard DJ." : "Démonstration : aucune donnée n’est collectée.";

  root.innerHTML =
    "<style>" + css + "</style>" +
    "<button class='launcher' aria-label='" + (isRealAssistant ? "Ouvrir l’assistant Richard DJ" : "Ouvrir la démonstration") + "'>" +
      "<span class='launcher-icon'><span class='bubble'></span></span>" +
      "<span><strong>" + escapeHtml(config.launcher) + "</strong><small>" + launcherStatus + "</small></span>" +
    "</button>" +
    "<aside class='panel' aria-label='" + (isRealAssistant ? "Assistant Richard DJ" : "Démonstration de l’assistant") + "'>" +
      "<header class='head'>" +
        "<div class='identity'><span class='avatar'><span class='bubble'></span></span><span><strong>" + escapeHtml(config.name) + "</strong><small>" + headerStatus + "</small></span></div>" +
        "<div class='head-actions'><button class='home' type='button'>Menu principal</button><button class='close' type='button' aria-label='Fermer'>×</button></div>" +
      "</header>" +
      "<div class='conversation' aria-live='polite'></div>" +
      "<footer class='foot'>" + footerText + "</footer>" +
    "</aside>";

  var launcher = root.querySelector(".launcher");
  var panel = root.querySelector(".panel");
  var conversation = root.querySelector(".conversation");

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function scrollEnd() {
    conversation.scrollTop = conversation.scrollHeight;
  }

  function addMessage(text, kind) {
    var item = document.createElement("div");
    item.className = "message" + (kind === "user" ? " user" : "");
    item.textContent = text;
    conversation.appendChild(item);
    scrollEnd();
  }

  function addChoices(items, key, isInfo, allowMenuShortcut) {
    var group = document.createElement("div");
    group.className = "choices";
    var choices = items.slice();
    if (!isRealAssistant && isInfo && !choices.some(function (choice) { return choice[1] === "demo_end"; })) {
      choices.push(["Terminer la démonstration", "demo_end"]);
    }
    if (
      isRealAssistant &&
      allowMenuShortcut !== false &&
      !choices.some(function (choice) { return choice[1] === "start"; })
    ) {
      choices.push(["Revenir au menu principal", "start"]);
    }

    choices.forEach(function (choice) {
      var label = choice[0];
      var next = choice[1];
      var answerValue = choice[2];
      var answerKey = choice[3] || key;
      var isWeb = next.indexOf("http") === 0;
      var isProtocol = /^(tel:|mailto:)/.test(next);
      var control = document.createElement(isWeb ? "a" : "button");
      control.className = "choice";
      control.textContent = label;

      if (isWeb) {
        control.href = next;
        control.target = "_blank";
        control.rel = "noopener";
      } else if (isProtocol) {
        control.type = "button";
        control.addEventListener("click", function () {
          group.remove();
          addMessage(label, "user");
          var destination = next.replace(/^tel:|^mailto:/, "");
          if (isRealAssistant) {
            addMessage(
              next.indexOf("tel:") === 0
                ? "L’appel vers " + destination + " va s’ouvrir sur votre appareil."
                : "Votre messagerie va s’ouvrir avec l’adresse " + destination + " préremplie."
            );
            addChoices([["Revenir au menu principal", "start"]]);
            window.location.href = next;
            return;
          }
          addMessage(
            next.indexOf("tel:") === 0
              ? "Sur un téléphone, l’appel vers " + destination + " s’ouvrirait automatiquement. Aucun appel réel n’est lancé dans cette démonstration."
              : "Votre messagerie s’ouvrirait avec l’adresse " + destination + " préremplie. Aucun e-mail réel n’est envoyé dans cette démonstration."
          );
          var followups;
          if (config.name.indexOf("Yoga") !== -1) {
            followups = [["Être rappelé pour des renseignements", "callback"], ["Revenir au menu principal", "start"], ["Terminer la démonstration", "demo_end"]];
          } else if (config.name.indexOf("Le Gourmet") !== -1) {
            followups = [["Réserver une table", "service"], ["Revenir au menu principal", "start"], ["Terminer la démonstration", "demo_end"]];
          } else if (config.name.indexOf("Baiona Immo") !== -1) {
            followups = [["Être rappelé par un conseiller", "callback"], ["Revenir au menu principal", "start"], ["Terminer la démonstration", "demo_end"]];
          } else if (config.name.indexOf("Richard DJ") !== -1) {
            followups = [["Préparer mon mariage", "dj_project_date"], ["Revenir au menu principal", "start"], ["Terminer la démonstration", "demo_end"]];
          } else {
            followups = [["Être rappelé", "callback"], ["Revenir au menu principal", "start"], ["Terminer la démonstration", "demo_end"]];
          }
          addChoices(followups);
        });
      } else {
        control.type = "button";
        control.addEventListener("click", function () {
          group.remove();
          addMessage(label, "user");
          if (answerKey) answers[answerKey] = answerValue || label;
          if (next === "start") return reset();
          go(next);
        });
      }
      group.appendChild(control);
    });
    conversation.appendChild(group);
    scrollEnd();
  }

  function go(id) {
    if (id === "guests") return showGuests();
    if (id === "date") return showDate();
    if (id === "time") return showTime();
    if (id === "event_other") return showEventOther();
    if (id === "contact") return showContact("booking");
    if (id === "callback") return showContact("callback");
    if (id === "summary") return showSummary();
    if (id === "demo_end") return showDemoEnd();
    if (id === "menu_choice" && answers.menu) return showContact("booking");

    var step = config.steps[id];
    if (!step) return reset();
    if (step.multi) return showMulti(step);
    if (step.input) return showInput(step);
    if (step.dateInput) return showDateInput(step);
    window.setTimeout(function () {
      addMessage(step.message);
      addChoices(step.choices || [], step.key, step.info, id !== config.start);
    }, 180);
  }

  function formShell(label, inputHtml, buttonLabel) {
    var form = document.createElement("form");
    form.className = "form";
    form.innerHTML = "<label>" + label + inputHtml + "</label><button type='submit'>" + buttonLabel + "</button>";
    conversation.appendChild(form);
    scrollEnd();
    return form;
  }

  function showMulti(step) {
    window.setTimeout(function () {
      addMessage(step.message);
      var form = document.createElement("form");
      form.className = "form";
      var options = (step.choices || []).map(function (label) {
        return "<label class='multi-option'><input type='checkbox' name='items' value='" +
          escapeHtml(label) + "'><span>" + escapeHtml(label) + "</span></label>";
      }).join("");
      form.innerHTML =
        "<p class='form-note'><strong>Plusieurs réponses possibles.</strong><br>Vous pouvez également tout sélectionner en un clic.</p>" +
        "<div class='multi-list'>" + options + "</div>" +
        "<div class='multi-actions'><button class='select-all' type='button'>Tout sélectionner</button><button type='submit'>" +
        escapeHtml(step.buttonLabel || "Valider mes choix") + "</button></div>";
      var selectAll = form.querySelector(".select-all");
      selectAll.addEventListener("click", function () {
        var boxes = Array.from(form.querySelectorAll("input[type='checkbox']"));
        var shouldSelect = boxes.some(function (box) { return !box.checked; });
        boxes.forEach(function (box) { box.checked = shouldSelect; });
        selectAll.textContent = shouldSelect ? "Tout désélectionner" : "Tout sélectionner";
      });
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var selected = Array.from(form.querySelectorAll("input[type='checkbox']:checked"))
          .map(function (box) { return box.value; });
        if (!selected.length) return;
        answers[step.key] = selected.join(", ");
        form.remove();
        addMessage(selected.join(" · "), "user");
        go(step.next);
      });
      conversation.appendChild(form);
      scrollEnd();
    }, 180);
  }

  function showInput(step) {
    window.setTimeout(function () {
      addMessage(step.message);
      var type = step.input.type || "text";
      var attributes = " type='" + escapeHtml(type) + "' name='value' required";
      if (step.input.placeholder) attributes += " placeholder='" + escapeHtml(step.input.placeholder) + "'";
      if (step.input.min != null) attributes += " min='" + escapeHtml(step.input.min) + "'";
      if (step.input.max != null) attributes += " max='" + escapeHtml(step.input.max) + "'";
      if (step.input.maxlength != null) attributes += " maxlength='" + escapeHtml(step.input.maxlength) + "'";
      var form = formShell(
        escapeHtml(step.input.label),
        "<input" + attributes + ">",
        escapeHtml(step.input.buttonLabel || "Valider")
      );
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = String(form.elements.value.value || "").trim();
        if (!value) return;
        var display = value + (step.input.suffix || "");
        answers[step.key] = display;
        form.remove();
        addMessage(display, "user");
        go(step.next);
      });
    }, 180);
  }

  function showDateInput(step) {
    window.setTimeout(function () {
      addMessage(step.message);
      var now = new Date();
      var suggested = new Date(now);
      suggested.setDate(now.getDate() + 30);
      var form = formShell(
        escapeHtml(step.label || "Date souhaitée"),
        "<input name='value' type='date' min='" + localDate(now) + "' value='" + localDate(suggested) + "' required>",
        escapeHtml(step.buttonLabel || "Valider cette date")
      );
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = form.elements.value.value;
        if (!value) return;
        var formatted = new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" })
          .format(new Date(value + "T12:00:00Z"));
        answers[step.key || "date"] = formatted.charAt(0).toUpperCase() + formatted.slice(1);
        form.remove();
        addMessage(answers[step.key || "date"], "user");
        go(step.next);
      });
    }, 180);
  }

  function showGuests() {
    window.setTimeout(function () {
      addMessage("Pour combien de personnes souhaitez-vous réserver ?");
      var form = formShell("Nombre de personnes", "<input name='value' type='number' min='1' max='30' placeholder='Ex. : 2' required>", "Valider");
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var count = parseInt(form.elements.value.value, 10);
        if (!Number.isInteger(count) || count < 1 || count > 30) return;
        answers.guests = count + (count === 1 ? " personne" : " personnes");
        form.remove();
        addMessage(answers.guests, "user");
        go("date");
      });
    }, 180);
  }

  function localDate(date) {
    var shifted = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
    return shifted.toISOString().slice(0, 10);
  }

  function showDate() {
    window.setTimeout(function () {
      var yoga = config.name.indexOf("Yoga") !== -1;
      addMessage(yoga ? "Choisissez la date à laquelle vous aimeriez découvrir le studio." : "Choisissez maintenant la date souhaitée.");
      var now = new Date();
      var suggested = new Date(now);
      suggested.setDate(now.getDate() + 7);
      var form = formShell(
        yoga ? "Date souhaitée pour la découverte" : "Date de la réservation",
        "<input name='value' type='date' min='" + localDate(now) + "' value='" + localDate(suggested) + "' required>",
        "Valider cette date"
      );
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = form.elements.value.value;
        if (!value) return;
        var formatted = new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "UTC" })
          .format(new Date(value + "T12:00:00Z"));
        answers.date = formatted.charAt(0).toUpperCase() + formatted.slice(1);
        form.remove();
        addMessage(answers.date, "user");
        showTime();
      });
    }, 180);
  }

  function showTime() {
    window.setTimeout(function () {
      var yoga = config.name.indexOf("Yoga") !== -1;
      addMessage(yoga ? "À quelle heure souhaiteriez-vous découvrir le studio ?" : "À quelle heure souhaitez-vous réserver ?");
      var form = formShell(
        yoga ? "Heure souhaitée pour la découverte" : "Heure de la réservation",
        "<input name='value' type='time' required>",
        "Valider cette heure"
      );
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = form.elements.value.value;
        if (!value) return;
        answers.time = value.replace(":", " h ");
        form.remove();
        addMessage(answers.time, "user");
        if (yoga) {
          addMessage("Pour finaliser ce rendez-vous découverte, le studio peut vous rappeler directement.");
          addChoices([["Être rappelé pour finaliser", "callback"], ["Voir les coordonnées", "contact_info"]]);
        } else {
          go("event");
        }
      });
    }, 180);
  }

  function showEventOther() {
    window.setTimeout(function () {
      addMessage("Précisez la nature de l’événement.");
      var form = formShell("Votre événement", "<input name='value' type='text' maxlength='80' placeholder='Ex. : demande en mariage' required>", "Valider l’événement");
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var value = form.elements.value.value.trim();
        if (!value) return;
        answers.event = value;
        form.remove();
        addMessage(value, "user");
        go("menu_choice");
      });
    }, 180);
  }

  function showContact(mode) {
    window.setTimeout(function () {
      if (config.realPreview || config.realLive) {
        addMessage(mode === "callback"
          ? "Pour que Richard puisse vous rappeler, indiquez vos coordonnées."
          : "Dernière étape : indiquez vos coordonnées pour transmettre votre demande à Richard.");
        var realForm = document.createElement("form");
        var turnstileToken = "";
        var turnstileWidgetId = null;
        realForm.className = "form";
        realForm.innerHTML =
          "<p class='form-note'><strong>Vos coordonnées</strong><br>Les champs marqués d’un astérisque sont obligatoires.</p>" +
          "<div class='grid'>" +
            "<label>Prénom *<input name='firstName' autocomplete='given-name' required></label>" +
            "<label>Nom *<input name='lastName' autocomplete='family-name' required></label>" +
            "<label>E-mail *<input name='email' type='email' autocomplete='email' required></label>" +
            "<label>Téléphone *<input name='phone' type='tel' inputmode='tel' autocomplete='tel' required></label>" +
          "</div>" +
          "<label class='consent'><input name='consent' type='checkbox' required><span>J’accepte que mes informations soient utilisées par Richard DJ Event pour répondre à ma demande.</span></label>" +
          (config.realLive ? "<div class='turnstile-slot'></div>" : "") +
          "<p class='secure-note'>🔒 Protection antispam Cloudflare Turnstile.</p>" +
          "<p class='form-error'>Vérifiez vos coordonnées et acceptez l’utilisation de vos informations.</p>" +
          "<button type='submit'>" + (mode === "callback" ? "Demander à être rappelé" : "Envoyer ma demande") + "</button>";
        realForm.addEventListener("submit", async function (event) {
          event.preventDefault();
          var firstName = realForm.elements.firstName.value.trim();
          var lastName = realForm.elements.lastName.value.trim();
          var email = realForm.elements.email.value.trim();
          var phone = realForm.elements.phone.value.trim();
          var phoneDigits = phone.replace(/\D/g, "");
          if (!firstName || !lastName || !email.includes("@") || phoneDigits.length < 10 || !realForm.elements.consent.checked) {
            realForm.querySelector(".form-error").style.display = "block";
            return;
          }
          if (config.realLive && !turnstileToken) {
            var captchaError = realForm.querySelector(".form-error");
            captchaError.textContent = "Veuillez valider la protection antispam avant l’envoi.";
            captchaError.style.display = "block";
            return;
          }
          answers.firstName = firstName;
          answers.lastName = lastName;
          answers.email = email;
          answers.phone = phone;

          if (config.realLive) {
            var submitButton = realForm.querySelector("button[type='submit']");
            submitButton.disabled = true;
            submitButton.textContent = "Envoi en cours…";
            realForm.querySelector(".form-error").style.display = "none";
            try {
              var fields = config.fieldsByIntent && config.fieldsByIntent[answers.intent]
                ? config.fieldsByIntent[answers.intent]
                : [];
              var details = fields.map(function (field) {
                return field[0] + " : " + (answers[field[1]] || "À préciser");
              });
              var scoreContainer = document.createElement("div");
              scoreContainer.innerHTML = config.qualify && mode !== "callback" ? scoreMarkup() : "";
              var scoreLabel = scoreContainer.querySelector(".score b");
              var scoreReason = scoreContainer.querySelector(".score span");
              var messageLines = [
                "Nouvelle demande depuis l’assistant Richard DJ",
                "",
                "Contact : " + firstName + " " + lastName,
                "E-mail : " + email,
                "Téléphone : " + phone,
                mode === "callback" ? "Demande : rappel par Richard" : "",
                ...details,
                scoreLabel ? "Qualification : " + scoreLabel.textContent : "",
                scoreReason ? "Analyse : " + scoreReason.textContent.replace("Qualification automatique", "").trim() : "",
              ].filter(Boolean);
              var payload = new FormData();
              payload.append("subject", config.mailSubject || "Nouvelle demande via l’assistant Richard DJ");
              payload.append("botcheck", "");
              payload.append("prenom", firstName);
              payload.append("nom", lastName);
              payload.append("email", email);
              payload.append("telephone", phone);
              payload.append("date", answers.date || "");
              payload.append("lieu", answers.venue || answers.location || "");
              payload.append("message", messageLines.join("\n"));
              payload.append("cf-turnstile-response", turnstileToken);
              var captchaPayload = new FormData();
              captchaPayload.append("cf-turnstile-response", turnstileToken);
              var captchaResponse = await fetch("/api/contact/verify", {
                method: "POST",
                headers: { Accept: "application/json" },
                body: captchaPayload,
              });
              var captchaResult = await captchaResponse.json();
              if (!captchaResponse.ok || !captchaResult.success) throw new Error(captchaResult.message || "Captcha refusé");
              payload.delete("cf-turnstile-response");
              payload.delete("botcheck");
              payload.append("access_key", "3f6d1840-64d1-4521-bb72-95d8b95071e5");
              payload.append("from_name", "Assistant Richard DJ");
              payload.append("name", firstName + " " + lastName);
              var response = await fetch("https://api.web3forms.com/submit", {
                method: "POST",
                headers: { Accept: "application/json" },
                body: payload,
              });
              var result = await response.json();
              if (!response.ok || !result.success) throw new Error(result.message || "Envoi impossible");
              realForm.remove();
              addMessage(firstName + " " + lastName + " · Coordonnées transmises", "user");
              showRealSuccess(mode);
              return;
            } catch (error) {
              var sendError = realForm.querySelector(".form-error");
              sendError.textContent = "L’envoi n’a pas abouti. Réessayez ou contactez Richard directement.";
              sendError.style.display = "block";
              submitButton.disabled = false;
              submitButton.textContent = mode === "callback" ? "Demander à être rappelé" : "Envoyer ma demande";
              turnstileToken = "";
              if (window.turnstile && turnstileWidgetId !== null) window.turnstile.reset(turnstileWidgetId);
              return;
            }
          }

          realForm.remove();
          addMessage(firstName + " " + lastName + " · Coordonnées renseignées", "user");
          showRealPreviewOutcome(mode);
        });
        conversation.appendChild(realForm);
        if (config.realLive) {
          renderTurnstile(realForm.querySelector(".turnstile-slot"), function (token, widgetId) {
            turnstileToken = token;
            if (widgetId !== undefined) turnstileWidgetId = widgetId;
          });
        }
        scrollEnd();
        return;
      }

      addMessage(mode === "callback"
        ? "Pour organiser votre rappel, voici les coordonnées fictives utilisées dans la simulation."
        : "Dernière étape : voici les coordonnées fictives utilisées dans la simulation.");
      var form = document.createElement("form");
      form.className = "form";
      form.innerHTML =
        "<p class='form-note'><strong>Coordonnées fictives préremplies.</strong><br>Rien ne sera enregistré ni transmis.</p>" +
        "<div class='grid'>" +
          "<label>Prénom<input name='firstName' value='Camille' readonly></label>" +
          "<label>Nom<input name='lastName' value='Martin' readonly></label>" +
          "<label>E-mail<input name='email' value='camille@exemple.fr' readonly></label>" +
          "<label>Téléphone<input name='phone' value='06 00 00 00 00' readonly></label>" +
        "</div><button type='submit'>" + (mode === "callback" ? "Demander mon rappel" : "Envoyer ma demande") + "</button>";
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        answers.firstName = "Camille";
        answers.lastName = "Martin";
        answers.email = "camille@exemple.fr";
        answers.phone = "06 00 00 00 00";
        form.remove();
        addMessage("Camille Martin · Coordonnées renseignées", "user");
        mode === "callback" ? showCallbackOutcome() : showSummary();
      });
      conversation.appendChild(form);
      scrollEnd();
    }, 180);
  }

  function showRealPreviewOutcome(mode) {
    window.setTimeout(function () {
      addBreak("Préproduction : les informations saisies restent uniquement dans votre navigateur et aucune demande n’a été envoyée à Richard.");
      var fields = config.fieldsByIntent && config.fieldsByIntent[answers.intent]
        ? config.fieldsByIntent[answers.intent]
        : [];
      var lines = fields.map(function (field) {
        return escapeHtml(field[0]) + " : " + escapeHtml(answers[field[1]] || "À préciser");
      }).join("<br>");
      var item = document.createElement("div");
      item.className = "summary";
      item.innerHTML =
        "<strong>" + (mode === "callback" ? "Demande de rappel prête" : "Votre demande est prête") + "</strong>" +
        escapeHtml(answers.firstName + " " + answers.lastName) + "<br>" +
        escapeHtml(answers.email) + " · " + escapeHtml(answers.phone) +
        (lines ? "<div class='mail'><b>" + escapeHtml(config.mailSubject || "Nouvelle demande") + "</b>" + lines + "</div>" : "") +
        (config.qualify && mode !== "callback" ? scoreMarkup() : "") +
        "<div class='badges'><span>✓ Consentement recueilli</span><span>✓ Envoi sécurisé prévu</span><span>✓ Réponse sous 24 h</span></div>";
      conversation.appendChild(item);
      addMessage("Une fois activée, cette demande sera envoyée immédiatement à Richard. Il pourra ensuite vous répondre par e-mail ou vous rappeler.");
      addChoices([["Recommencer le parcours", "start"]]);
    }, 180);
  }

  function renderTurnstile(container, onToken) {
    var attempts = 0;
    var timer = window.setInterval(function () {
      attempts += 1;
      if (window.turnstile && typeof window.turnstile.render === "function") {
        window.clearInterval(timer);
        var widgetId = window.turnstile.render(container, {
          sitekey: config.turnstileSiteKey,
          theme: "dark",
          language: "fr",
          callback: function (token) { onToken(token, widgetId); },
          "expired-callback": function () { onToken("", widgetId); },
          "error-callback": function () { onToken("", widgetId); },
        });
        onToken("", widgetId);
      } else if (attempts > 40) {
        window.clearInterval(timer);
        var error = document.createElement("p");
        error.className = "form-error";
        error.style.display = "block";
        error.textContent = "La protection antispam n’a pas pu se charger. Rechargez la page.";
        container.appendChild(error);
      }
    }, 250);
  }

  function showRealSuccess(mode) {
    window.setTimeout(function () {
      var item = document.createElement("div");
      item.className = "live-success";
      item.innerHTML =
        "<strong>Votre demande a bien été envoyée</strong>" +
        "<p>Merci " + escapeHtml(answers.firstName) + ". Richard a reçu votre " +
        (mode === "callback" ? "demande de rappel" : "projet de mariage") +
        " et vous répondra sous 24 h.</p>" +
        "<div class='badges'><span>✓ Envoi sécurisé</span><span>✓ Richard prévenu</span><span>✓ Réponse sous 24 h</span></div>";
      conversation.appendChild(item);
      addChoices([
        ["Revenir au menu principal", "start"],
        ["Appeler Richard", "tel:+33684331824"],
      ]);
      scrollEnd();
    }, 180);
  }

  function addBreak(text) {
    var item = document.createElement("div");
    item.className = "break";
    item.innerHTML = "<strong>Fin de la simulation</strong><p>" + escapeHtml(text) + "</p>";
    conversation.appendChild(item);
  }

  function addMailHeading() {
    var item = document.createElement("div");
    item.className = "mail-heading";
    item.innerHTML = "<strong>Ce que vous recevez par mail</strong>";
    conversation.appendChild(item);
  }

  function addHtags() {
    if (isRealAssistant) return;
    var item = document.createElement("div");
    item.className = "htags";
    item.innerHTML =
      "<h3>" + escapeHtml(config.ctaTitle) + "</h3>" +
      "<p>" + escapeHtml(config.ctaText) + "</p>" +
      "<a class='cta' href='" + escapeHtml(config.ctaHref) + "' target='_blank' rel='noopener'>" + escapeHtml(config.ctaLabel) + " →</a>" +
      "<button class='restart' type='button'>↻ Recommencer la démo</button>";
    item.querySelector(".restart").addEventListener("click", reset);
    conversation.appendChild(item);
    scrollEnd();
  }

  function showDemoEnd() {
    if (isRealAssistant) return reset();
    window.setTimeout(function () {
      addBreak("Vous venez de tester une fonctionnalité de l’assistant. Aucune donnée personnelle n’a été collectée.");
      addHtags();
    }, 180);
  }

  function scoreMarkup() {
    var label = "Prospect froid";
    var reason = "Visiteur en phase de renseignement";

    if (config.qualificationMode === "dj") {
      var djPoints = 0;
      var djStages = {
        "Oui, la date et le lieu sont confirmés": 2,
        "La date et le lieu sont confirmés": 4,
        "La date est confirmée, le lieu reste à choisir": 3,
        "La date est encore flexible": 0,
        "L’organisation est en cours": 1,
        "Je prends simplement des renseignements": 0
      };
      var djSearchStages = {
        "Je commence mes recherches": 0,
        "Je compare plusieurs DJ": 1,
        "J’ai déjà reçu un ou plusieurs devis": 2,
        "Notre choix est presque arrêté": 3,
        "Nous devons remplacer un DJ devenu indisponible": 4
      };
      djPoints += djStages[answers.projectStage] || 0;
      djPoints += djSearchStages[answers.djSearchStatus] || 0;

      if (answers.intent !== "Demande de disponibilité") {
        if (answers.date) djPoints += 1;
        if (answers.location) djPoints += 1;
        if (answers.moments && answers.moments.indexOf("Soirée dansante") !== -1) djPoints += 1;
      }

      var urgentDj = answers.djSearchStatus === "Nous devons remplacer un DJ devenu indisponible";
      var hotDj = urgentDj || djPoints >= 5;
      var warmDj = djPoints >= 2;

      if (hotDj) {
        label = "Prospect chaud";
        reason = urgentDj
          ? "Recherche urgente pour remplacer un DJ indisponible"
          : "Date précise et recherche de DJ suffisamment avancée";
      } else if (warmDj) {
        label = "Prospect tiède";
        reason = answers.intent === "Demande de disponibilité"
          ? "Date ou lieu confirmé, recherche de DJ encore en cours"
          : "Projet réel, encore en cours d’organisation";
      } else {
        reason = "Première prise de renseignements sur la prestation";
      }
    } else if (config.qualificationMode === "immobilier") {
      var points = 0;
      var activeStages = {
        "Je visite déjà des biens": 3,
        "Ma recherche est active": 2,
        "Je définis mes critères": 1,
        "La décision de vendre est prise": 3,
        "Je souhaite d’abord une estimation": 2,
        "Je compare plusieurs agences": 1,
        "Je souhaite lancer rapidement l’étude": 3,
        "Je veux vérifier la faisabilité": 2,
        "Je compare plusieurs solutions": 1
      };
      var financingScores = {
        "Financement validé": 3,
        "Achat sans financement": 3,
        "Accord de principe obtenu": 2,
        "Démarches en cours": 1
      };
      points += activeStages[answers.projectStage] || 0;
      points += financingScores[answers.financing] || 0;
      if (answers.date === "Dès que possible" || answers.date === "Dans 1 à 3 mois") points += 2;
      else if (answers.date === "Dans 3 à 6 mois") points += 1;

      var hotThreshold = answers.intent === "Vendre ou faire estimer" ? 5 : 6;
      if (points >= hotThreshold) {
        label = "Prospect chaud";
        reason = answers.intent === "Vendre ou faire estimer"
          ? "Décision avancée et calendrier de vente proche"
          : "Recherche active, financement avancé et délai court";
      } else if (points >= 3) {
        label = "Prospect tiède";
        reason = "Projet réel mais encore en cours de préparation";
      } else {
        reason = "Projet immobilier encore en phase de réflexion";
      }
    } else if (answers.date === "Dès que possible" || answers.date === "Dans 1 à 3 mois") {
      label = "Prospect chaud";
      reason = "Projet précis, délai court et coordonnées complètes";
    } else if (answers.date === "Dans 3 à 6 mois") {
      label = "Prospect tiède";
      reason = "Projet défini avec une échéance moins immédiate";
    }
    var scoreClass = label === "Prospect chaud"
      ? "score-hot"
      : (label === "Prospect tiède" ? "score-warm" : "score-cold");
    return "<div class='score'><span><strong>Qualification automatique</strong><br>" + escapeHtml(reason) + "</span><b class='" + scoreClass + "'>" + label + "</b></div>";
  }

  function showCallbackOutcome() {
    window.setTimeout(function () {
      var yoga = config.name.indexOf("Yoga") !== -1;
      addBreak("Les coordonnées utilisées sont fictives et n’ont pas été enregistrées. Sur votre landing page, cette demande vous est transmise immédiatement et automatiquement.");
      addMailHeading();
      var context = yoga && answers.date
        ? "Découverte souhaitée : " + answers.date + (answers.time ? " à " + answers.time : "")
        : "Motif et créneau du rappel à confirmer";
      var item = document.createElement("div");
      item.className = "delivery";
      item.innerHTML =
        "<strong>Ce que vous recevez</strong>" +
        "<div class='mail'><b>Camille Martin souhaite être rappelé(e)</b>camille@exemple.fr<br>06 00 00 00 00<br>" + escapeHtml(context) + "</div>" +
        "<div class='badges'><span>✓ " + (yoga ? "Élève identifié" : "Prospect identifié") + "</span><span>✓ E-mail immédiat</span><span>✓ SMS activable</span></div>" +
        (config.qualify ? scoreMarkup() : "");
      conversation.appendChild(item);
      addHtags();
    }, 180);
  }

  function showSummary() {
    window.setTimeout(function () {
      if (config.name.indexOf("Le Gourmet") !== -1) {
        addMessage(
          "Je vous confirme que vous souhaitez réserver le " + (answers.date || "jour à confirmer") +
          " à " + (answers.time || "l’heure à confirmer") + ", pour " + (answers.guests || "un nombre de personnes à confirmer") +
          ". Vous êtes joignable à l’adresse " + answers.email + " et au " + answers.phone +
          ". Pour toute modification ou annulation, merci de nous rappeler au " + config.cancelPhone + "."
        );
      }

      addBreak("Les coordonnées utilisées sont fictives et n’ont pas été enregistrées. Sur votre landing page, cette demande vous est transmise immédiatement et automatiquement.");
      addMailHeading();
      var pathKey = answers.intent + "|" + (answers.saleMode || answers.property || "");
      var fields = config.fieldsByPath && config.fieldsByPath[pathKey]
        ? config.fieldsByPath[pathKey]
        : (config.fieldsByIntent && config.fieldsByIntent[answers.intent]
          ? config.fieldsByIntent[answers.intent]
          : (config.fields || []));
      var lines = fields.map(function (field) {
        return escapeHtml(field[0]) + " : " + escapeHtml(answers[field[1]] || "À préciser");
      }).join("<br>");
      var item = document.createElement("div");
      item.className = "summary";
      item.innerHTML =
        "<strong>" + escapeHtml(config.summaryTitle || "Aperçu de votre demande") + "</strong>" + lines +
        "<div class='mail'><b>" + escapeHtml(config.mailSubject || "Nouvelle demande") + "</b>" +
        "Camille Martin · camille@exemple.fr · 06 00 00 00 00<br>" + lines + "</div>" +
        "<div class='badges'><span>✓ " + escapeHtml(config.identityBadge || "Contact identifié") + "</span><span>✓ E-mail immédiat</span><span>✓ SMS activable</span></div>" +
        (config.qualify ? scoreMarkup() : "");
      conversation.appendChild(item);
      addHtags();
    }, 180);
  }

  function reset() {
    answers = {};
    conversation.innerHTML = "";
    go(config.start);
  }

  function open() {
    panel.classList.add("open");
    launcher.style.display = "none";
    if (!conversation.children.length) reset();
  }

  function close() {
    panel.classList.remove("open");
    launcher.style.display = "flex";
  }

  launcher.addEventListener("click", open);
  root.querySelector(".home").addEventListener("click", reset);
  root.querySelector(".close").addEventListener("click", close);
  if (config.autoOpen) window.setTimeout(open, 700);
})();

    })();
