#!/usr/bin/env python3
"""Génère reel-2-destin/index.html (proposition 2 : le destin).

Grammaire du reel une·deux (CLAUDE.md) appliquée à des archives fixes :
  - géométrie du composite : fenêtre nette 1080x888 à y=420 + fond flouté désaturé plein cadre ;
  - sous-titres style KARAOKÉ (§4.B) : une ligne = un carton, Anton 80px fixe, top:1480px,
    contour 1.5px rgba(44,40,35,.35), cartons contigus, fondus opacity seuls ;
  - rythme : 13 caractères/seconde, plancher 0.8 s par carton (§5).
Les **mots** entre doubles astérisques passent en ocre (même convention que CORPS (karaoké)).
"""
import html, re, pathlib

CPS, FLOOR = 13.0, 0.8
CTA = 3.6

# (image, légende d'archive, [cartons])
SEGMENTS = [
    ("bleu", "CISOWSKI, BALLON EN MAIN, ET PUSKÁS · 1956", [
        "**5 BUTS** EN UN MATCH",
        "AVEC LES BLEUS.",
        "**ZÉRO** COUPE DU MONDE.",
    ]),
    ("portrait", "THADÉE CISOWSKI · RACING CLUB DE PARIS", [
        "THADÉE **CISOWSKI**.",
        "NÉ EN POLOGNE.",
        "FILS DE MINEUR.",
    ]),
    ("mine", "MINE DE LA MOURIÈRE, PIENNES · ANNÉES 1930", [
        "À **14 ANS**,",
        "IL DESCEND AU FOND.",
    ]),
    ("racing", "CISOWSKI AVEC LE RACING · ANNÉES 1950", [
        "**1951**.",
        "PREMIÈRE SÉLECTION.",
        "9E MINUTE :",
        "**JAMBE CASSÉE**.",
        "IL REVIENT.",
    ]),
    ("couleur", "AVEC LE RACING CLUB DE PARIS · PHOTO COLORISÉE", [
        "**1956**.",
        "**MEILLEUR BUTEUR**",
        "DU CHAMPIONNAT.",
    ]),
    ("action", "FRANCE-BELGIQUE, 11 NOVEMBRE 1956 · MIROIR SPRINT", [
        "FRANCE – BELGIQUE.",
        "UN BUT.",
        "DEUX.",
    ]),
    ("duel", "FRANCE-BELGIQUE, 11 NOVEMBRE 1956 · MIROIR SPRINT", [
        "TROIS.",
        "QUATRE.",
    ]),
    ("but", "FRANCE-BELGIQUE, 11 NOVEMBRE 1956 · MIROIR SPRINT", [
        "**CINQ**.",
        "LES BLEUS FILENT",
        "VERS LE **MONDIAL 1958**.",
    ]),
    ("bleu", "CISOWSKI SOUS LE MAILLOT BLEU · 1956", [
        "1958 : **BLESSÉ**, ENCORE.",
        "LE MONDIAL SE JOUE",
        "**SANS LUI**.",
    ]),
    ("fontaine", "JUST FONTAINE · VIGNETTE PANINI", [
        "UN AUTRE AVANT-CENTRE",
        "Y MARQUE **13 BUTS**.",
        "JUST FONTAINE.",
    ]),
    ("carte", "CARTE DÉDICACÉE DE THADÉE CISOWSKI", [
        "IL MEURT EN **2005**.",
        "SON RECORD, LUI,",
        "TIENT DEPUIS **70 ANS**.",
    ]),
]

# bruitages : (clé de carton « texte brut », fichier, volume, durée) — calés sur le début du carton
SFX_ON_CARD = {
    "JAMBE CASSÉE.": ("impact-bass-1.mp3", 0.30, 2.0),
    "CINQ.": ("impact-bass-1.mp3", 0.34, 2.0),
    "SANS LUI.": ("impact-bass-1.mp3", 0.28, 2.0),
    "Y MARQUE 13 BUTS.": ("ping.mp3", 0.4, 1.3),
    "UN BUT.": ("ping.mp3", 0.34, 0.8), "DEUX.": ("ping.mp3", 0.34, 0.8),
    "TROIS.": ("ping.mp3", 0.34, 0.8), "QUATRE.": ("ping.mp3", 0.34, 0.8),
}

