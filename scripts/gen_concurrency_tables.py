#!/usr/bin/env python3
"""Draw the tables in resource-level-concurrency-for-terraform as images.

    python3 scripts/gen_concurrency_tables.py

The source is scripts/data/resource-level-concurrency-tables.md. Drawing,
footer, PNG export and the links list come from gen_vendor_power_tables, so
these images match that post's: dark PNG to static/img/ for the post, light
PNG and both SVGs to ~/Documents/blogs/resource-level-concurrency-for-terraform/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_expectations_tables as tables  # noqa: E402
import gen_vendor_power_tables as vp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts/data/resource-level-concurrency-tables.md"
SITE = ROOT / "static/img"
BLOG = Path.home() / "Documents/blogs/resource-level-concurrency-for-terraform"

#: (heading in the source, image stem, column widths summing to 1036)
WANTED = [
    ("Stock backends", "concurrency-stock-table", [196, 310, 260, 270]),
    ("terragucci on stock backends", "concurrency-terragucci-table", [236, 400, 400]),
    ("choudoufu live backend", "concurrency-choudoufu-table", [196, 280, 280, 280]),
]

# add_footer reads the address from its own module.
vp.URL = "lex00.github.io/posts/resource-level-concurrency-for-terraform"


def main() -> None:
    BLOG.mkdir(parents=True, exist_ok=True)
    tables.OUT = BLOG
    text = SOURCE.read_text()
    for heading, stem, cols in WANTED:
        rows = vp.table_after(heading, text)
        plain = [[vp.LINK.sub(r"\1", c) for c in r] for r in rows]
        # Untitled on the site, where the post's heading names it; titled for
        # the standalone light copy.
        for title, dest_for in (("", lambda sfx: SITE / f"{stem}.png" if sfx == "" else None),
                                (heading, lambda sfx: BLOG / f"{stem}{sfx}.png" if sfx else None)):
            tables.render(title, "", cols, plain[0], plain[1:], stem)
            for suffix, theme in tables.THEMES.items():
                dest = dest_for(suffix)
                if dest is None:
                    continue
                svg = BLOG / f"{stem}{suffix}.svg"
                vp.png(svg, dest, vp.add_footer(svg, theme))
                print(f"  wrote {dest}")
        print(f"\n<!-- links for {heading} -->\n{vp.links(rows)}\n")


if __name__ == "__main__":
    main()
