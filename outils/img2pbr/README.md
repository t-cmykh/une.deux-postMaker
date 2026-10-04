# img2pbr

Une image → cartes PBR **carrées** en **EXR ACEScg**, avec un **USD + shader MaterialX** en option.

```bash
pip install -r requirements.txt

# interface locale (sélecteur 1K/2K/4K + toggle USD)
python3 app.py            # http://127.0.0.1:8765

# ligne de commande
python3 img2pbr.py photo.jpg -o sortie --res 2k --usd
```

## Export

| Option | Valeurs |
|---|---|
| Résolution (carré) | `--res 1k` (1024) · `2k` (2048) · `4k` (4096). L'image est recadrée au centre en carré. |
| USD / MaterialX | `--usd` (toggle « Exporter aussi un USD » dans l'interface). `--usd-format usda\|usdc`, `--usd-plane` pour un plan de test. |

Fichiers : `<nom>_basecolor_<res>.exr`, `_normal_`, `_roughness_`, `_height_`, `_ao_` (+ `_metallic_` si `--metallic > 0`), puis `<nom>.usda`.

- **basecolor** : EXR half RGB en **ACEScg** (AP1, blanc D60), chromaticités AP1 écrites dans l'en-tête, attribut `oiio:ColorSpace=ACEScg`. Conversion depuis sRGB → linéaire Rec.709 → ACEScg (Bradford).
- **normal, roughness, height, ao, metallic** : données **Raw** (non converties). Normal OpenGL (+Y), encodé 0..1, `--flip-green` pour DirectX. Roughness/AO/metallic en half 1 canal (`Y`), height en float32.

## USD

Un `Material` MaterialX (`outputs:mtlx:surface` / `outputs:mtlx:displacement`) :
`ND_standard_surface_surfaceshader` ← `ND_image_color3` (basecolor, `acescg`), `ND_image_float` (roughness, metalness si exporté), `ND_normalmap_float` ← `ND_image_vector3` (normal), et `height − 0.5` → `ND_displacement_float` (échelle `--disp-scale`, 0.01 = 1 cm). Chemins des textures relatifs au USD : garde les fichiers dans le même dossier.
L'AO est exportée mais **non branchée** (standard_surface n'a pas d'entrée d'occlusion).

Vérifié : les identifiants de nœuds, noms et types de ports sont contrôlés contre la librairie standard MaterialX 1.39 et les connexions résolues par `pxr.Usd`. **Non vérifié** : le rendu dans un moteur MaterialX (Karma, Storm, Arnold…). Les nœuds suivent le nommage MaterialX 1.39 (`ND_normalmap_float`) : un hôte en 1.38 attend `ND_normalmap`.

## Limites

Les cartes sont **estimées à partir de l'image seule** (aucun modèle ML) : albedo dé-éclairé par filtrage basse fréquence, height = bande de fréquences de la luminance, normal = Sobel sur la height, roughness = heuristique (détail local + luminance), AO = cavités de la height. Roughness et metallic sont à retoucher. Pas de mise en tuile (seamless) automatique.
