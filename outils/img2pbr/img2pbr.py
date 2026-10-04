#!/usr/bin/env python3
"""img2pbr — une image -> cartes PBR carrées (EXR ACEScg) + USD MaterialX optionnel.

Cartes produites : basecolor, normal (OpenGL), roughness, height, ao (+ metallic si > 0).
Toutes les cartes sont estimées à partir de l'image seule (pas de modèle ML) : ce sont des
approximations à retoucher, surtout roughness et metallic. Voir README.md.

Usage :
    python3 img2pbr.py photo.jpg -o sortie --res 2k --usd
"""
import argparse
import io
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageOps

RESOLUTIONS = {"1k": 1024, "2k": 2048, "4k": 4096}
MAPS = ("basecolor", "normal", "roughness", "height", "ao", "metallic")
DATA_COLORSPACE = "Raw"
COLOR_COLORSPACE = "ACEScg"      # nom OCIO / attribut EXR
MTLX_COLORSPACE = {"ACEScg": "acescg", "Raw": "raw"}   # noms MaterialX / USD

# ---------------------------------------------------------------- couleur : sRGB -> ACEScg


def _rgb_to_xyz(prim, white):
    (rx, ry), (gx, gy), (bx, by) = prim
    xyz = lambda x, y: np.array([x / y, 1.0, (1 - x - y) / y])
    P = np.stack([xyz(rx, ry), xyz(gx, gy), xyz(bx, by)], axis=1)
    W = xyz(*white)
    S = np.linalg.solve(P, W)
    return P * S


def _bradford(src_white, dst_white):
    M = np.array([[0.8951, 0.2664, -0.1614], [-0.7502, 1.7135, 0.0367], [0.0389, -0.0685, 1.0296]])
    xyz = lambda x, y: np.array([x / y, 1.0, (1 - x - y) / y])
    s, d = M @ xyz(*src_white), M @ xyz(*dst_white)
    return np.linalg.inv(M) @ np.diag(d / s) @ M


D65 = (0.3127, 0.3290)
D60 = (0.32168, 0.33767)  # blanc ACES
AP1 = ((0.713, 0.293), (0.165, 0.830), (0.128, 0.044))
REC709 = ((0.640, 0.330), (0.300, 0.600), (0.150, 0.060))
# Rec.709 linéaire (D65) -> ACEScg (AP1, D60), adaptation Bradford
SRGB_TO_ACESCG = np.linalg.inv(_rgb_to_xyz(AP1, D60)) @ _bradford(D65, D60) @ _rgb_to_xyz(REC709, D65)
ACESCG_TO_SRGB = np.linalg.inv(SRGB_TO_ACESCG)


