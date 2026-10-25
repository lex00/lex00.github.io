#!/usr/bin/env python3
"""Draw the hero for resource-level-concurrency-for-terraform.

    python3 scripts/gen_concurrency_hero.py

A padlock split by a hammer with "choudoufu" on the handle, on the same
pixel grid as the tf-vendor-power hero. Writes the post's banner,
static/img/concurrency-hero.svg; its link preview at 1200x630,
static/img/concurrency-share.png; and a white 1200x630 copy at 2x for a
LinkedIn image post, cover-light.png in
~/Documents/blogs/resource-level-concurrency-for-terraform/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_vendor_power_hero import png  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static/img/concurrency-hero.svg"
SHARE = ROOT / "static/img/concurrency-share.png"
BLOG = Path.home() / "Documents/blogs/resource-level-concurrency-for-terraform"

W, H, GROUND, PX = 1280, 400, 370, 9
#: The lock is drawn on a coarser grid so it reads as a padlock beside the hammer.
LP = 12
TITLE = "Resource-level concurrency for Terraform"

THEMES = {
    "dark": dict(bg="#0d1117", rule="#30363d", title="#e6edf3",
                 brass="#c9a227", brass_hi="#e3c35a", brass_lo="#8a6d12", hole="#0d1117",
                 steel="#8b949e", steel_hi="#c9d1d9", steel_lo="#57606a",
                 wood="#a0673a", wood_lo="#7a4b28", label="#ffffff",
                 spark="#f2cc60", swing="#30363d"),
    "light": dict(bg="#ffffff", rule="#d0d7de", title="#1f2328",
                  brass="#c9a227", brass_hi="#e3c35a", brass_lo="#8a6d12", hole="#ffffff",
                  steel="#6e7781", steel_hi="#afb8c1", steel_lo="#424a53",
                  wood="#a0673a", wood_lo="#7a4b28", label="#ffffff",
                  spark="#d4a72c", swing="#d0d7de"),
}

# B brass, H highlight, L shade, K keyhole, "." the crack and the background.
BODY = """
HHHHHHHHHHHHHHHH
BBBBBBBB.BBBBBBB
BBBBBBBB..BBBBBB
BBBBBBBBB.BBBBBB
BBBBBBKKBB.BBBBB
BBBBBBKKBB..BBBB
BBBBBBBKBBB.BBBB
BBBBBBBKBBBB.BBB
BBBBBBBBBBB..BBB
BBBBBBBBBBBB.BBB
LLLLLLLLLLLL..LL
LLLLLLLLLLLLL.LL
"""

# S steel, T its highlight. The shackle, split at the crown where it's struck.
SHACKLE = """
..TTT..TTT..
.SSSS..SSSS.
SSS......SSS
SS........SS
SS........SS
SS........SS
SS........SS
SS........SS
"""

# Sparks around the strike, as pixel offsets from it.
SPARKS = [(-7, -3), (-9, -6), (-6, -8), (8, -4), (10, -7), (7, -9), (12, -2)]


def sprite(art: str, palette: dict[str, str], x0: int, y0: int, px: int = PX) -> str:
    rects = []
    for j, row in enumerate(art.strip("\n").splitlines()):
        for i, c in enumerate(row):
            if c in palette:
                rects.append(f'<rect x="{x0 + i * px}" y="{y0 + j * px}" width="{px}" '
                             f'height="{px}" fill="{palette[c]}"/>')
    return "\n    ".join(rects)


def hammer(t: dict[str, str], fx: int, fy: int) -> str:
    """A hammer whose face strikes at fx, fy, the handle running up and right.

    Drawn level, head upright at the left end of the handle with its face at
    the bottom, then turned 10 degrees so the face comes down on the lock.
    """
    head_w, head_h = 6 * PX, 13 * PX
    grip_l, grip_h = 36 * PX, 5 * PX
    hx = -head_w // 2
    return f'''<g transform="translate({fx} {fy}) rotate(-10) translate(0 {-head_h // 2})" shape-rendering="crispEdges">
    <rect x="{head_w // 2}" y="{-grip_h // 2}" width="{grip_l}" height="{grip_h}" fill="{t['wood']}"/>
    <rect x="{head_w // 2}" y="{grip_h // 2 - PX}" width="{grip_l}" height="{PX}" fill="{t['wood_lo']}"/>
    <rect x="{head_w // 2 + grip_l - 6 * PX}" y="{-grip_h // 2}" width="{6 * PX}" height="{grip_h}" fill="{t['wood_lo']}"/>
    <text x="{head_w // 2 + (grip_l - 6 * PX) // 2}" y="{11}" text-anchor="middle" font-size="30" font-weight="700" fill="{t['label']}" letter-spacing="1">choudoufu</text>
    <rect x="{hx}" y="{-head_h // 2}" width="{head_w}" height="{head_h}" fill="{t['steel']}"/>
    <rect x="{hx}" y="{-head_h // 2}" width="{PX * 2}" height="{head_h}" fill="{t['steel_hi']}"/>
    <rect x="{hx + head_w - PX}" y="{-head_h // 2}" width="{PX}" height="{head_h}" fill="{t['steel_lo']}"/>
    <rect x="{hx - PX}" y="{head_h // 2 - 2 * PX}" width="{head_w + 2 * PX}" height="{2 * PX}" fill="{t['steel_lo']}"/>
    <rect x="{hx - PX}" y="{-head_h // 2}" width="{head_w + 2 * PX}" height="{2 * PX}" fill="{t['steel_lo']}"/>
  </g>'''


def scene(t: dict[str, str]) -> str:
    bw, bh = 16 * LP, 12 * LP
    bx, by = W // 2 - bw // 2 - 80, GROUND - bh
    body = sprite(BODY, {"B": t["brass"], "H": t["brass_hi"], "L": t["brass_lo"],
                         "K": t["hole"]}, bx, by, LP)
    # The shackle sits in the body; its legs run under the body's top row.
    sx, sy = bx + 2 * LP, by - 7 * LP
    shackle = sprite(SHACKLE, {"S": t["steel"], "T": t["steel_hi"]}, sx, sy, LP)
    # The hammer comes down on the shackle's crown.
    fx, fy = sx + 6 * LP, sy
    sparks = "\n    ".join(
        f'<rect x="{fx + dx * PX}" y="{fy + dy * PX}" width="{PX}" height="{PX}" fill="{t["spark"]}"/>'
        for dx, dy in SPARKS)
    swing = "\n  ".join(
        f'<path d="M{fx + 150 + k * 46} {fy - 60 + k * 18} q 70 40 90 120" fill="none" '
        f'stroke="{t["swing"]}" stroke-width="6" stroke-linecap="round"/>'
        for k in range(3))
    return f'''<line x1="80" y1="{GROUND}" x2="{W - 80}" y2="{GROUND}" stroke="{t['rule']}" stroke-width="2"/>
  {swing}
  <g shape-rendering="crispEdges">
    {shackle}
    {body}
    {sparks}
  </g>
  {hammer(t, fx, fy)}'''


def render(t: dict[str, str], size: str = "hero") -> str:
    font = 'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif"'
    if size == "hero":
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" {font}>\n'
                f'  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>\n  {scene(t)}\n</svg>\n')
    sw, sh, s = 1200, 630, 0.9
    x = (sw - W * s) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sw} {sh}" {font}>\n'
            f'  <rect width="{sw}" height="{sh}" fill="{t["bg"]}"/>\n'
            f'  <text x="{sw // 2}" y="96" text-anchor="middle" font-size="52" font-weight="700" '
            f'fill="{t["title"]}">{TITLE}</text>\n'
            f'  <g transform="translate({x:.0f} 230) scale({s})">\n  {scene(t)}\n  </g>\n</svg>\n')


def main() -> None:
    OUT.write_text(render(THEMES["dark"]))
    print(f"wrote {OUT}")
    BLOG.mkdir(parents=True, exist_ok=True)
    svg = BLOG / "share.svg"
    svg.write_text(render(THEMES["dark"], "share"))
    png(svg, SHARE, 1200, 630, 1)
    print(f"wrote {SHARE}")
    svg = BLOG / "cover-light.svg"
    svg.write_text(render(THEMES["light"], "share"))
    png(svg, BLOG / "cover-light.png", 1200, 630, 2)
    print(f"wrote {BLOG / 'cover-light.png'}")


if __name__ == "__main__":
    main()
