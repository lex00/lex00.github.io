#!/usr/bin/env python3
"""Draw the tables in tf-vendor-power-without-the-saas as images.

    python3 scripts/gen_vendor_power_tables.py

The post shows its tables as PNGs so they paste into places that drop an
HTML table, such as LinkedIn. The source is scripts/data/tf-vendor-power-
tables.md, written as markdown tables with their links. This script:

  - draws each table with `gen_expectations_tables.render`, so the type and
    palette match the other table images on the site, and puts the post's
    address under the last row;
  - writes the dark PNG to static/img/ for the post, and the light PNG (with
    both SVGs) to ~/Documents/blogs/tf-vendor-power-without-the-saas/;
  - prints, for each table, the markdown list of its links, which goes under
    the image in the post so every cell can still be checked.

PNGs are rendered with headless Chrome at 2x.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_expectations_tables as tables  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts/data/tf-vendor-power-tables.md"
SITE = ROOT / "static/img"
BLOG = Path.home() / "Documents/blogs/tf-vendor-power-without-the-saas"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

#: (heading in the source, image stem, column widths summing to 1036)
WANTED = [
    ("What you'd pay a SaaS for", "tf-vendor-power-saas-table", [336, 700]),
    ("State and locking", "tf-vendor-power-state-table", [336, 380, 320]),
    ("The detail", "tf-vendor-power-detail-table", [236, 400, 400]),
]

URL = "lex00.github.io/posts/tf-vendor-power-without-the-saas"
FOOT = 56
LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def table_after(heading: str, text: str) -> list[list[str]]:
    start = text.index(f"## {heading}\n")
    rows = []
    for l in text[start:].splitlines()[1:]:
        if l.startswith("|"):
            rows.append([c.strip() for c in l.strip("|").split("|")])
        elif rows:
            break
    return [rows[0]] + rows[2:]  # header, then skip the |---| row


def add_footer(svg: Path, theme: dict[str, str]) -> int:
    """Grow the canvas, put the post's address under the last row, return the height."""
    text = svg.read_text()
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', text).groups())
    text = text.replace(f'viewBox="0 0 {w} {h}"', f'viewBox="0 0 {w} {h + FOOT}"', 1)
    text = text.replace(f'height="{h}" fill', f'height="{h + FOOT}" fill', 1)
    foot = (f'<line x1="{tables.MARGIN}" y1="{h + 4}" x2="{w - tables.MARGIN}" y2="{h + 4}" '
            f'stroke="{theme["rule"]}" stroke-width="1"/>\n'
            f'<text x="{tables.MARGIN}" y="{h + 38}" font-size="19" fill="{theme["dim"]}">'
            f'Links and sources: <tspan fill="{theme["mono"]}">{URL}</tspan></text>\n')
    svg.write_text(text.replace("</svg>", foot + "</svg>"))
    return h + FOOT


def png(svg: Path, dest: Path, height: int) -> None:
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={tables.WIDTH},{height}",
                    f"--screenshot={dest}", f"file://{svg}"],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def links(rows: list[list[str]]) -> str:
    """One line per row that has links: the row's name, then each link."""
    out = []
    for row in rows[1:]:
        found = [f"[{t}]({u})" for cell in row[1:] for t, u in LINK.findall(cell)]
        if found:
            name = LINK.sub(r"\1", row[0])
            out.append(f"- {name}: " + ", ".join(found))
    return "\n".join(out)


def main() -> None:
    BLOG.mkdir(parents=True, exist_ok=True)
    tables.OUT = BLOG
    text = SOURCE.read_text()
    for heading, stem, cols in WANTED:
        rows = table_after(heading, text)
        plain = [[LINK.sub(r"\1", c) for c in r] for r in rows]
        # The post's heading already names the table, so the site image goes
        # without a title; a LinkedIn image stands alone and keeps one.
        for title, dest_for in (("", lambda sfx: SITE / f"{stem}.png" if sfx == "" else None),
                                (heading, lambda sfx: BLOG / f"{stem}{sfx}.png" if sfx else None)):
            tables.render(title, "", cols, plain[0], plain[1:], stem)
            for suffix, theme in tables.THEMES.items():
                dest = dest_for(suffix)
                if dest is None:
                    continue
                svg = BLOG / f"{stem}{suffix}.svg"
                png(svg, dest, add_footer(svg, theme))
                print(f"  wrote {dest}")
        print(f"\n<!-- links for {heading} -->\n{links(rows)}\n")


if __name__ == "__main__":
    main()