def srgb_to_linear(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(x):
    x = np.clip(x, 0, None)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


# ---------------------------------------------------------------- outils image


def _resize(a, n, resample=Image.LANCZOS):
    """redimensionne un tableau float32 HxW ou HxWx3 vers nxn."""
    if a.ndim == 2:
        return np.asarray(Image.fromarray(a.astype(np.float32), "F").resize((n, n), resample), dtype=np.float32)
    return np.stack([_resize(a[..., c], n, resample) for c in range(a.shape[2])], axis=-1)


def blur(a, sigma):
    """flou gaussien rapide quelle que soit la taille de sigma (travail sur une copie réduite)."""
    from scipy.ndimage import gaussian_filter

    n = a.shape[0]
    f = int(max(1, sigma // 6))
    if f == 1:
        return gaussian_filter(a, sigma, mode="reflect")
    m = max(8, n // f)
    small = _resize(a, m, Image.BOX)
    small = gaussian_filter(small, sigma * m / n, mode="reflect")
    return _resize(small, n, Image.BICUBIC)


def norm01(a, lo=1.0, hi=99.0):
    l, h = np.percentile(a, [lo, hi])
    return np.clip((a - l) / max(h - l, 1e-6), 0, 1)


def load_square(src, n):
    """charge une image (chemin ou octets), recadre au centre en carré, passe en lin. Rec.709 nxn."""
    im = Image.open(io.BytesIO(src) if isinstance(src, (bytes, bytearray)) else src)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("I;16", "I;16B", "I"):
        im = im.point(lambda v: v / 256).convert("L")
    im = im.convert("RGB")
    w, h = im.size
    s = min(w, h)
    left, top = (w - s) // 2, (h - s) // 2
    im = im.crop((left, top, left + s, top + s))
    lin = srgb_to_linear(np.asarray(im, dtype=np.float32) / 255.0).astype(np.float32)
    lin = np.clip(_resize(lin, n), 0, None)
    return lin, dict(source_size=(w, h), crop=s, upscaled=bool(s < n))


# ---------------------------------------------------------------- cartes


def make_maps(lin, delight=0.6, normal_strength=2.0, flip_green=False, invert_height=False,
              roughness_bias=0.0, roughness_contrast=1.0, ao_strength=0.8, metallic=0.0):
    n = lin.shape[0]
    luma = lin @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    # albedo : on retire l'éclairage de grande échelle, on plafonne à une valeur physique
    flat = blur(np.clip(luma, 1e-4, None), n / 6)
    gain = (flat.mean() / np.maximum(flat, 1e-4)) ** delight
    albedo = lin * gain[..., None]
    albedo *= min(1.0, 0.9 / max(float(np.percentile(albedo, 99.5)), 1e-4))
    albedo = np.clip(albedo, 0.0, 1.0).astype(np.float32)
    # height : bande de fréquences de la luminance perceptuelle
    yp = linear_to_srgb(albedo @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)).astype(np.float32)
    h = blur(yp, max(0.8, n * 0.0015)) - blur(yp, n / 12)
    height = norm01(h)
    if invert_height:
        height = 1.0 - height
    # normal : Sobel sur la hauteur, intensité indépendante de la résolution
    from scipy.ndimage import sobel

    k = normal_strength * (n / 1024.0) * 0.6
    dx = sobel(height, axis=1, mode="reflect") / 8.0 * k
    dy = sobel(height, axis=0, mode="reflect") / 8.0 * k  # y image vers le bas
    ny = dy if flip_green else -dy  # OpenGL : +Y vers le haut
    nrm = np.stack([-dx, ny, np.ones_like(dx)], axis=-1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    normal = (nrm * 0.5 + 0.5).astype(np.float32)
    # roughness : heuristique (plus de détail local et plus sombre => plus rugueux)
    detail = norm01(blur(np.abs(yp - blur(yp, max(1.0, n / 256))), n / 64))
    yn = norm01(blur(yp, n / 128), 2, 98)
    rough = 0.62 + 0.30 * (detail - 0.5) * 2 * 0.5 + 0.20 * (0.5 - yn)
    rough = np.clip((rough - 0.62) * roughness_contrast + 0.62 + roughness_bias, 0.15, 1.0).astype(np.float32)
    # ao : cavités de la hauteur à deux échelles
    c = np.maximum(blur(height, n / 256) - height, 0) + 0.6 * np.maximum(blur(height, n / 64) - height, 0)
    ao = (1.0 - ao_strength * norm01(c, 0, 99)).astype(np.float32)
    out = dict(basecolor=albedo, normal=normal, roughness=rough, height=height.astype(np.float32), ao=ao)
    if metallic > 0:
        out["metallic"] = np.full((n, n), float(metallic), dtype=np.float32)
    return out


# ---------------------------------------------------------------- EXR


def write_exr(path, arr, colorspace):
    """EXR scanline ZIP. Couleur : half ACEScg + chromaticités AP1. Données : half (height : float32)."""
    import OpenEXR

    is_color = colorspace == COLOR_COLORSPACE
    hdr = {"compression": OpenEXR.ZIP_COMPRESSION, "type": OpenEXR.scanlineimage, "oiio:ColorSpace": colorspace}
    if is_color:
        hdr["chromaticities"] = (*AP1[0], *AP1[1], *AP1[2], *D60)
    if arr.ndim == 2:
        data = {"Y": np.ascontiguousarray(arr, dtype=np.float32 if "height" in os.path.basename(path) else np.float16)}
    else:
        data = {"RGB": np.ascontiguousarray(arr, dtype=np.float16)}
    OpenEXR.File(hdr, data).write(path)


def to_acescg(lin_rec709):
    return (lin_rec709 @ SRGB_TO_ACESCG.T.astype(np.float32)).astype(np.float32)


# ---------------------------------------------------------------- USD + MaterialX


def write_usd(path, name, files, has_metallic, disp_scale=0.01, plane=False, fmt="usda"):
    """USD avec un matériau MaterialX (standard_surface) dont les textures EXR sont branchées."""
    from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade, Vt

    stage = Usd.Stage.CreateNew(path)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    UsdGeom.SetStageMetersPerUnit(stage, 1.0)
    root = UsdGeom.Xform.Define(stage, f"/{name}")
    stage.SetDefaultPrim(root.GetPrim())
    UsdGeom.Scope.Define(stage, f"/{name}/Materials")
    base = f"/{name}/Materials/{name}"
    mat = UsdShade.Material.Define(stage, base)
    T = Sdf.ValueTypeNames

    def node(nid, nname, out_type):
        s = UsdShade.Shader.Define(stage, f"{base}/{nname}")
        s.CreateIdAttr(nid)
        o = s.CreateOutput("out", out_type)
        return s, o

    uv, uv_out = node("ND_texcoord_vector2", "uv", T.Float2)

    def image(nid, nname, out_type, key, cs):
        s, o = node(nid, nname, out_type)
        f = s.CreateInput("file", T.Asset)
        f.Set(Sdf.AssetPath("./" + os.path.basename(files[key])))
        f.GetAttr().SetColorSpace(MTLX_COLORSPACE[cs])
        s.CreateInput("texcoord", T.Float2).ConnectToSource(uv_out)
        return s, o

    ss, ss_out = node("ND_standard_surface_surfaceshader", "surface", T.Token)
    ss.CreateInput("base", T.Float).Set(1.0)
    _, c = image("ND_image_color3", "basecolor", T.Color3f, "basecolor", COLOR_COLORSPACE)
    ss.CreateInput("base_color", T.Color3f).ConnectToSource(c)
    _, r = image("ND_image_float", "roughness", T.Float, "roughness", DATA_COLORSPACE)
    ss.CreateInput("specular_roughness", T.Float).ConnectToSource(r)
    if has_metallic:
        _, m = image("ND_image_float", "metallic", T.Float, "metallic", DATA_COLORSPACE)
        ss.CreateInput("metalness", T.Float).ConnectToSource(m)
    else:
        ss.CreateInput("metalness", T.Float).Set(0.0)
    _, nm = image("ND_image_vector3", "normal_tex", T.Float3, "normal", DATA_COLORSPACE)
    nmap, nmap_out = node("ND_normalmap_float", "normal_map", T.Float3)
    nmap.CreateInput("in", T.Float3).ConnectToSource(nm)
    nmap.CreateInput("scale", T.Float).Set(1.0)
    ss.CreateInput("normal", T.Float3).ConnectToSource(nmap_out)
    mat.CreateSurfaceOutput("mtlx").ConnectToSource(ss_out)
    # déplacement : (height - 0.5) * échelle
    _, hh = image("ND_image_float", "height", T.Float, "height", DATA_COLORSPACE)
    sub, sub_out = node("ND_subtract_float", "height_centered", T.Float)
    sub.CreateInput("in1", T.Float).ConnectToSource(hh)
    sub.CreateInput("in2", T.Float).Set(0.5)
    disp, disp_out = node("ND_displacement_float", "displacement", T.Token)
    disp.CreateInput("displacement", T.Float).ConnectToSource(sub_out)
    disp.CreateInput("scale", T.Float).Set(float(disp_scale))
    mat.CreateDisplacementOutput("mtlx").ConnectToSource(disp_out)

    if plane:  # plan 1 m x 1 m avec UV, pour tester le matériau tel quel
        q = UsdGeom.Mesh.Define(stage, f"/{name}/Preview")
        q.CreatePointsAttr(Vt.Vec3fArray([Gf.Vec3f(-.5, 0, -.5), Gf.Vec3f(.5, 0, -.5), Gf.Vec3f(.5, 0, .5), Gf.Vec3f(-.5, 0, .5)]))
        q.CreateFaceVertexCountsAttr([4]); q.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
        q.CreateNormalsAttr(Vt.Vec3fArray([Gf.Vec3f(0, 1, 0)] * 4)); q.SetNormalsInterpolation("vertex")
        pv = UsdGeom.PrimvarsAPI(q).CreatePrimvar("st", T.TexCoord2fArray, UsdGeom.Tokens.vertex)
        pv.Set(Vt.Vec2fArray([Gf.Vec2f(0, 0), Gf.Vec2f(1, 0), Gf.Vec2f(1, 1), Gf.Vec2f(0, 1)]))
        UsdShade.MaterialBindingAPI.Apply(q.GetPrim()).Bind(mat)
    stage.GetRootLayer().documentation = f"img2pbr : matériau MaterialX {name}. Couleur ACEScg, cartes de données raw."
    stage.GetRootLayer().Save()


# ---------------------------------------------------------------- orchestration


def preview_png(arr, kind, size=256):
    """aperçu 8 bits sRGB d'une carte (pour l'interface)."""
    a = linear_to_srgb(arr) if kind == "basecolor" else arr
    a = np.clip(a, 0, 1)
    im = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    im = im.resize((size, size), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "PNG")
    return b.getvalue()


def generate(src, out_dir, name="texture", res="2k", usd=False, usd_plane=False, usd_format="usda",
             disp_scale=0.01, want_previews=False, **map_opts):
    n = RESOLUTIONS[res.lower()] if isinstance(res, str) else int(res)
    if n not in RESOLUTIONS.values():
        raise ValueError("résolution carrée attendue : 1k, 2k ou 4k")
    os.makedirs(out_dir, exist_ok=True)
    lin, info = load_square(src, n)
    maps = make_maps(lin, **map_opts)
    tag = {v: k for k, v in RESOLUTIONS.items()}[n]
    files, previews = {}, {}
    for key, arr in maps.items():
        p = os.path.join(out_dir, f"{name}_{key}_{tag}.exr")
        if key == "basecolor":
            write_exr(p, to_acescg(arr), COLOR_COLORSPACE)
        else:
            write_exr(p, arr, DATA_COLORSPACE)
        files[key] = p
        if want_previews:
            previews[key] = preview_png(arr, key)
    if usd:
        p = os.path.join(out_dir, f"{name}.{usd_format}")
        write_usd(p, name, files, "metallic" in maps, disp_scale=disp_scale, plane=usd_plane, fmt=usd_format)
        files["usd"] = p
    meta = dict(name=name, resolution=n, colorspace=dict(color=COLOR_COLORSPACE, data=DATA_COLORSPACE), **info)
    return dict(files=files, previews=previews, meta=meta)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Image -> cartes PBR carrées EXR ACEScg (+ USD MaterialX).")
    ap.add_argument("image")
    ap.add_argument("-o", "--out", default="sortie_pbr")
    ap.add_argument("-n", "--name", help="nom de base (défaut : nom du fichier)")
    ap.add_argument("--res", choices=list(RESOLUTIONS), default="2k", help="résolution carrée d'export")
    ap.add_argument("--usd", action=argparse.BooleanOptionalAction, default=False,
                    help="exporte aussi un USD avec un shader MaterialX branché sur les textures")
    ap.add_argument("--usd-format", choices=("usda", "usdc"), default="usda")
    ap.add_argument("--usd-plane", action="store_true", help="ajoute un plan de test lié au matériau")
    ap.add_argument("--disp-scale", type=float, default=0.01, help="échelle du déplacement dans l'USD (unités USD = m)")
    ap.add_argument("--delight", type=float, default=0.6, help="retrait de l'éclairage de l'albedo, 0..1")
    ap.add_argument("--normal-strength", type=float, default=2.0)
    ap.add_argument("--flip-green", action="store_true", help="normal DirectX (Y inversé) au lieu d'OpenGL")
    ap.add_argument("--invert-height", action="store_true")
    ap.add_argument("--roughness-bias", type=float, default=0.0)
    ap.add_argument("--roughness-contrast", type=float, default=1.0)
    ap.add_argument("--ao-strength", type=float, default=0.8)
    ap.add_argument("--metallic", type=float, default=0.0, help="> 0 : exporte une carte metallic constante")
    a = ap.parse_args(argv)
    name = a.name or os.path.splitext(os.path.basename(a.image))[0]
    r = generate(a.image, a.out, name, a.res, usd=a.usd, usd_plane=a.usd_plane, usd_format=a.usd_format,
                 disp_scale=a.disp_scale, delight=a.delight, normal_strength=a.normal_strength,
                 flip_green=a.flip_green, invert_height=a.invert_height, roughness_bias=a.roughness_bias,
                 roughness_contrast=a.roughness_contrast, ao_strength=a.ao_strength, metallic=a.metallic)
    if r["meta"]["upscaled"]:
        print(f"attention : la source ({r['meta']['crop']} px carrés) est plus petite que {r['meta']['resolution']} px, "
              "elle a été agrandie", file=sys.stderr)
    print(json.dumps({k: v for k, v in r["files"].items()}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
