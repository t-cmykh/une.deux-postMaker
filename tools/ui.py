#!/usr/bin/env python3
"""Mini-UI web locale pour le workflow post → Drive.

Lance un petit serveur local et ouvre une page avec un formulaire :
  - les liens des images (un par ligne ; URL cloudfront OU lien images.higgs.ai) ;
  - le JSON du post Insta (collé) ;
  - le dossier Drive de destination (chemin OU ID).
Au clic sur « Lancer », le workflow télécharge, renomme dans l'ordre des slides,
et (option) téléverse dans un dossier <post> de ton Drive — journal en direct.

À lancer sur TA machine :
    python ui.py
puis ouvre http://127.0.0.1:8765 (ouvert automatiquement).

Pré-requis Drive identiques au CLI : credentials.json à côté du script, et
  pip install google-api-python-client google-auth-oauthlib
"""
from __future__ import annotations

import json
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import download_higgsfield as dh

HOST, PORT = "127.0.0.1", 8765

PAGE = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>une·deux — post → Drive</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Helvetica Neue',Arial,sans-serif;background:#0a0a0a;color:#fff;
       min-height:100dvh;padding:32px 16px;display:flex;justify-content:center}
  .wrap{width:100%;max-width:760px}
  h1{font-size:1.7rem;font-weight:300;letter-spacing:.15em;text-transform:uppercase;margin-bottom:4px}
  h1 b{font-weight:700}
  .sub{color:rgba(255,255,255,.45);font-size:.85rem;margin-bottom:28px}
  label{display:block;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;
        color:rgba(255,255,255,.6);margin:18px 0 6px}
  textarea,input[type=text]{width:100%;background:rgba(255,255,255,.04);color:#fff;
        border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:12px 14px;
        font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85rem}
  textarea{resize:vertical}
  textarea#sources{min-height:120px}
  textarea#postjson{min-height:150px}
  .row{display:flex;gap:14px;flex-wrap:wrap}
  .row>div{flex:1;min-width:220px}
  .opt{display:flex;align-items:center;gap:8px;margin-top:16px;font-size:.85rem;color:rgba(255,255,255,.8)}
  .opt input{width:16px;height:16px}
  button{margin-top:24px;width:100%;padding:14px;border:none;border-radius:10px;
        background:#27543C;color:#fff;font-size:1rem;font-weight:600;letter-spacing:.05em;
        text-transform:uppercase;cursor:pointer;transition:.2s}
  button:hover{background:#2f6648}
  button:disabled{opacity:.5;cursor:wait}
  pre#log{margin-top:24px;background:#000;border:1px solid rgba(255,255,255,.12);border-radius:10px;
        padding:14px;font-size:.8rem;white-space:pre-wrap;min-height:60px;color:#cfead8}
  a{color:#C2A04E}
  .hint{font-size:.72rem;color:rgba(255,255,255,.35);margin-top:4px}
</style></head><body>
<div class="wrap">
  <h1>une<b>·</b>deux — post <b>→</b> Drive</h1>
  <div class="sub">Liens + JSON du post + dossier Drive → téléchargement, renommage, envoi.</div>

  <label>Liens des images (un par ligne, dans l'ordre des slides)</label>
  <textarea id="sources" placeholder="https://…cloudfront.net/…png&#10;https://images.higgs.ai/?…&url=…&#10;ou un chemin local C:\\…\\image.png"></textarea>
  <div class="hint">URL cloudfront directe OU lien images.higgs.ai (déballé en pleine résolution) OU chemin local.</div>

  <label>JSON du post (collé)</label>
  <textarea id="postjson" placeholder='{"slides":[{"title":"…","media":"mbappe_01.jpg"}, …]}'></textarea>
  <div class="hint">Le nom du dossier est dérivé du préfixe des médias (mbappe_01 → « mbappe »).</div>

  <div class="row">
    <div>
      <label>Dossier Drive — chemin</label>
      <input type="text" id="parent" value="une·deux/Posts" placeholder="une·deux/Posts">
    </div>
    <div>
      <label>… ou ID de dossier (prioritaire)</label>
      <input type="text" id="parentid" placeholder="1AbCdEf…">
    </div>
  </div>
  <div class="row">
    <div>
      <label>Nom du post (optionnel — sinon auto)</label>
      <input type="text" id="name" placeholder="(auto depuis le JSON)">
    </div>
  </div>

  <label class="opt"><input type="checkbox" id="todrive" checked> Envoyer sur Google Drive</label>

  <button id="go">Lancer</button>
  <pre id="log">Prêt.</pre>
</div>

<script>
const $ = id => document.getElementById(id);
$('go').onclick = async () => {
  const body = {
    sources: $('sources').value,
    post_json: $('postjson').value,
    to_drive: $('todrive').checked,
    drive_parent: $('parent').value,
    drive_parent_id: $('parentid').value,
    name: $('name').value,
  };
  $('go').disabled = true;
  $('log').textContent = 'Traitement en cours… (une fenêtre Google peut s\\'ouvrir au 1er envoi Drive)';
  try {
    const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)});
    const data = await r.json();
    let out = (data.log || []).join('\\n');
    if (data.folder_link) out += '\\n\\n📂 ' + data.folder_link;
    $('log').innerHTML = out.replace(/(https?:\\/\\/\\S+)/g, '<a href="$1" target="_blank">$1</a>');
  } catch(e) {
    $('log').textContent = 'Erreur : ' + e;
  } finally {
    $('go').disabled = false;
  }
};
</script>
</body></html>"""


def run_workflow(payload: dict) -> dict:
    log: list[str] = []
    folder_link = None

    # 1) Sources (ordre conservé), normalisées (déballe images.higgs.ai).
    raw = [l.strip() for l in (payload.get("sources") or "").splitlines()]
    sources = [dh.normalize_source(s) for s in raw if s and not s.startswith("#")]
    if not sources:
        return {"log": ["✗ Aucun lien fourni."]}

    # 2) JSON du post -> médias ordonnés.
    try:
        data = json.loads(payload.get("post_json") or "")
    except Exception as e:
        return {"log": [f"✗ JSON du post invalide : {e}"]}
    try:
        medias = dh.post_media_from_data(data)
    except Exception as e:
        return {"log": [f"✗ {e}"]}
    if not medias:
        return {"log": ["✗ Aucun champ 'media' dans le JSON du post."]}

    post_name = (payload.get("name") or "").strip() or dh.derive_post_name(medias)
    n = min(len(sources), len(medias))
    if len(sources) != len(medias):
        log.append(f"⚠️ {len(sources)} lien(s) vs {len(medias)} média(s) — on associe les {n} premiers, dans l'ordre.")

    out_dir = dh.DEFAULT_OUT / post_name
    out_dir.mkdir(parents=True, exist_ok=True)
    log.append(f"Post « {post_name} » — {n} fichier(s) → {out_dir}")

    # 3) Téléchargement + renommage dans l'ordre.
    ready: list[Path] = []
    for i in range(n):
        dest = out_dir / dh.target_name(medias[i], sources[i])
        status, msg = dh.fetch_to(sources[i], dest, retries=4, overwrite=False)
        log.append(f"  {'✓' if status=='ok' else '•' if status=='skip' else '✗'} {msg}")
        if status in ("ok", "skip"):
            ready.append(dest)

    # 4) Drive (option).
    if not payload.get("to_drive"):
        log.append("(Envoi Drive non coché : dossier local prêt.)")
        return {"log": log, "post_name": post_name}

    try:
        log.append("Drive : authentification…")
        svc = dh.drive_service(dh.HERE / "credentials.json", dh.HERE / "token.json")
        pid = (payload.get("drive_parent_id") or "").strip()
        if pid:
            parent_id = pid
        else:
            parent = (payload.get("drive_parent") or "").strip()
            parent_id = dh.drive_ensure_path(svc, parent) if parent else None
        folder_id = dh.drive_ensure_folder(svc, post_name, parent_id)
        for p in sorted(ready):
            res = dh.drive_upload(svc, p, folder_id)
            log.append(f"  ↑ {p.name} ({res})")
        folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
        log.append(f"✓ Dossier Drive « {post_name} » prêt.")
    except SystemExit as e:
        log.append(f"✗ Drive : {e}")
    except Exception:
        log.append("✗ Drive : " + traceback.format_exc().splitlines()[-1])

    return {"log": log, "post_name": post_name, "folder_link": folder_link}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE)
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/run":
            self._send(404, "not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = run_workflow(payload)
        except Exception:
            result = {"log": ["✗ " + traceback.format_exc().splitlines()[-1]]}
        self._send(200, json.dumps(result), "application/json; charset=utf-8")

    def log_message(self, *args):  # silencieux
        pass


def main() -> int:
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"UI prête → {url}  (Ctrl+C pour arrêter)")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
