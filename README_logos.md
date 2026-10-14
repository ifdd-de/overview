# Regenerating the brand assets

`brand/ifdd_logo.py` generates the IFDD mark from geometry, not from a drawing. Every
asset in `brand/assets/` is reproducible from the script plus the font file.

---

## 1. Create a virtual environment

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
```

Install the dependencies:

```bash
pip install -r brand/requirements.txt
```

| Package | Needed for |
| --- | --- |
| `fonttools` | reading the letter outlines — required |
| `cairosvg` | PNG and ICO export — optional |
| `Pillow` | packing the ICO file — optional |

SVG output works with `fonttools` alone. `cairosvg` needs the system library
`libcairo`; on Debian and Ubuntu: `sudo apt install libcairo2`.

## 2. Provide the font

The mark is set in **Archivo Black** (SIL Open Font License). Place
`ArchivoBlack-Regular.ttf` next to the script or pass its path with `--font`:

```bash
curl -L -o brand/ArchivoBlack-Regular.ttf \
  https://raw.githubusercontent.com/google/fonts/main/ofl/archivoblack/ArchivoBlack-Regular.ttf
```

Letter outlines are converted to paths, so the font is only needed at generation time,
never at display time.

## 3. Generate

```bash
cd brand
python ifdd_logo.py --ico
```

This writes into `brand/assets/`:

| File | Use |
| --- | --- |
| `ifdd-monogram-light.svg` | avatar and header on light backgrounds |
| `ifdd-monogram-dark.svg` | avatar and header on dark backgrounds |
| `ifdd-favicon.svg` | small sizes — diamond only, letters dropped |
| `ifdd-favicon.ico` | browser favicon, 16 – 256 px in one file |

## 4. Options

```bash
python ifdd_logo.py --help
```

| Option | Default | Effect |
| --- | --- | --- |
| `--font PATH` | `ArchivoBlack-Regular.ttf` | font file to read the outlines from |
| `--output DIR` | `assets` | target directory |
| `--seam-gap PX` | `5` | width of the mitre seam; `0` closes the joint |
| `--ico` | off | also export `ifdd-favicon.ico` |

The seam gap is the only aesthetic parameter. At `5` the joint is visible when the
mark is shown large and disappears below roughly 32 px, which keeps small renderings
clean. `--seam-gap 0` gives a solid picture-frame mitre.

## 5. Raster exports

The repository ships SVG and one ICO file. Produce PNGs on demand:

```bash
python -c "import cairosvg; cairosvg.svg2png(url='assets/ifdd-monogram-light.svg', \
  write_to='ifdd-avatar-1024.png', output_width=1024, output_height=1024)"
```

GitHub renders organisation and profile avatars as circles. The monogram keeps a 10 %
safe margin, so the letters survive the crop, but the corners are clipped. Where a
circular crop is certain, prefer `ifdd-favicon.svg`.

## 6. Design constants

All values live at the top of `ifdd_logo.py`. Changing them changes every asset
consistently.

| Constant | Value | Meaning |
| --- | --- | --- |
| `CANVAS` | 512 | edge length of the square artboard |
| `SAFE_MARGIN` | 10 % | clear space kept on every side |
| `CORNER_RADIUS` | 56 | rounding of the background square |
| `DIAMOND_SEAM_GAP` | 5 | default mitre seam |

Colours are defined once as `LIGHT` and `DARK` palettes.

| Role | Hex |
| --- | --- |
| Background, light | `#EDF1F4` |
| Background, dark / letters | `#0F2B46` |
| Edge, primary | `#3FA396` |
| Edge, secondary | `#D2803A` |
| Core | `#F2A65A` |