def plain(t): return t.replace("**", "")
def dur(t): return max(FLOOR, len(plain(t)) / CPS)
def markup(t):
    out, parts = [], re.split(r"\*\*(.+?)\*\*", t)
    for i, p in enumerate(parts):
        if not p: continue
        out.append(f'<b class="ocre">{html.escape(p)}</b>' if i % 2 else html.escape(p))
    return "".join(out)
r2 = lambda x: f"{x:.2f}".rstrip("0").rstrip(".")

t = 0.0
seg_html, card_html, audio_html, js_segs, js_cards = [], [], [], [], []
ci = 0
for si, (img, cap, cards) in enumerate(SEGMENTS):
    s0 = t
    for text in cards:
        d = round(dur(text), 2)
        cid = f"k{ci}"
        card_html.append(f'        <div class="story-line clip" id="{cid}" data-start="{r2(t)}" data-duration="{r2(d)}">{markup(text)}</div>')
        js_cards.append(f"'{cid}'")
        if plain(text) in SFX_ON_CARD:
            f, v, sd = SFX_ON_CARD[plain(text)]
            audio_html.append(f'      <audio id="sfxK{ci}" src="assets/sfx/{f}" data-start="{r2(t)}" data-duration="{r2(sd)}" data-volume="{v}"></audio>')
        t = round(t + d, 2); ci += 1
    sd = round(t - s0, 2)
    seg_html.append(
        f'      <div class="bgwrap clip" id="bg{si}" data-start="{r2(s0)}" data-duration="{r2(sd)}"><img id="bg{si}img" src="assets/bg-{img}.jpg" alt="" data-layout-allow-overflow /></div>\n'
        f'      <div class="win clip" id="win{si}" data-start="{r2(s0)}" data-duration="{r2(sd)}"><img id="win{si}img" src="assets/w-{img}.jpg" alt="" data-layout-allow-overflow /></div>\n'
        f'      <div class="cap clip" id="cap{si}" data-start="{r2(s0)}" data-duration="{r2(sd)}">{html.escape(cap)}</div>')
    js_segs.append(str(si))
    if si > 0:
        audio_html.append(f'      <audio id="sfxS{si}" src="assets/sfx/whoosh-short.mp3" data-start="{r2(max(0, s0 - 0.03))}" data-duration="0.57" data-volume="0.32"></audio>')
END = t
TOTAL = round(END + CTA, 2)
audio_html.append(f'      <audio id="sfxCta" src="assets/sfx/pop.mp3" data-start="{r2(END + 0.04)}" data-duration="0.72" data-volume="0.55"></audio>')
audio_html.append(f'      <audio id="sfxCta2" src="assets/sfx/click.mp3" data-start="{r2(END + 0.22)}" data-duration="0.37" data-volume="0.55"></audio>')

