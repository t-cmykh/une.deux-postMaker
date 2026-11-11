#!/usr/bin/env python3
"""Génère index.html : reel « Portraits — Paul Breitner » à partir du carrousel (sources/slide*.png)."""
import html, re
CPS, FLOOR, CTA = 19.0, 1.1, 3.4
S = [  # (image, [lignes de titre], [sous-titres])
 (1, ["IL A MARQUÉ DANS", "DEUX FINALES", "DE COUPE DU MONDE"], ["Et presque personne ne l'a fait."]),
 (2, ["LE BARBU", "DE MUNICH"], ["**Paul Breitner**, 22 ans en 1974.", "Il pose chez lui devant un portrait de **Mao**."]),
 (3, ["MENÉ D'ENTRÉE"], ["7 juillet 1974, finale contre les Pays-Bas.", "2e minute : penalty. Neeskens marque. **0-1**."]),
 (4, ["LE BALLON,", "IL LE PREND"], ["25e minute, nouveau penalty.", "Breitner n'est **pas le tireur prévu**.", "Il marque. 1-1. La RFA est **championne du monde**."]),
 (5, ["IL CLAQUE", "LA PORTE"], ["Il part au Real Madrid et quitte la sélection.", "Le Mondial 1978 se joue **sans lui**.", "Rappelé en 1981, il finit **2e du Ballon d'Or**."]),
 (6, ["BERNABÉU,", "83E MINUTE"], ["11 juillet 1982, finale contre l'Italie.", "Menée 0-3, la RFA marque. Le buteur : **Breitner**."]),
 (7, ["LA BARBE À", "150 000 MARKS"], ["Et le plus fou, c'est pas ça.", "Avant ce Mondial, une marque de cosmétiques le paie", "**150 000 marks** pour raser sa barbe."]),
 (8, ["LE CLUB", "DES CINQ"], ["Buteurs dans deux finales différentes :", "Vavá, Pelé, **Breitner**, Zidane, Mbappé.", "Il est le **seul Allemand** de la liste."]),
]
plain=lambda t:t.replace("**","")
def mk(t):
    return "".join((f'<b>{html.escape(p)}</b>' if i%2 else html.escape(p)) for i,p in enumerate(re.split(r"\*\*(.+?)\*\*",t)) if p)
r=lambda x:f"{x:.2f}".rstrip("0").rstrip(".")
t=0.0; body=[]; aud=[]; js=[]
for si,(img,tit,subs) in enumerate(S):
    s0=t; durs=[round(max(FLOOR,len(plain(x))/CPS),2) for x in subs]
    if si==0: durs=[2.5]
    D=round(sum(durs),2)
    body.append(f'      <div class="bgwrap clip" id="bg{si}" data-start="{r(s0)}" data-duration="{r(D)}"><img id="bg{si}i" src="assets/bg{img}.jpg" alt="" data-layout-allow-overflow /></div>')
    body.append(f'      <div class="win clip" id="w{si}" data-start="{r(s0)}" data-duration="{r(D)}"><img id="w{si}i" src="assets/w{img}.jpg" alt="" data-layout-allow-overflow /></div>')
    y0=1250-118*len(tit)
    for li,l in enumerate(tit):
        body.append(f'      <div class="tl clip" id="t{si}_{li}" style="top:{y0+118*li}px" data-start="{r(s0)}" data-duration="{r(D)}" data-layout-allow-overlap><span class="box" id="t{si}_{li}b"></span><span class="tx" id="t{si}_{li}x">{html.escape(l)}</span></div>')
    for ki,(x,d) in enumerate(zip(subs,durs)):
        body.append(f'      <div class="sub clip" id="s{si}_{ki}" data-start="{r(t)}" data-duration="{r(d)}"><span>{mk(x)}</span></div>')
        js.append(f"['#s{si}_{ki}',{1 if (si==0 and ki==0) else 0}]"); t=round(t+d,2)
    aud.append(f'      <audio id="a{si}" src="assets/sfx/whoosh-short.mp3" data-start="{r(s0)}" data-duration="0.57" data-volume="0.4"></audio>')
