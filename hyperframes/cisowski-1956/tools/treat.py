"""Traitements d'image une·deux pour les reels Cisowski.
   - duotone  : niveaux de gris -> dégradé encre/crème (tirage sépia de la marque)
   - halftone : trame de points à 45° (rendu « presse d'époque »), nette à la taille de sortie,
                ce qui permet d'agrandir des archives basse définition sans flou
   Usage: python3 treat.py <src> <dst> --size WxH [--focus fx,fy] [--zoom z] [--mode duotone|halftone|color]
"""
import argparse, math
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

INK   = np.array([0x2C, 0x28, 0x23], dtype=np.float32)   # --ink
CREAM = np.array([0xED, 0xDC, 0xB2], dtype=np.float32)   # --cream

def cover(img, size, focus=(0.5, 0.5), zoom=1.0):
    W, H = size
    sw, sh = img.size
    s = max(W / sw, H / sh) * zoom
    nw, nh = max(W, round(sw * s)), max(H, round(sh * s))
    img = img.resize((nw, nh), Image.LANCZOS)
    x = min(max(0, round(nw * focus[0] - W / 2)), nw - W)
    y = min(max(0, round(nh * focus[1] - H / 2)), nh - H)
    return img.crop((x, y, x + W, y + H))

def tone(gray, lo=1.0, hi=99.0, gamma=1.0):
    a = np.asarray(gray, dtype=np.float32) / 255.0
    p0, p1 = np.percentile(a, [lo, hi])
    a = np.clip((a - p0) / max(1e-4, (p1 - p0)), 0, 1)
    return a ** gamma

def duotone(a, ink=INK, cream=CREAM):
    out = ink[None, None, :] * (1 - a[..., None]) + cream[None, None, :] * a[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")

def halftone(a, pitch=9.0, angle=45.0, ss=3, ink=INK, cream=CREAM, softness=0.9, dark=False):
    """a: luminance 0..1 (H,W). Trame AM : point d'encre dont le rayon suit la densité."""
    H, W = a.shape
    big = Image.fromarray((a * 255).astype(np.uint8)).resize((W * ss, H * ss), Image.BICUBIC)
    A = np.asarray(big, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:H * ss, 0:W * ss].astype(np.float32)
    t = math.radians(angle); p = pitch * ss
    u = (xx * math.cos(t) + yy * math.sin(t)) / p
    v = (-xx * math.sin(t) + yy * math.cos(t)) / p
    spot = (np.cos(2 * np.pi * u) + np.cos(2 * np.pi * v)) / 4 + 0.5      # 0..1, max au centre de cellule
    k = softness * 0.18
    if dark:   # fond encre, points crème dont la taille suit la lumière (image positive sur papier sombre)
        m = 1 - np.clip((A - (1 - spot)) / k + 0.5, 0, 1)                 # 1 = encre
    else:      # fond crème, points d'encre dont la taille suit la densité
        m = np.clip(((1 - A) - (1 - spot)) / k + 0.5, 0, 1)
    rgb = cream[None, None, :] * (1 - m[..., None]) + ink[None, None, :] * m[..., None]
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")
    return img.resize((W, H), Image.LANCZOS)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--focus", default="0.5,0.5")
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--mode", default="duotone")
    ap.add_argument("--pitch", type=float, default=9.0)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--crop", default="")          # l,t,r,b en fraction, appliqué avant tout
    ap.add_argument("--blur", type=float, default=0.0)
    ap.add_argument("--dim", type=float, default=1.0)   # <1 assombrit (fond sous texte)
    ap.add_argument("--sat", type=float, default=0.75)
    ap.add_argument("--quality", type=int, default=92)
    ap.add_argument("--fade-top", type=int, default=0)   # fondu vers l'encre sur N px en haut (image posée sous le header)
    a = ap.parse_args()
    W, H = map(int, a.size.lower().split("x")); fx, fy = map(float, a.focus.split(","))
    img = Image.open(a.src).convert("RGB")
    if a.crop:
        l, t, r, b = map(float, a.crop.split(",")); w, h = img.size
        img = img.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
    img = cover(img, (W, H), (fx, fy), a.zoom)
    if a.mode == "color":
        img = ImageEnhance.Color(img).enhance(a.sat)
        warm = Image.new("RGB", img.size, (120, 90, 40))
        img = Image.blend(img, warm, 0.10)
        img = ImageEnhance.Contrast(img).enhance(1.06)
    else:
        g = ImageOps.grayscale(img)
        if a.blur: g = g.filter(ImageFilter.GaussianBlur(a.blur))
        lum = tone(g, gamma=a.gamma)
        if a.dim != 1.0: lum = lum * a.dim
        if a.fade_top:
            ramp = np.clip(np.arange(lum.shape[0], dtype=np.float32) / a.fade_top, 0, 1) ** 1.5
            lum = lum * ramp[:, None]
        if a.mode == "halftone": img = halftone(lum, pitch=a.pitch)
        elif a.mode == "halftone-dark": img = halftone(lum, pitch=a.pitch, dark=True)
        else: img = duotone(lum)
    if a.blur and a.mode == "color": img = img.filter(ImageFilter.GaussianBlur(a.blur))
    if a.dst.lower().endswith(".png"): img.save(a.dst)
    else: img.save(a.dst, quality=a.quality, subsampling=0)
    print(a.dst, img.size)