DOC = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>une·deux — Ce jour-là · Cisowski, 5 buts (proposition 2 : le destin)</title>
    <!-- Fichier généré par tools/gen_reel2.py — modifier le script, pas ce fichier. -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="tokens/fonts.css" />
    <link rel="stylesheet" href="tokens/colors.css" />
    <style>
      /* Couleur de série : calibrée par pixel-sampling sur hyperframes@0.9.31 (aucun décalage à compenser). */
      :root {{ --ocre-render: #C2A04E; }}

      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #2C2823; }}
      body {{ font-family: 'Archivo', system-ui, sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .clip {{ opacity: 0; }}
      .base {{ position: absolute; inset: 0; background: var(--ink); z-index: 0; }}

      /* ===== composite : fond flouté désaturé + fenêtre nette (même géométrie que le reel vidéo) ===== */
      .bgwrap {{ position: absolute; inset: 0; overflow: hidden; z-index: 1; }}
      .bgwrap img {{ position: absolute; inset: 0; width: 1080px; height: 1920px; display: block; }}
      .win {{ position: absolute; left: 0; top: 420px; width: 1080px; height: 888px; overflow: hidden; z-index: 5; background: var(--panel); }}
      .win img {{ position: absolute; inset: 0; width: 1080px; height: 888px; display: block; }}
      .cap {{ position: absolute; left: 0; top: 1256px; height: 52px; display: flex; align-items: center; z-index: 6;
        background: var(--ink); color: var(--muted-cream); padding: 0 18px 0 96px; white-space: nowrap;
        font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 28px; letter-spacing: .05em; }}

      /* ===== header une·deux (constantes de l'éditeur de série) ===== */
      #hdr {{ position: absolute; inset: 0 0 auto 0; z-index: 30; }}
      .ring {{ position: absolute; left: 96px; top: 216px; width: 92px; height: 92px; border-radius: 50%;
        border: 4px solid var(--cream); display: flex; align-items: center; justify-content: center;
        font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 38px; color: var(--cream); }}
      .wordmark {{ position: absolute; left: 214px; top: 262px; transform: translateY(-50%);
        font-family: 'Anton', sans-serif; font-size: 58px; color: var(--cream); }}
      .handle {{ position: absolute; right: 96px; top: 262px; transform: translateY(-50%);
        font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 32px; color: var(--cream); }}
      .hairline {{ position: absolute; left: 96px; right: 96px; top: 318px; height: 4px; background: var(--cream); }}
      .tag {{ position: absolute; left: 96px; top: 350px; height: 58px; display: flex; align-items: center;
        background: var(--ocre-render); color: var(--ink);
        font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 32px; padding: 0 15px; z-index: 30; }}

      /* ===== sous-titres karaoké (§4.B) ===== */
      .story-zone {{ position: absolute; left: 96px; right: 96px; top: 0; height: 1920px; z-index: 20; text-align: center; }}
      .story-line {{
        position: absolute; left: 0; right: 0;
        top: 1480px; transform: translateY(-50%);
        font-family: 'Anton', sans-serif; font-size: 80px; line-height: 1.1; text-transform: uppercase;
        color: var(--cream);
        -webkit-text-stroke: 1.5px rgba(44,40,35,.35);
      }}
      .story-line b.ocre {{ color: var(--ocre-render); font-weight: inherit; }}

      /* ===== CTA (slide « reste dans le jeu ») ===== */
      .cta {{ position: absolute; inset: 0; z-index: 40; background-color: var(--cream);
        background-image: repeating-linear-gradient(-45deg, rgba(44,40,35,0.06) 0px, rgba(44,40,35,0.06) 2px, transparent 2px, transparent 46px); }}
      .cta .c-ring {{ position: absolute; left: 96px; top: 216px; width: 92px; height: 92px; border-radius: 50%; border: 4px solid var(--ink);
        display: flex; align-items: center; justify-content: center; font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 38px; color: var(--ink); }}
      .cta .c-word {{ position: absolute; left: 214px; top: 262px; transform: translateY(-50%); font-family: 'Anton', sans-serif; font-size: 58px; color: var(--ink); }}
      .cta .c-handle {{ position: absolute; right: 96px; top: 262px; transform: translateY(-50%); font-family: 'Saira Condensed', sans-serif; font-weight: 600; font-size: 32px; color: var(--ink); }}
      .cta .c-hair {{ position: absolute; left: 96px; right: 96px; top: 318px; height: 4px; background: var(--ink); }}
      .cta .c-mark {{ position: absolute; left: 465px; top: 620px; width: 150px; height: 195px; }}
      .cta .c-btn {{ position: absolute; left: 390px; top: 872px; width: 300px; height: 84px; display: flex; justify-content: center; align-items: center;
        background: var(--ocre-render); color: var(--ink); font-family: 'Saira Condensed', sans-serif; font-weight: 700; font-size: 46px; letter-spacing: .08em; }}
      .cta .c-t {{ position: absolute; left: 0; right: 0; text-align: center; font-family: 'Anton', sans-serif; font-size: 150px; line-height: 1; color: var(--ink); }}
      .cta .c-body {{ position: absolute; left: 120px; right: 120px; top: 1340px; text-align: center; font-family: 'Archivo', sans-serif; font-weight: 500; font-size: 42px; line-height: 1.3; color: var(--ink); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{r2(TOTAL)}" data-fps="30">
      <div class="base clip" id="base" data-start="0" data-duration="{r2(TOTAL)}"></div>

      <!-- ================= ARCHIVES (fond flouté + fenêtre nette + légende) ================= -->
{chr(10).join(seg_html)}

      <!-- ================= HEADER ================= -->
      <div class="clip" id="hdr" data-start="0" data-duration="{r2(END)}">
        <div class="ring">1·2</div>
        <div class="wordmark">une·deux</div>
        <div class="handle">@UNE.DEUX</div>
        <div class="hairline"></div>
      </div>
      <div class="tag clip" id="tag" data-start="0" data-duration="{r2(END)}">CE JOUR LÀ · 11 NOVEMBRE 1956</div>

      <!-- ================= SOUS-TITRES KARAOKÉ (une ligne = un carton) ================= -->
      <div class="story-zone">
{chr(10).join(card_html)}
      </div>

      <!-- ================= CTA ================= -->
      <div class="cta clip" id="cta" data-start="{r2(END)}" data-duration="{r2(CTA)}">
        <div class="c-ring">1·2</div><div class="c-word">une·deux</div><div class="c-handle">@UNE.DEUX</div><div class="c-hair"></div>
        <svg class="c-mark" id="ctaMark" viewBox="0 0 120 156"><path fill="#C2A04E" d="M14 0h92a14 14 0 0 1 14 14v142L60 98 0 156V14A14 14 0 0 1 14 0Z" /></svg>
        <div class="c-btn" id="ctaBtn">FOLLOW</div>
        <div class="c-t" id="ctaT1" style="top:1010px">RESTE DANS</div>
        <div class="c-t" id="ctaT2" style="top:1160px">LE JEU</div>
        <div class="c-body" id="ctaBody">Une histoire de foot oubliée, tous les jours.</div>
      </div>

      <!-- ================= SON ================= -->
{chr(10).join(audio_html)}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const T = (sel) => {{ const el = document.querySelector(sel); const s = parseFloat(el.dataset.start); return [s, s + parseFloat(el.dataset.duration)]; }};
      const END = {r2(END)};

      tl.set('#base', {{ opacity: 1 }}, 0);
      tl.set(['#hdr', '#tag'], {{ opacity: 1 }}, 0);
      tl.set(['#hdr', '#tag'], {{ opacity: 0 }}, END);

      // archives : coupe franche, poussée lente et continue dans la fenêtre (jamais d'aller-retour)
      [{", ".join(js_segs)}].forEach((i) => {{
        const [s, e] = T('#win' + i);
        tl.set(['#bg' + i, '#win' + i, '#cap' + i], {{ opacity: 1 }}, s);
        tl.fromTo('#win' + i + 'img', {{ scale: 1.0 }}, {{ scale: 1.0 + 0.016 * (e - s) + 0.02, duration: e - s, ease: 'none' }}, s);
        tl.fromTo('#bg' + i + 'img', {{ scale: 1.04 }}, {{ scale: 1.1, duration: e - s, ease: 'none' }}, s);
        tl.set(['#bg' + i, '#win' + i, '#cap' + i], {{ opacity: 0 }}, e);
      }});

      // karaoké : fondus opacity seuls (le centrage vertical est un transform statique — jamais de tween y)
      function fadeBlockKaraoke(sel, first) {{
        const [s, e] = T(sel);
        if (first) tl.set(sel, {{ opacity: 1 }}, s);
        else tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.10, ease: 'power2.out' }}, s);
        tl.to(sel, {{ opacity: 0, duration: 0.08, ease: 'sine.in' }}, e - 0.08);
        tl.set(sel, {{ opacity: 0 }}, e);
      }}
      [{", ".join(js_cards)}].forEach((id, i) => fadeBlockKaraoke('#' + id, i === 0));

      // CTA
      {{
        const s = END;
        tl.set('#cta', {{ opacity: 1 }}, s);
        tl.fromTo('#ctaMark', {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.36, ease: 'power4.out' }}, s + 0.04);
        tl.fromTo('#ctaBtn', {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(1.6)' }}, s + 0.22);
        tl.fromTo('#ctaT1', {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.36, ease: 'power4.out' }}, s + 0.3);
        tl.fromTo('#ctaT2', {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.36, ease: 'power4.out' }}, s + 0.4);
        tl.fromTo('#ctaBody', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: 'power2.out' }}, s + 0.5);
        tl.to('#ctaBtn', {{ scale: 1.08, duration: 0.18, ease: 'power2.out' }}, s + 1.5);
        tl.to('#ctaBtn', {{ scale: 1, duration: 0.22, ease: 'power2.inOut' }}, s + 1.68);
      }}

      window.__timelines['main'] = tl;
    </script>
  </body>
</html>
"""
out = pathlib.Path(__file__).resolve().parent.parent / "reel-2-destin" / "index.html"
out.write_text(DOC, encoding="utf-8")
print(f"{out}  cartons={ci}  fin du récit={END:.2f}s  total={TOTAL:.2f}s")
for si, (img, cap, cards) in enumerate(SEGMENTS):
    print(f"  seg{si} {img:9s} {sum(round(dur(c),2) for c in cards):5.2f}s  " + " / ".join(plain(c) for c in cards))
