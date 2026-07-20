#!/usr/bin/env python3
"""Build preview/studio-preview.html — a self-contained, scrubbable copy of
../index.html for the Artifact tool (offline: no CDN fonts/GSAP, no CDN
video). Regenerate after any edit to ../index.html or ../assets/*.mp4:

    cd hyperframes/cejourla-reel/preview
    python3 build.py

Requires: ffmpeg, curl (fetches GSAP + Google Fonts once, cached in this dir).
Then republish with the Artifact tool, same file_path, to keep the same URL.
"""
import base64
import re
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # hyperframes/cejourla-reel/
PREVIEW = Path(__file__).resolve().parent  # hyperframes/cejourla-reel/preview/

# Video clips used in the composition: id -> source mp4 filename. Keep in
# sync with the <video src="assets/..."> tags in ../index.html. Full length
# is used (no trim) — "garder la totalité des vidéos" per the brief.
CLIPS = {
    "v1": "wc1-bresil-but.mp4",
    "v2": "wc2-bresil-reaction.mp4",
    "v3": "wc3-angleterre-a.mp4",
    "v4": "wc4-angleterre-b.mp4",
    "v5": "wc5-angleterre-c.mp4",
    "v6": "wc6-angleterre-d.mp4",
}

GSAP_URL = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
FONTS_CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Anton&family=Archivo:wght@400;500;700&family=Saira+Condensed:wght@600;700&display=swap"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"


def fetch(url: str, headers: dict | None = None) -> bytes:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as r:
        return r.read()


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def ensure_gsap() -> Path:
    p = PREVIEW / "gsap.min.js"
    if not p.exists():
        p.write_bytes(fetch(GSAP_URL))
    return p


def ensure_fonts() -> dict[str, Path]:
    """Anton/Archivo/Saira Condensed (600, 700), "latin" subset only —
    enough for the reel's French copy, keeps the artifact small."""
    names = {"anton": PREVIEW / "anton.woff2", "archivo": PREVIEW / "archivo.woff2",
             "saira600": PREVIEW / "saira600.woff2", "saira700": PREVIEW / "saira700.woff2"}
    if all(p.exists() for p in names.values()):
        return names
    css = fetch(FONTS_CSS_URL, {"User-Agent": UA}).decode()
    blocks = css.split("@font-face")[1:]
    urls = {}
    for i, b in enumerate(blocks):
        fam = re.search(r"font-family:\s*'([^']+)'", b).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", b).group(1)
        url = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", b).group(1)
        preceding = css.split("@font-face")[i]
        subset = re.findall(r"/\*\s*(\w[\w-]*)\s*\*/", preceding)[-1]
        if subset != "latin":
            continue
        urls[(fam, weight)] = url
    (PREVIEW / "anton.woff2").write_bytes(fetch(urls[("Anton", "400")]))
    (PREVIEW / "archivo.woff2").write_bytes(fetch(urls[("Archivo", "400")]))
    (PREVIEW / "saira600.woff2").write_bytes(fetch(urls[("Saira Condensed", "600")]))
    (PREVIEW / "saira700.woff2").write_bytes(fetch(urls[("Saira Condensed", "700")]))
    return names


def ensure_proxies() -> dict[str, Path]:
    """Small (406x720, VP9/WebM, muted) trims of the source clips — VP9
    because vanilla/open-source Chromium builds (incl. headless test
    browsers) drop H.264 decode support; VP9 plays everywhere reliably."""
    out = {}
    for vid, src_name in CLIPS.items():
        out_path = PREVIEW / f"proxy_{vid}.webm"
        out[vid] = out_path
        if out_path.exists():
            continue
        src = ROOT / "assets" / src_name
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(src), "-vf", "scale=406:720",
             "-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0", "-cpu-used", "4", "-an",
             str(out_path), "-loglevel", "error"],
            check=True,
        )
    return out


