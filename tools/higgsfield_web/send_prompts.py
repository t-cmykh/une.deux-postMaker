#!/usr/bin/env python3
"""Envoie des prompts sur higgsfield.ai (interface web) via Playwright,
en cochant l'option « Unlimited » avant chaque génération.

Pourquoi un navigateur et pas l'API : le mode « Unlimited » (générations qui
ne consomment pas de crédits) n'existe que dans l'app web. Ce script pilote un
vrai Chromium connecté à TON compte pour reproduire ton clic.

Installation (sur TA machine) :
    pip install playwright
    playwright install chromium

Étape 1 — se connecter une seule fois (session sauvegardée dans ./hf_profile) :
    python3 send_prompts.py login

Étape 2 — envoyer les prompts (un par ligne dans prompts.txt) :
    python3 send_prompts.py run --prompts prompts.txt

Le profil persistant (--profile) garde ta session entre les exécutions, donc
tu ne te reconnectes pas à chaque fois.

⚠️  Automatiser l'interface web peut être contraire aux CGU de Higgsfield.
    Tu utilises ici TON compte et TON entitlement « unlimited » ; à toi de
    vérifier que c'est autorisé. Garde un délai raisonnable entre prompts.

Les SÉLECTEURS ci-dessous sont des points d'ajustement : lance d'abord en mode
fenêtré (par défaut). Si un élément n'est pas trouvé, ouvre les DevTools sur la
page de création, repère le bon texte/placeholder/role et remplace la valeur
correspondante dans SELECTORS. En cas d'échec, une capture est enregistrée
dans ./hf_debug pour t'aider.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    sys.exit("Playwright manquant. Installe-le : pip install playwright && playwright install chromium")

HERE = Path(__file__).resolve().parent

# --- À AJUSTER si besoin après le premier run -------------------------------
CONFIG = {
    # Page où l'on tape un prompt. Adapte si l'URL de création diffère.
    "create_url": "https://higgsfield.ai/create/image",
    # URL servant à vérifier qu'on est bien connecté (présence d'un élément app).
    "home_url": "https://higgsfield.ai/",
}

SELECTORS = {
    # Zone de saisie du prompt. On essaie ces stratégies dans l'ordre.
    "prompt_input": {
        "placeholder": "Describe",          # get_by_placeholder (sous-chaîne)
        "role": ("textbox", None),           # get_by_role("textbox")
        "css": "textarea",                   # fallback CSS
    },
    # Bouton/case « Unlimited ». On gère un toggle déjà actif (aria-checked).
    "unlimited_toggle": {
        "text": "Unlimited",                 # get_by_text (sous-chaîne, insensible casse)
        "css": "[data-testid*='unlimited'], [aria-label*='Unlimited']",
    },
    # Bouton de lancement de la génération.
    "generate_button": {
        "names": ["Generate", "Create", "Run"],  # get_by_role("button", name=...)
        "css": "button[type='submit']",
    },
}
# ---------------------------------------------------------------------------


def log(msg: str) -> None:
    print(f"[hf] {msg}", flush=True)


def find_prompt_input(page):
    s = SELECTORS["prompt_input"]
    if s.get("placeholder"):
        loc = page.get_by_placeholder(s["placeholder"], exact=False)
        if loc.count():
            return loc.first
    if s.get("role"):
        role, name = s["role"]
        loc = page.get_by_role(role) if not name else page.get_by_role(role, name=name)
        if loc.count():
            return loc.first
    loc = page.locator(s["css"])
    if loc.count():
        return loc.first
    raise RuntimeError("Champ de prompt introuvable — ajuste SELECTORS['prompt_input'].")


def ensure_unlimited(page) -> None:
    """Active l'option Unlimited si elle ne l'est pas déjà."""
    s = SELECTORS["unlimited_toggle"]
    loc = None
    if s.get("text"):
        cand = page.get_by_text(s["text"], exact=False)
        if cand.count():
            loc = cand.first
    if loc is None and s.get("css"):
        cand = page.locator(s["css"])
        if cand.count():
            loc = cand.first
    if loc is None:
        log("⚠️  Toggle 'Unlimited' introuvable — vérifie SELECTORS['unlimited_toggle']. On continue sans.")
        return
    # Si l'élément expose un état coché, ne re-clique pas inutilement.
    state = None
    for attr in ("aria-checked", "data-state", "aria-pressed"):
        val = loc.get_attribute(attr)
        if val is not None:
            state = val
            break
    if state in ("true", "checked", "on", "active"):
        log("Unlimited déjà actif.")
        return
    try:
        loc.click(timeout=4000)
        log("Unlimited coché.")
    except PWTimeout:
        log("⚠️  Impossible de cliquer le toggle Unlimited (timeout).")


def click_generate(page) -> None:
    s = SELECTORS["generate_button"]
    for name in s.get("names", []):
        loc = page.get_by_role("button", name=name, exact=False)
        if loc.count():
            loc.first.click()
            return
    loc = page.locator(s["css"])
    if loc.count():
        loc.first.click()
        return
    raise RuntimeError("Bouton de génération introuvable — ajuste SELECTORS['generate_button'].")


def read_prompts(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def make_context(pw, profile: Path, headless: bool):
    profile.mkdir(parents=True, exist_ok=True)
    return pw.chromium.launch_persistent_context(
        user_data_dir=str(profile),
        headless=headless,
        viewport={"width": 1380, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )


def cmd_login(args) -> int:
    with sync_playwright() as pw:
        ctx = make_context(pw, args.profile, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(CONFIG["home_url"])
        log("Connecte-toi dans la fenêtre, puis reviens ici et appuie sur Entrée…")
        try:
            input()
        except EOFError:
            time.sleep(60)
        ctx.close()
    log("Session sauvegardée dans le profil. Tu peux lancer 'run'.")
    return 0


def cmd_run(args) -> int:
    prompts = read_prompts(args.prompts)
    if not prompts:
        log("Aucun prompt à envoyer.")
        return 1
    debug = HERE / "hf_debug"
    debug.mkdir(exist_ok=True)
    log(f"{len(prompts)} prompt(s) à envoyer (délai {args.delay}s, unlimited={'on' if not args.no_unlimited else 'off'}).")

    sent = 0
    with sync_playwright() as pw:
        ctx = make_context(pw, args.profile, headless=args.headless)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, prompt in enumerate(prompts, 1):
            try:
                page.goto(CONFIG["create_url"], wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
                field = find_prompt_input(page)
                field.click()
                field.fill("")
                field.type(prompt, delay=10)
                if not args.no_unlimited:
                    ensure_unlimited(page)
                if args.dry_run:
                    log(f"[{i}/{len(prompts)}] (dry-run) prêt : {prompt[:60]}…")
                else:
                    click_generate(page)
                    log(f"[{i}/{len(prompts)}] envoyé : {prompt[:60]}…")
                    sent += 1
                    page.wait_for_timeout(int(args.delay * 1000))
            except Exception as exc:  # noqa: BLE001 — on veut continuer la file
                shot = debug / f"error_{i:03d}.png"
                try:
                    page.screenshot(path=str(shot))
                except Exception:
                    shot = "(capture impossible)"
                log(f"[{i}/{len(prompts)}] ÉCHEC: {exc} — capture: {shot}")
        ctx.close()
    log(f"Terminé : {sent}/{len(prompts)} envoyé(s).")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Envoi de prompts Higgsfield (web, mode Unlimited).")
    ap.add_argument("--profile", type=Path, default=HERE / "hf_profile",
                    help="Dossier de profil Chromium persistant (session connectée).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_login = sub.add_parser("login", help="Ouvre un navigateur pour te connecter une fois.")
    p_login.set_defaults(func=cmd_login)

    p_run = sub.add_parser("run", help="Envoie les prompts.")
    p_run.add_argument("--prompts", type=Path, default=HERE / "prompts.txt", help="Fichier de prompts.")
    p_run.add_argument("--delay", type=float, default=8.0, help="Délai (s) entre deux envois.")
    p_run.add_argument("--headless", action="store_true", help="Sans fenêtre (déconseillé au début).")
    p_run.add_argument("--no-unlimited", action="store_true", help="Ne pas cocher Unlimited.")
    p_run.add_argument("--dry-run", action="store_true", help="Remplit le prompt sans cliquer Generate.")
    p_run.set_defaults(func=cmd_run)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
