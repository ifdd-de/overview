"""Generate the IFDD brand mark: an IFDD monogram around a two-coloured diamond.

The mark exists in three forms that share one geometry:

* ``monogram``  - four letters in the corners, diamond in the centre (avatar)
* ``favicon``   - diamond only, for sizes where letters stop being legible
* both of them in a light and a dark palette

Run the module to write every asset into the output directory.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

CANVAS = 512
CORNER_RADIUS = 56
SAFE_MARGIN = 0.10 * CANVAS
CENTRE = CANVAS / 2

LETTER_SIZE = 182
LETTER_OPTICAL_LIFT = 4

DIAMOND_RADIUS = 124
DIAMOND_WIDTH = 20
DIAMOND_SEAM_GAP = 5

FAVICON_RADIUS = 176
FAVICON_WIDTH = 56
FAVICON_CORE_RADIUS = 64
MONOGRAM_CORE_RADIUS = 24

DEFAULT_FONT = Path("ArchivoBlack-Regular.ttf")
DEFAULT_OUTPUT = Path("assets")

Point = tuple[float, float]
Vector = tuple[float, float]

NORTH: Vector = (0.0, -1.0)
EAST: Vector = (1.0, 0.0)
SOUTH: Vector = (0.0, 1.0)
WEST: Vector = (-1.0, 0.0)


@dataclass(frozen=True)
class Palette:
    """Colours of one rendering. Edge colours alternate around the diamond."""

    background: str
    letters: str
    edge_primary: str
    edge_secondary: str
    core: str


LIGHT = Palette(
    background="#EDF1F4",
    letters="#0F2B46",
    edge_primary="#3FA396",
    edge_secondary="#D2803A",
    core="#F2A65A",
)

DARK = Palette(
    background="#0F2B46",
    letters="#EDF1F4",
    edge_primary="#3FA396",
    edge_secondary="#D2803A",
    core="#F2A65A",
)


@dataclass(frozen=True)
class Glyph:
    """A single letter outline, ready to be placed by its ink area."""

    path: str
    scale: float
    ink_width: float
    ink_height: float
    ink_left: float

    @classmethod
    def load(cls, font: TTFont, character: str, size: float) -> "Glyph":
        scale = size / font["head"].unitsPerEm
        glyph_set = font.getGlyphSet()
        glyph_name = font.getBestCmap()[ord(character)]

        pen = SVGPathPen(glyph_set)
        glyph_set[glyph_name].draw(pen)

        bounds = font["glyf"][glyph_name]
        return cls(
            path=pen.getCommands(),
            scale=scale,
            ink_width=(bounds.xMax - bounds.xMin) * scale,
            ink_height=(bounds.yMax - bounds.yMin) * scale,
            ink_left=bounds.xMin * scale,
        )

    def placed_at(self, centre_x: float, centre_y: float) -> str:
        """Centre the glyph on its ink area rather than on its advance width."""
        offset_x = centre_x - self.ink_width / 2 - self.ink_left
        offset_y = centre_y + self.ink_height / 2
        return (
            f'<g transform="translate({offset_x:.2f} {offset_y:.2f}) '
            f'scale({self.scale:.5f} {-self.scale:.5f})">'
            f'<path d="{self.path}"/></g>'
        )


@dataclass(frozen=True)
class LetterSlot:
    """One corner of the monogram: which letter goes there and in which corner."""

    character: str
    horizontal: float
    vertical: float


LETTER_SLOTS = (
    LetterSlot("I", -1, -1),
    LetterSlot("F", +1, -1),
    LetterSlot("D", -1, +1),
    LetterSlot("D", +1, +1),
)


def monogram_letters(font_path: Path, size: float = LETTER_SIZE) -> str:
    """Set the four letters flush against the safe margin."""
    font = TTFont(font_path)
    glyphs = {character: Glyph.load(font, character, size) for character in "IFD"}

    placements = []
    for slot in LETTER_SLOTS:
        glyph = glyphs[slot.character]
        x = (
            SAFE_MARGIN + glyph.ink_width / 2
            if slot.horizontal < 0
            else CANVAS - SAFE_MARGIN - glyph.ink_width / 2
        )
        y = (
            SAFE_MARGIN + glyph.ink_height / 2
            if slot.vertical < 0
            else CANVAS - SAFE_MARGIN - glyph.ink_height / 2
        )
        placements.append(glyph.placed_at(x, y - LETTER_OPTICAL_LIFT))

    return "".join(placements)


def _corner(direction: Vector, distance: float) -> Point:
    return CENTRE + direction[0] * distance, CENTRE + direction[1] * distance


def _edge_band(start: Vector, end: Vector, radius: float, width: float, seam_gap: float) -> str:
    """One edge of the diamond as a polygon.

    The outer points sit exactly on the symmetry axes, so neighbouring edges meet
    in a mitre joint. ``seam_gap`` pulls the inner points away from those axes,
    which opens the joint towards the centre and makes the seam visible when the
    mark is displayed large.
    """
    outer_radius = radius + width / 2
    inner_radius = radius - width / 2

    outer_start = _corner(start, outer_radius)
    outer_end = _corner(end, outer_radius)
    inner_start = (
        CENTRE + start[0] * inner_radius + end[0] * seam_gap,
        CENTRE + start[1] * inner_radius + end[1] * seam_gap,
    )
    inner_end = (
        CENTRE + end[0] * inner_radius + start[0] * seam_gap,
        CENTRE + end[1] * inner_radius + start[1] * seam_gap,
    )

    corners = (outer_start, outer_end, inner_end, inner_start)
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in corners)


def diamond(palette: Palette, radius: float, width: float, seam_gap: float) -> str:
    """Four mitred edges; opposite edges share a colour."""
    edges = (
        (NORTH, EAST, palette.edge_primary),
        (EAST, SOUTH, palette.edge_secondary),
        (SOUTH, WEST, palette.edge_primary),
        (WEST, NORTH, palette.edge_secondary),
    )
    return "".join(
        f'<polygon points="{_edge_band(start, end, radius, width, seam_gap)}" fill="{colour}"/>'
        for start, end, colour in edges
    )


def core(palette: Palette, radius: float) -> str:
    return f'<circle cx="{CENTRE:g}" cy="{CENTRE:g}" r="{radius}" fill="{palette.core}"/>'


def _document(palette: Palette, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" '
        f'width="{CANVAS}" height="{CANVAS}" role="img" aria-label="IFDD">'
        f"<title>IFDD</title>"
        f'<rect width="{CANVAS}" height="{CANVAS}" rx="{CORNER_RADIUS}" fill="{palette.background}"/>'
        f"{body}</svg>"
    )


def render_monogram(palette: Palette, font_path: Path, seam_gap: float = DIAMOND_SEAM_GAP) -> str:
    body = (
        f'<g fill="{palette.letters}">{monogram_letters(font_path)}</g>'
        f"{diamond(palette, DIAMOND_RADIUS, DIAMOND_WIDTH, seam_gap)}"
        f"{core(palette, MONOGRAM_CORE_RADIUS)}"
    )
    return _document(palette, body)


def render_favicon(palette: Palette = DARK, seam_gap: float = DIAMOND_SEAM_GAP) -> str:
    """The diamond alone, with the seam gap scaled to the larger radius."""
    scaled_gap = seam_gap * FAVICON_RADIUS / DIAMOND_RADIUS
    body = (
        f"{diamond(palette, FAVICON_RADIUS, FAVICON_WIDTH, scaled_gap)}"
        f"{core(palette, FAVICON_CORE_RADIUS)}"
    )
    return _document(palette, body)


def write_assets(output_dir: Path, font_path: Path, seam_gap: float = DIAMOND_SEAM_GAP) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    assets = {
        "ifdd-monogram-light.svg": render_monogram(LIGHT, font_path, seam_gap),
        "ifdd-monogram-dark.svg": render_monogram(DARK, font_path, seam_gap),
        "ifdd-favicon.svg": render_favicon(DARK, seam_gap),
    }

    written = []
    for name, markup in assets.items():
        target = output_dir / name
        target.write_text(markup, encoding="utf-8")
        written.append(target)
    return written


def export_favicon_ico(svg_path: Path, ico_path: Path) -> Path:
    """Convert the favicon into a multi-resolution ICO file.

    Requires ``cairosvg`` and ``Pillow``; both are optional for pure SVG output.
    """
    import io

    import cairosvg
    from PIL import Image

    sizes = (16, 32, 48, 64, 128, 256)
    largest = cairosvg.svg2png(url=str(svg_path), output_width=max(sizes), output_height=max(sizes))
    Image.open(io.BytesIO(largest)).convert("RGBA").save(
        ico_path, format="ICO", sizes=[(size, size) for size in sizes]
    )
    return ico_path


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the IFDD brand mark.")
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT, help="TrueType file of Archivo Black")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="directory for the generated files")
    parser.add_argument(
        "--seam-gap",
        type=float,
        default=DIAMOND_SEAM_GAP,
        help="width of the mitre seam in pixels; 0 closes the joint completely",
    )
    parser.add_argument("--ico", action="store_true", help="also export the favicon as an ICO file")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    written = write_assets(arguments.output, arguments.font, arguments.seam_gap)

    if arguments.ico:
        favicon_svg = arguments.output / "ifdd-favicon.svg"
        written.append(export_favicon_ico(favicon_svg, arguments.output / "ifdd-favicon.ico"))

    for path in written:
        print(path)


if __name__ == "__main__":
    main()