CONTROLS_CSS = """
      #scrubber-bar {
        position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000;
        background: #16140f; border-top: 1px solid #35302a;
        padding: 10px 16px 14px; font-family: 'Saira Condensed', system-ui, sans-serif;
        display: flex; align-items: center; gap: 12px; box-sizing: border-box;
      }
      #scrubber-bar button {
        background: #C2A04E; color: #2C2823; border: none; width: 38px; height: 38px;
        border-radius: 50%; font-size: 16px; cursor: pointer; flex: 0 0 auto;
        display: flex; align-items: center; justify-content: center;
      }
      #scrubber-bar input[type=range] { flex: 1; accent-color: #C2A04E; }
      #scrubber-bar button:focus-visible,
      #scrubber-bar input[type=range]:focus-visible { outline: 2px solid #C2A04E; outline-offset: 2px; }
      #scrubber-bar .time { color: #EDDCB2; font-weight: 700; font-size: 14px; min-width: 96px; text-align: right; }
      #scrubber-note {
        position: fixed; top: 10px; left: 10px; z-index: 1000; color: #EDDCB2; opacity: .55;
        font-family: 'Saira Condensed', system-ui, sans-serif; font-size: 11px; letter-spacing: .04em;
      }
"""

CONTROLS_HTML = """
    <div id="scrubber-note">une·deux — reel "Ce jour-là" — aperçu (vidéos basse résolution, sans son)</div>
    <div id="scrubber-bar">
      <button id="playBtn">▶</button>
      <input type="range" id="seek" min="0" max="{TOTAL}" step="0.01" value="0" />
      <div class="time" id="timeLabel">0.0s / {TOTAL}s</div>
    </div>
"""

ENGINE_JS = """
      // ================= standalone scrubber engine =================
      // HyperFrames' own runtime (clip show/hide, video currentTime sync) only
      // exists inside the CLI preview/render pipeline. This block re-implements
      // just enough of it — driven by the same `tl` GSAP timeline above — so the
      // composition can scrub interactively in a plain browser tab. Videos are
      // handed to Chromium as blob: URLs (decoded from the base64 payloads
      // above) rather than raw data: URIs — far more reliably demuxed/seekable.
      function b64ToBlobUrl(b64, mime) {
        const bin = atob(b64);
        const bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
        return URL.createObjectURL(new Blob([bytes], { type: mime }));
      }
      Object.keys(VIDEO_B64).forEach((id) => {
        document.getElementById(id).src = b64ToBlobUrl(VIDEO_B64[id], 'video/webm');
      });

      const TOTAL = parseFloat(document.getElementById('root').dataset.duration);
      const clips = Array.from(document.querySelectorAll('[data-start][data-duration]'))
        .filter((el) => el.id !== 'root');

      function fitStage() {
        const pad = 70; // room for the scrubber bar
        const scale = Math.min(window.innerWidth / 1080, (window.innerHeight - pad) / 1920);
        const root = document.getElementById('root');
        root.style.transform = `scale(${scale})`;
        root.style.left = `${(window.innerWidth - 1080 * scale) / 2}px`;
      }
      window.addEventListener('resize', fitStage);
      fitStage();

      let isPlaying = false;
      let current = 0;
      let lastTs = null;

      function renderClips(t) {
        clips.forEach((el) => {
          const start = parseFloat(el.dataset.start);
          const dur = parseFloat(el.dataset.duration);
          const visible = t >= start && t <= start + dur;
          el.style.display = visible ? '' : 'none';
          if (el.tagName === 'VIDEO') {
            if (visible) {
              const local = Math.min(Math.max(t - start, 0), dur);
              if (Math.abs(el.currentTime - local) > 0.1) el.currentTime = local;
              if (isPlaying) { if (el.paused) el.play().catch(() => {}); }
              else if (!el.paused) el.pause();
            } else if (!el.paused) {
              el.pause();
            }
          }
        });
      }

      function seekTo(t) {
        current = Math.min(Math.max(t, 0), TOTAL);
        tl.time(current);
        renderClips(current);
        document.getElementById('seek').value = current;
        document.getElementById('timeLabel').textContent = `${current.toFixed(1)}s / ${TOTAL.toFixed(1)}s`;
      }

      function tick(ts) {
        if (isPlaying) {
          if (lastTs != null) {
            current += (ts - lastTs) / 1000;
            if (current >= TOTAL) { current = TOTAL; isPlaying = false; document.getElementById('playBtn').textContent = '▶'; }
          }
          lastTs = ts;
          seekTo(current);
        }
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);

      document.getElementById('playBtn').addEventListener('click', () => {
        isPlaying = !isPlaying;
        lastTs = null;
        if (isPlaying && current >= TOTAL) current = 0;
        document.getElementById('playBtn').textContent = isPlaying ? '❚❚' : '▶';
      });
      document.getElementById('seek').addEventListener('input', (e) => {
        isPlaying = false;
        document.getElementById('playBtn').textContent = '▶';
        seekTo(parseFloat(e.target.value));
      });

      seekTo(0);
"""


