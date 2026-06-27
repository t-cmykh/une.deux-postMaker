// ──────────────────────────────────────────────────────────
// une·deux — Éphéméride foot quotidienne (brouillon Gmail)
// Google Apps Script — à coller dans script.google.com
// ──────────────────────────────────────────────────────────

// ▸ Remplace par ta clé API Anthropic (https://console.anthropic.com)
const ANTHROPIC_API_KEY = "sk-ant-XXXXXXXXXXXXXXXXXXXXXXXX";

// ▸ Adresse email du brouillon (ton compte Gmail)
const EMAIL_TO = "unedeux.officiel@gmail.com";

// ▸ Modèle Claude à utiliser
const MODEL = "claude-sonnet-4-6";

function creerBrouillonEphemeride() {
  const aujourd_hui = new Date();
  const jour = aujourd_hui.getDate();
  const moisNoms = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
  ];
  const mois = moisNoms[aujourd_hui.getMonth()];
  const annee = aujourd_hui.getFullYear();
  const dateFormatee = jour + " " + mois + " " + annee;

  const prompt = `Tu es l'archiviste-conteur de une·deux, un média foot Instagram qui raconte des histoires méconnues du football.

Aujourd'hui nous sommes le ${dateFormatee}.

Donne-moi les éphémérides football pour le ${jour} ${mois} (tous les ${jour} ${mois} de l'histoire du foot). Liste 5 à 8 événements marquants, méconnus ou surprenants qui se sont passés à cette date.

Pour chaque événement :
- 📅 Année
- ⚽ Ce qui s'est passé (2-3 phrases max, ton une·deux : factuel, surprenant, archiviste)
- 💡 Potentiel post une·deux : note de 1 à 3 (3 = histoire forte, méconnue, parfaite pour un carrousel)

Privilégie :
- Les histoires oubliées, les pionniers, les détails fous
- Les liens avec la Coupe du Monde 2026 (joueurs/équipes concernés)
- Les contradictions, injustices, destins brisés

Termine par "🎯 MA RECOMMANDATION" : l'événement qui ferait le meilleur post une·deux et pourquoi (en 2 lignes).

Format : texte brut lisible dans un email, pas de markdown complexe.`;

  const payload = {
    model: MODEL,
    max_tokens: 1500,
    messages: [{ role: "user", content: prompt }]
  };

  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch("https://api.anthropic.com/v1/messages", options);
  const result = JSON.parse(response.getContentText());

  if (result.error) {
    Logger.log("Erreur API Claude : " + result.error.message);
    return;
  }

  const contenu = result.content[0].text;

  const sujet = "⚽ Éphéméride une·deux — " + dateFormatee;

  const corpsHtml = "<div style='font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; max-width: 600px;'>"
    + "<h2 style='color: #1a1a1a;'>⚽ Éphéméride foot — " + dateFormatee + "</h2>"
    + "<hr style='border: 1px solid #4CAF50;'>"
    + "<pre style='white-space: pre-wrap; font-family: Arial, sans-serif; font-size: 14px;'>"
    + contenu
    + "</pre>"
    + "<hr style='border: 1px solid #4CAF50;'>"
    + "<p style='color: #888; font-size: 12px;'>Généré automatiquement par Claude pour une·deux</p>"
    + "</div>";

  GmailApp.createDraft(EMAIL_TO, sujet, contenu, { htmlBody: corpsHtml });

  Logger.log("Brouillon créé : " + sujet);
}

// ──────────────────────────────────────────────────────────
// INSTALLATION DU TRIGGER (à exécuter UNE SEULE FOIS)
// ──────────────────────────────────────────────────────────
function installerTriggerQuotidien() {
  // Supprime les anciens triggers de cette fonction
  const triggers = ScriptApp.getProjectTriggers();
  for (const trigger of triggers) {
    if (trigger.getHandlerFunction() === "creerBrouillonEphemeride") {
      ScriptApp.deleteTrigger(trigger);
    }
  }

  // Crée un trigger quotidien à 18h (fuseau horaire du projet = Europe/Paris)
  ScriptApp.newTrigger("creerBrouillonEphemeride")
    .timeBased()
    .everyDays(1)
    .atHour(18)
    .nearMinute(0)
    .inTimezone("Europe/Paris")
    .create();

  Logger.log("Trigger quotidien installé : tous les jours à 18h (Paris)");
}