END=t; TOT=round(END+CTA,2)
segs="".join(f'<div class="seg"><i id="p{i}"></i></div>' for i in range(len(S)))
segjs=",".join(f"[{i},{len(t_)}]" for i,(_,t_,_) in enumerate(S))
doc=f'''<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>une·deux — Portraits · Paul Breitner (reel)</title>
    <!-- Généré par gen.py -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="tokens/fonts.css" />
    <link rel="stylesheet" href="tokens/colors.css" />
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#2C2823; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
      .clip {{ opacity:0; }}
      .base {{ position:absolute; inset:0; background:var(--ink); }}
      .bgwrap {{ position:absolute; inset:0; overflow:hidden; z-index:1; }}
      .bgwrap img {{ position:absolute; inset:0; width:1080px; height:1920px; display:block; }}
      .win {{ position:absolute; left:0; top:420px; width:1080px; height:760px; overflow:hidden; z-index:5; background:var(--panel); }}
      .win img {{ position:absolute; inset:0; width:1080px; height:760px; display:block; }}
      #hdr {{ position:absolute; inset:0 0 auto 0; z-index:30; }}
      .ring {{ position:absolute; left:96px; top:216px; width:92px; height:92px; border-radius:50%; border:4px solid var(--cream); display:flex; align-items:center; justify-content:center; font-family:'Saira Condensed',sans-serif; font-weight:600; font-size:38px; color:var(--cream); }}
      .wordmark {{ position:absolute; left:214px; top:262px; transform:translateY(-50%); font-family:'Anton',sans-serif; font-size:58px; color:var(--cream); }}
      .handle {{ position:absolute; right:96px; top:262px; transform:translateY(-50%); font-family:'Saira Condensed',sans-serif; font-weight:600; font-size:32px; color:var(--cream); }}
      .hairline {{ position:absolute; left:96px; right:96px; top:318px; height:4px; background:var(--cream); }}
      .tag {{ position:absolute; left:96px; top:350px; height:50px; display:flex; align-items:center; background:var(--cream); color:var(--ink); font-family:'Saira Condensed',sans-serif; font-weight:600; font-size:32px; padding:0 15px; z-index:30; }}
      .bar {{ position:absolute; left:330px; right:96px; top:371px; height:8px; display:flex; gap:8px; z-index:30; }}
      .seg {{ flex:1; height:8px; background:rgba(237,220,178,.25); position:relative; overflow:hidden; }}
      .seg i {{ position:absolute; inset:0; display:block; background:var(--cream); transform:scaleX(0); transform-origin:0 50%; }}
      .tl {{ position:absolute; left:80px; height:112px; z-index:10; display:inline-block; }}
      .tl .box {{ position:absolute; inset:0; background:var(--cream); transform-origin:0 50%; display:block; }}
      .tl .tx {{ position:relative; display:block; padding:0 16px; font-family:'Anton',sans-serif; font-size:100px; line-height:112px; color:var(--ink); white-space:nowrap; }}
      .sub {{ position:absolute; left:80px; right:80px; top:1300px; height:300px; display:flex; align-items:center; justify-content:center; text-align:center; z-index:12; }}
      .sub span {{ display:block; font-family:'Archivo',sans-serif; font-weight:600; font-size:56px; line-height:1.2; color:var(--cream); }}
      .sub b {{ font-weight:700; color:var(--ocre); }}
      .cta {{ position:absolute; inset:0; z-index:40; background-color:var(--cream); background-image:repeating-linear-gradient(-45deg, rgba(44,40,35,0.06) 0px, rgba(44,40,35,0.06) 2px, transparent 2px, transparent 46px); }}
      .cta .c-ring {{ position:absolute; left:96px; top:216px; width:92px; height:92px; border-radius:50%; border:4px solid var(--ink); display:flex; align-items:center; justify-content:center; font-family:'Saira Condensed',sans-serif; font-weight:600; font-size:38px; color:var(--ink); }}
      .cta .c-word {{ position:absolute; left:214px; top:262px; transform:translateY(-50%); font-family:'Anton',sans-serif; font-size:58px; color:var(--ink); }}
      .cta .c-hair {{ position:absolute; left:96px; right:96px; top:318px; height:4px; background:var(--ink); }}
      .cta .c-tag {{ position:absolute; left:440px; top:700px; width:200px; height:64px; display:flex; align-items:center; justify-content:center; background:var(--ink); color:var(--cream); font-family:'Saira Condensed',sans-serif; font-weight:600; font-size:36px; }}
      .cta .c-t {{ position:absolute; left:0; right:0; text-align:center; font-family:'Anton',sans-serif; font-size:160px; line-height:1; color:var(--ink); }}
      .cta .c-body {{ position:absolute; left:110px; right:110px; top:1150px; text-align:center; font-family:'Archivo',sans-serif; font-weight:500; font-size:46px; line-height:1.3; color:var(--ink); }}
      .cta .c-btn {{ position:absolute; left:390px; top:1400px; width:300px; height:88px; display:flex; align-items:center; justify-content:center; background:var(--ink); color:var(--cream); font-family:'Saira Condensed',sans-serif; font-weight:700; font-size:46px; letter-spacing:.08em; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{r(TOT)}" data-fps="30">
      <div class="base clip" id="base" data-start="0" data-duration="{r(TOT)}"></div>
{chr(10).join(body)}
      <div class="clip" id="hdr" data-start="0" data-duration="{r(END)}"><div class="ring">1·2</div><div class="wordmark">une·deux</div><div class="handle">@UNE.DEUX</div><div class="hairline"></div></div>
      <div class="tag clip" id="tag" data-start="0" data-duration="{r(END)}">PORTRAITS</div>
      <div class="bar clip" id="bar" data-start="0" data-duration="{r(END)}">{segs}</div>
      <div class="cta clip" id="cta" data-start="{r(END)}" data-duration="{r(CTA)}">
        <div class="c-ring">1·2</div><div class="c-word">une·deux</div><div class="c-hair"></div>
        <div class="c-tag" id="cTag">PORTRAITS</div>
        <div class="c-t" id="c1" style="top:790px">PAUL</div><div class="c-t" id="c2" style="top:950px">BREITNER</div>
        <div class="c-body" id="cB">Chaque semaine, le portrait d'une légende du foot.</div>
        <div class="c-btn" id="cBtn">FOLLOW</div>
      </div>
{chr(10).join(aud)}
      <audio id="aCta" src="assets/sfx/pop.mp3" data-start="{r(END+0.05)}" data-duration="0.72" data-volume="0.55"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const T = (sel) => {{ const el = document.querySelector(sel); const s = parseFloat(el.dataset.start); return [s, s + parseFloat(el.dataset.duration)]; }};
      const END = {r(END)};
      tl.set(['#base','#hdr','#tag','#bar'], {{ opacity: 1 }}, 0);
      tl.set(['#hdr','#tag','#bar'], {{ opacity: 0 }}, END);
      [{segjs}].forEach(([i, n]) => {{
        const [s, e] = T('#w' + i);
        tl.set(['#bg' + i, '#w' + i], {{ opacity: 1 }}, s);
        tl.fromTo('#w' + i + 'i', {{ scale: 1.14, x: (i % 2 ? 24 : -24) }}, {{ scale: 1.02, x: 0, duration: e - s, ease: 'power2.out' }}, s);
        tl.fromTo('#bg' + i + 'i', {{ scale: 1.05 }}, {{ scale: 1.12, duration: e - s, ease: 'none' }}, s);
        tl.set(['#bg' + i, '#w' + i], {{ opacity: 0 }}, e);
        tl.fromTo('#p' + i, {{ scaleX: 0 }}, {{ scaleX: 1, duration: e - s, ease: 'none' }}, s);
        for (let l = 0; l < n; l++) {{
          const id = '#t' + i + '_' + l, d = i === 0 ? 0 : 0.07 * l;
          tl.set(id, {{ opacity: 1 }}, s);
          if (i === 0) {{ tl.set([id + 'b', id + 'x'], {{ opacity: 1 }}, 0); }}
          else {{
            tl.fromTo(id + 'b', {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.26, ease: 'power4.out' }}, s + d);
            tl.fromTo(id + 'x', {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.24, ease: 'power3.out' }}, s + d + 0.08);
          }}
          tl.set(id, {{ opacity: 0 }}, e);
        }}
      }});
      [{",".join(js)}].forEach(([id, first]) => {{
        const [s, e] = T(id);
        if (first) tl.fromTo(id, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, s + 0.5);
        else tl.fromTo(id, {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: 'power3.out' }}, s);
        tl.set(id, {{ opacity: 0 }}, e);
      }});
      tl.set('#cta', {{ opacity: 1 }}, END);
      tl.fromTo('#cTag', {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: 'power4.out' }}, END + 0.05);
      tl.fromTo('#c1', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.34, ease: 'power4.out' }}, END + 0.15);
      tl.fromTo('#c2', {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.34, ease: 'power4.out' }}, END + 0.25);
      tl.fromTo('#cB', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, END + 0.45);
      tl.fromTo('#cBtn', {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(1.6)' }}, END + 0.6);
      window.__timelines['main'] = tl;
    </script>
  </body>
</html>
'''
open('index.html','w').write(doc); print('fin',END,'total',TOT)
