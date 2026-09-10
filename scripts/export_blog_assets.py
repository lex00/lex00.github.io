#!/usr/bin/env python3
"""Export this post's figures to ~/Documents/blogs/<slug>/, dark and light, SVG and PNG.

    python3 scripts/export_blog_assets.py

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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "static" / "img"
SLUG = "infra-tooling-expectations-in-2026"
OUT = Path.home() / "Documents" / "blogs" / SLUG

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
}

PAIRS = [("expectations-hero", "hero"),
         ("expectations-claims", "claims"),
         ("expectations-ops", "ops")]


def to_light(svg: str) -> str:
    pat = re.compile("|".join(re.escape(k) for k in LIGHT), re.IGNORECASE)
    return pat.sub(lambda m: LIGHT[m.group(0).lower()], svg)


def viewbox(svg: str) -> tuple[int, int]:
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', svg)
    return (round(float(m.group(1))), round(float(m.group(2))))


def png(src: Path, dst: Path, w: int, h: int) -> None:
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={w},{h}",
                    f"--screenshot={dst}", f"file://{src}"],
                   check=True, capture_output=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # The hero has no generated light twin; derive it beside the dark one.
    hero = IMG / "expectations-hero.svg"
    (IMG / "expectations-hero-light.svg").write_text(to_light(hero.read_text()))

    for stem, name in PAIRS:
        for suffix, out in (("", name), ("-light", f"{name}-light")):
            src = IMG / f"{stem}{suffix}.svg"
            svg = src.read_text()
            shutil.copyfile(src, OUT / f"{out}.svg")
            w, h = viewbox(svg)
            png(OUT / f"{out}.svg", OUT / f"{out}.png", w, h)
            print(f"  {out}.svg  {out}.png  ({w}x{h} at 2x)")


if __name__ == "__main__":
    main()
