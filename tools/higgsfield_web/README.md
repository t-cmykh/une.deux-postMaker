# Envoi de prompts Higgsfield (web, mode « Unlimited »)

`send_prompts.py` pilote un vrai Chromium (via **Playwright**) connecté à ton
compte higgsfield.ai, tape chaque prompt, **coche « Unlimited »** et lance la
génération. C'est la seule façon d'utiliser l'option *Unlimited* : elle n'existe
que dans l'app web, pas dans l'API.

> ⚠️ À lancer **sur ta machine** (le script a besoin de ta session connectée).
> Automatiser l'interface web peut être contraire aux **CGU de Higgsfield** —
> tu utilises ton propre plan/entitlement, mais vérifie que c'est autorisé.

## Installation

```bash
pip install playwright
playwright install chromium
```

## 1) Connexion (une seule fois)

```bash
python3 send_prompts.py login
```

Une fenêtre s'ouvre : connecte-toi à Higgsfield, reviens au terminal, appuie sur
Entrée. La session est gardée dans `./hf_profile` (réutilisée ensuite).

## 2) Envoi des prompts

Mets un prompt par ligne dans `prompts.txt`, puis :

```bash
# Vérifie d'abord sans rien lancer (remplit le prompt, ne clique pas Generate)
python3 send_prompts.py run --dry-run

# Pour de vrai
python3 send_prompts.py run --prompts prompts.txt --delay 8
```

Options utiles : `--headless`, `--no-unlimited`, `--delay <s>`,
`--profile <dossier>`.

## Ajuster les sélecteurs

Le script ne peut pas deviner parfaitement le DOM de Higgsfield. Il tourne en
**mode fenêtré** par défaut pour que tu voies ce qui se passe. Si un élément
n'est pas trouvé :

1. ouvre la page de création dans Chrome, **F12** → inspecte l'élément
   (champ de prompt, toggle « Unlimited », bouton Generate) ;
2. dans `send_prompts.py`, ajuste les valeurs du dictionnaire `SELECTORS`
   (placeholder, texte, rôle ou CSS) ;
3. vérifie aussi `CONFIG['create_url']` si l'URL de création diffère.

En cas d'échec sur un prompt, une capture est écrite dans `./hf_debug/` pour
t'aider à repérer le bon sélecteur. Le script continue avec les prompts suivants.
```
