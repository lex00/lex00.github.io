#!/usr/bin/env python3
"""Draw the hero for tf-vendor-power-without-the-saas.

    python3 scripts/gen_vendor_power_hero.py

Writes static/img/tf-vendor-power-cover.svg: the TF state industry as a few
pixel dinosaurs on the left, the terragucci taco on the right. The taco is
the brand asset copied in, so it stays the real one; the dinosaurs are drawn
on the same pixel grid so the two halves match.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TACO = Path.home() / "Documents/checkouts/intentius/terragucci/docs-site/public/brand/taco.svg"
OUT = ROOT / "static/img/tf-vendor-power-cover.svg"

W, H = 1280, 400
GROUND = 344
PX = 9  # one dinosaur pixel

BG = "#0d1117"
RULE = "#30363d"

# X body, S shade, P plates, O eye. Every sprite faces right, toward the taco.
TREX = """
..........XXXXX.
.........XXXXXXX
.........XOXXXXX
.........XXXXXXX
.........XXXX...
.........XXXXXX.
X.......XXXXX...
XX.....XXXXXX...
XXX...XXXXXXXXX.
.XXXXXXXXXXX..X.
..XXXXXXXXXX....
...SSSSSSSS.....
....XXX.XX......
....XX...XX.....
"""

BRONTO = """
.....................XXX
....................XXOX
....................XXXX
...................XXX..
..................XXX...
.................XXX....
................XXX.....
.......XXXXXXX.XXX......
.....XXXXXXXXXXXXX......
...XXXXXXXXXXXXXXX......
XXXXXXXXXXXXXXXXXX......
.....SSSSSSSSSSSS.......
.....XX..XX..XX.XX......
.....XX..XX..XX.XX......
"""

STEGO = """
.......P..P..P......
......PXPPXPPXP.....
.....XXXXXXXXXXX....
X...XXXXXXXXXXXXX...
XX.XXXXXXXXXXXXXXXXX
.XXXXXXXXXXXXXXXXXOX
..XXXXXXXXXXXXXXXXX.
....SSSSSSSSSSSS....
....XX.XX..XX.XX....
....XX.XX..XX.XX....
"""

# Muted, a little fossilised next to the taco.
DINOS = [
    (TREX, {"X": "#56634f", "S": "#3f4a3a", "O": "#c9d1d9"}),
    (BRONTO, {"X": "#5b5f6a", "S": "#42454e", "O": "#c9d1d9"}),
    (STEGO, {"X": "#6a5a4a", "S": "#4d4136", "P": "#8a5a3c", "O": "#c9d1d9"}),
]


def sprite(art: str, palette: dict[str, str], x0: int) -> tuple[str, int]:
    rows = [r for r in art.strip("\n").splitlines()]
    h, w = len(rows), max(len(r) for r in rows)
    y0 = GROUND - h * PX
    rects = []
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c in palette:
                rects.append(
                    f'<rect x="{x0 + i * PX}" y="{y0 + j * PX}" width="{PX}" height="{PX}" fill="{palette[c]}"/>'
                )
    return "\n    ".join(rects), w * PX


def taco(cx: int, scale: int) -> str:
    src = TACO.read_text()
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', src).groups())
    inner = src[src.index(">") + 1 : src.rindex("</svg>")]
    x, y = cx - w * scale // 2, GROUND - h * scale + scale
    return f'<g transform="translate({x} {y}) scale({scale})" shape-rendering="crispEdges">{inner}</g>'


def main() -> None:
    gap = 28
    widths = [len(a.strip().splitlines()[0]) * PX for a, _ in DINOS]
    x = (W // 2 - (sum(widths) + gap * (len(DINOS) - 1))) // 2
    herd = []
    for art, pal in DINOS:
        rects, w = sprite(art, pal, x)
        herd.append(rects)
        x += w + gap

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <line x1="{W // 2}" y1="40" x2="{W // 2}" y2="{H - 40}" stroke="{RULE}" stroke-width="2" stroke-dasharray="6 8"/>
  <line x1="40" y1="{GROUND}" x2="{W // 2 - 40}" y2="{GROUND}" stroke="{RULE}" stroke-width="2"/>
  <line x1="{W // 2 + 40}" y1="{GROUND}" x2="{W - 40}" y2="{GROUND}" stroke="{RULE}" stroke-width="2"/>

  <text x="{W // 4}" y="92" text-anchor="middle" font-size="40" font-weight="700" fill="#8b949e">The TF state industry</text>
  <text x="{3 * W // 4}" y="92" text-anchor="middle" font-size="40" font-weight="700" fill="#e6edf3">Terragucci</text>

  <g shape-rendering="crispEdges">
    {chr(10).join("    " + h for h in herd)}
  </g>
  {taco(3 * W // 4, 7)}
</svg>
'''
    OUT.write_text(svg)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
