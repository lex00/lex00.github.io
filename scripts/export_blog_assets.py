#!/usr/bin/env python3
"""Export this post's figures to ~/Documents/blogs/<slug>/, dark and light, SVG and PNG.

    python3 scripts/export_blog_assets.py
    python3 scripts/export_blog_assets.py <slug> <svg-stem>:<out-name> ...

With no arguments it exports the expectations post, as it always has.

The table pairs already come out of gen_expectations_tables.py in both themes.
The hero is hand-drawn in the dark palette only, so its light twin is derived
here by swapping colours rather than maintained as a second file that drifts.

PNGs are rendered through headless Chrome at 2x, the same way the justfile
renders the og-card.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "img"
DEFAULT_SLUG = "infra-tooling-expectations-in-2026"
DEFAULT_PAIRS = [("expectations-hero", "hero"),
                 ("expectations-claims", "claims"),
                 ("expectations-ops", "ops")]

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

#: Dark hex to its light counterpart. Applied in one pass, so no swap feeds
#: another: #8b949e becomes #57606a without then becoming #8c959f.
LIGHT = {
    "#0d1117": "#ffffff",  # page ground, and the inset chips
    "#161b22": "#f6f8fa",  # box fill
    "#30363d": "#d0d7de",  # borders
    "#c9d1d9": "#1c2128",  # primary text, and the GitHub mark
    "#8b949e": "#57606a",  # dim text
    "#57606a": "#8c959f",  # rules and arrows
    "#7ee787": "#1a7f37",  # ownership green
    "#79c0ff": "#0550ae",  # graph blue
    "#f0883e": "#bc4c00",  # drift orange
    "#a78bfa": "#6639ba",  # forge purple
    "#e8985a": "#e24329",  # GitLab, brighter on white
    "#3a4048": "#8a929c",  # cylinder metal, dark end
    "#c8d0d8": "#f3f6f9",  # cylinder metal, lit band
    "#7d868f": "#b7bfc8",  # cylinder cap
    "#1f6feb": "#0969da",  # marker tag, darker on white
    "#7cc2ff": "#ffffff",  # chant's stamp label, white on the dark mount
    "#7fe888": "#ffffff",  # choudoufu's, likewise - the mount stays dark
    "#ffa657": "#bc4c00",  # AWS orange pills
    "#bc8cff": "#6639ba",  # schema purple
    "#ff7b72": "#cf222e",  # reconciler red
}


def to_light(svg: str) -> str:
    pat = re.compile("|".join(re.escape(k) for k in LIGHT), re.IGNORECASE)
    return pat.sub(lambda m: LIGHT[m.group(0).lower()], svg)


#: LinkedIn crops a feed image to 1.91:1. The heroes are wider than that, so
#: fit each one whole inside the frame with a margin rather than let the sides
#: get cut. 600x314 rendered at 2x is the 1200x628 LinkedIn actually wants.
LI_W, LI_H, LI_PAD = 600, 314, 20


def linkedin(svg: str) -> str:
    """Letterbox a hero into the LinkedIn frame, nothing cropped."""
    w, h = viewbox(svg)
    bg = re.search(r'<rect[^>]*fill="(#[0-9a-fA-F]{6})"', svg).group(1)
    box_w, box_h = LI_W - 2 * LI_PAD, LI_H - 2 * LI_PAD
    scale = min(box_w / w, box_h / h)
    fit_w, fit_h = w * scale, h * scale
    root = re.search(r"<svg[^>]*>", svg, re.S).group(0)
    # font-family is set on the root element, so it has to ride along to the
    # nested one or every label falls back to the default serif.
    font = re.search(r'font-family="([^"]*)"', root)
    font = f' font-family="{font.group(1)}"' if font else ""
    inner = re.sub(r"^.*?<svg[^>]*>", "", svg, count=1, flags=re.S).rsplit("</svg>", 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LI_W} {LI_H}"{font}>'
            f'<rect width="{LI_W}" height="{LI_H}" fill="{bg}"/>'
            f'<svg x="{(LI_W - fit_w) / 2:.1f}" y="{(LI_H - fit_h) / 2:.1f}"'
            f' width="{fit_w:.1f}" height="{fit_h:.1f}" viewBox="0 0 {w} {h}"{font}>'
            f'{inner}</svg></svg>\n')


def viewbox(svg: str) -> tuple[int, int]:
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg)
    return (round(float(m.group(1))), round(float(m.group(2))))


def png(src: Path, dst: Path, w: int, h: int) -> None:
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={w},{h}",
                    f"--screenshot={dst}", f"file://{src}"],
                   check=True, capture_output=True)


def main(argv: list[str]) -> None:
    if argv:
        slug, pairs = argv[0], [tuple(a.split(":", 1)) for a in argv[1:]]
    else:
        slug, pairs = DEFAULT_SLUG, DEFAULT_PAIRS
    out_dir = Path.home() / "Documents" / "blogs" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # Hand-drawn figures exist in the dark palette only; derive each light
    # twin beside its dark original rather than maintain a file that drifts.
    for stem, _ in pairs:
        light = IMG / f"{stem}-light.svg"
        if not light.exists():
            light.write_text(to_light((IMG / f"{stem}.svg").read_text()))

    for stem, name in pairs:
        for suffix, out in (("", name), ("-light", f"{name}-light")):
            src = IMG / f"{stem}{suffix}.svg"
            svg = src.read_text()
            shutil.copyfile(src, out_dir / f"{out}.svg")
            w, h = viewbox(svg)
            png(out_dir / f"{out}.svg", out_dir / f"{out}.png", w, h)
            print(f"  {out}.svg  {out}.png  ({w}x{h} at 2x)")

            if name == "hero":
                li = out_dir / f"{out}-linkedin.svg"
                li.write_text(linkedin(svg))
                png(li, out_dir / f"{out}-linkedin.png", LI_W, LI_H)
                li.unlink()
                print(f"  {out}-linkedin.png  ({LI_W}x{LI_H} at 2x, letterboxed)")


if __name__ == "__main__":
    main(sys.argv[1:])