def main():
    gsap_path = ensure_gsap()
    fonts = ensure_fonts()
    proxies = ensure_proxies()

    base = (ROOT / "index.html").read_text(encoding="utf-8")
    colors_css = (ROOT / "tokens" / "colors.css").read_text(encoding="utf-8")
    gsap_js = gsap_path.read_text(encoding="utf-8")

    fonts_inline = f"""
    @font-face {{ font-family: 'Anton'; src: url(data:font/woff2;base64,{b64(fonts['anton'])}) format('woff2'); font-weight: 400; }}
    @font-face {{ font-family: 'Archivo'; src: url(data:font/woff2;base64,{b64(fonts['archivo'])}) format('woff2'); font-weight: 400 700; }}
    @font-face {{ font-family: 'Saira Condensed'; src: url(data:font/woff2;base64,{b64(fonts['saira600'])}) format('woff2'); font-weight: 600; }}
    @font-face {{ font-family: 'Saira Condensed'; src: url(data:font/woff2;base64,{b64(fonts['saira700'])}) format('woff2'); font-weight: 700; }}
    {colors_css}
"""

    out = base
    out = out.replace('<link rel="stylesheet" href="tokens/fonts.css" />', "")
    out = out.replace('<link rel="stylesheet" href="tokens/colors.css" />', f"<style>{fonts_inline}</style>")
    out = out.replace(
        '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>',
        f"<script>{gsap_js}</script>",
    )
    for vid, src_name in CLIPS.items():
        out = out.replace(f'src="assets/{src_name}"', "")

    out = out.replace(
        "html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--ink); }",
        "html, body { width: 100%; height: 100%; overflow: hidden; background: #0e0d0c; }",
    )
    out = out.replace(
        "#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; }",
        "#root { position: absolute; top: 0; left: 0; width: 1080px; height: 1920px; overflow: hidden; "
        "transform-origin: top left; box-shadow: 0 20px 60px rgba(0,0,0,.5); }",
    )
    out = out.replace("      .anim { opacity: 0; }", "      .anim { opacity: 0; }\n" + CONTROLS_CSS)

    root_duration = re.search(r'data-duration="([\d.]+)"', out).group(1)
    marker = "    </div>\n\n    <script>"
    assert out.count(marker) == 1, "expected exactly one #root-closing / <script> boundary"
    out = out.replace(marker, "    </div>\n" + CONTROLS_HTML.format(TOTAL=root_duration) + "\n    <script>")

    video_b64_js = "const VIDEO_B64 = {\n" + ",\n".join(
        f'  {vid}: "{b64(proxies[vid])}"' for vid in CLIPS
    ) + "\n};\n"

    out = out.replace(
        "      window.__timelines['main'] = tl;\n    </script>",
        "      window.__timelines['main'] = tl;\n" + video_b64_js + ENGINE_JS + "    </script>",
    )

    dest = PREVIEW / "studio-preview.html"
    dest.write_text(out, encoding="utf-8")
    print(f"wrote {dest} ({len(out) / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
