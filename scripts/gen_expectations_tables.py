#!/usr/bin/env python3
"""Draw the four tables in the 2026 expectations post as SVGs.

    python3 scripts/gen_expectations_tables.py

Writes both themes into static/img/, one pair per table:

    expectations-ops.svg / -light.svg          the five Ops and their triggers
    expectations-claims.svg / -light.svg       the pitch, answered per tool

These started as markdown tables. The theme's table CSS is built for a
scorecard - `td:nth-child(n+3)` sets `white-space: nowrap` - and the cells
here hold sentences, so the third column ran off the page. Drawing them
means the type size is a decision rather than whatever the column left over.

Cells are wrapped here rather than by a browser, so the widths below are the
layout. Changing a cell's text can change how many lines it takes; re-run
this and look at the result before assuming it still fits.

Backticked spans render in the monospace face, the same as they would in
prose. Everything else is the system sans the rest of the site uses.
"""

from __future__ import annotations

import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "img"

SANS = "-apple-system, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "": dict(bg="#0d1117", fg="#e6edf3", dim="#8b949e", rule="#30363d",
             mono="#79c0ff", good="#68d391", bad="#ff7b72"),
    "-light": dict(bg="#ffffff", fg="#1c2128", dim="#57606a", rule="#d0d7de",
                   mono="#0550ae", good="#1a7f37", bad="#cf222e"),
}

WIDTH = 1100
MARGIN = 32
GUTTER = 22

BODY = 22.5
HEAD = 20.0
LINE = 31
ROW_PAD = 17
TITLE = 27

#: Rough advance width per character as a fraction of font size. Good enough
#: to wrap on; the alternative is shipping a font metrics table for two faces.
NARROW = set("iljtfrI.,:;'\"!|()[]{}`-")
WIDE = set("mwMW@")


def advance(ch: str, size: float, mono: bool) -> float:
    if mono:
        return size * 0.601
    if ch == " ":
        return size * 0.26
    if ch in NARROW:
        return size * 0.31
    if ch in WIDE:
        return size * 0.86
    if ch.isupper():
        return size * 0.63
    if ch.isdigit():
        return size * 0.55
    return size * 0.52


def measure(text: str, size: float, mono: bool) -> float:
    return sum(advance(c, size, mono) for c in text)


def segments(cell: str) -> list[tuple[str, bool]]:
    """Split a cell into (text, is_mono) runs on backticks."""
    out: list[tuple[str, bool]] = []
    for i, part in enumerate(re.split(r"`([^`]*)`", cell)):
        if part:
            out.append((part, i % 2 == 1))
    return out


def tokenize(cell: str) -> list[tuple[str, bool, bool]]:
    """(word, is_mono, space_before), preserving where spaces actually were.

    A backticked span is one token, so `-exclude`, keeps its comma tight
    instead of drifting a space away from it.
    """
    words: list[tuple[str, bool, bool]] = []
    pending = False
    for text, mono in segments(cell):
        if mono:
            words.append((text, True, pending and bool(words)))
            pending = False
            continue
        for i, piece in enumerate(re.split(r"(\s+)", text)):
            if piece == "":
                continue
            if piece.isspace():
                pending = True
            else:
                words.append((piece, False, pending and bool(words)))
                pending = False
    return words


def wrap(cell: str, width: float,
         size: float) -> list[list[tuple[str, bool, bool]]]:
    """Greedy wrap into lines of (word, is_mono, space_before) runs."""
    lines: list[list[tuple[str, bool, bool]]] = []
    cur: list[tuple[str, bool, bool]] = []
    cur_w = 0.0
    space = advance(" ", size, False)
    for w, mono, sp in tokenize(cell):
        ww = measure(w, size, mono) + (space if sp else 0.0)
        if cur and cur_w + ww > width:
            lines.append(cur)
            cur = [(w, mono, False)]
            cur_w = measure(w, size, mono)
        else:
            cur_w += ww
            cur.append((w, mono, sp))
    if cur:
        lines.append(cur)
    return lines or [[]]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def line_svg(runs: list[tuple[str, bool, bool]], x: float, y: float,
             size: float, fill: str, mono_fill: str, weight: int = 400) -> str:
    if not runs:
        return ""
    spans = []
    for i, (w, mono, sp) in enumerate(runs):
        lead = " " if (sp and i) else ""
        if mono:
            spans.append(
                f'<tspan font-family="{MONO}" font-size="{size * 0.93:.1f}" '
                f'fill="{mono_fill}">{esc(lead + w)}</tspan>'
            )
        else:
            spans.append(f"<tspan>{esc(lead + w)}</tspan>")
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" fill="{fill}"'
            f'{wt} xml:space="preserve">' + "".join(spans) + "</text>\n")


def render(title: str, subtitle: str, cols: list[int], header: list[str],
           rows: list[list[str]], stem: str) -> None:
    usable = WIDTH - 2 * MARGIN
    if sum(cols) != usable:
        raise SystemExit(
            f"{stem}: columns sum to {sum(cols)}, need {usable}. "
            "A wider sum silently runs the last column off the canvas."
        )
    inner = [c - GUTTER for c in cols]
    xs, x = [], MARGIN
    for c in cols:
        xs.append(x)
        x += c

    wrapped = [[wrap(cell, inner[i], BODY) for i, cell in enumerate(row)]
               for row in rows]
    heights = [max(len(c) for c in row) * LINE + ROW_PAD * 2 for row in wrapped]

    top = 74 if not subtitle else 104
    head_y = top + 24
    body_top = top + 48
    height = int(body_top + sum(heights) + 20)

    for suffix, t in THEMES.items():
        p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} '
             f'{height}" font-family="{SANS}">\n',
             f'<rect width="{WIDTH}" height="{height}" fill="{t["bg"]}"/>\n',
             f'<text x="{MARGIN}" y="48" font-size="{TITLE}" font-weight="800" '
             f'fill="{t["fg"]}">{esc(title)}</text>\n']
        if subtitle:
            p.append(f'<text x="{MARGIN}" y="78" font-size="19" '
                     f'fill="{t["dim"]}">{esc(subtitle)}</text>\n')

        for i, h in enumerate(header):
            for ln in wrap(h, inner[i], HEAD):
                p.append(line_svg(ln, xs[i], head_y, HEAD, t["dim"],
                                  t["dim"], weight=700))
        p.append(f'<line x1="{MARGIN}" y1="{head_y + 12}" '
                 f'x2="{WIDTH - MARGIN}" y2="{head_y + 12}" '
                 f'stroke="{t["rule"]}" stroke-width="1"/>\n')

        y = body_top
        for r, row in enumerate(wrapped):
            for i, cell in enumerate(row):
                ty = y + ROW_PAD + BODY
                for ln in cell:
                    p.append(line_svg(ln, xs[i], ty, BODY, t["fg"],
                                      t["mono"]))
                    ty += LINE
            y += heights[r]
            if r < len(wrapped) - 1:
                p.append(f'<line x1="{MARGIN}" y1="{y:.0f}" '
                         f'x2="{WIDTH - MARGIN}" y2="{y:.0f}" '
                         f'stroke="{t["rule"]}" stroke-width="1"/>\n')

        p.append("</svg>\n")
        (OUT / f"{stem}{suffix}.svg").write_text("".join(p))
        print(f"  {stem}{suffix}.svg  ({height}px tall)")


TABLES = [
    dict(
        stem="expectations-ops",
        title="The CI a choudoufu estate needs, as five Ops",
        subtitle="Generated for GitHub, Forgejo and GitLab from one project that builds",
        cols=[200, 180, 656],
        header=["Op and job name", "Trigger", "What it may do"],
        rows=[
            ["`live-check`", "pull request",
             "Nothing. No cloud call, no state, no credential"],
            ["`live-plan`", "pull request",
             "Read the live system, post the plan"],
            ["`live-adopt`", "push to `staging`",
             "Write two tags per adoptable resource, after an approval"],
            ["`live-apply`", "push to `main`",
             "Change the estate, after an approval"],
            ["`live-discover`", "cron",
             "Read the account, open an issue"],
        ],
    ),
    dict(
        stem="expectations-claims",
        title="The 2026 pitch, answered line by line",
        subtitle="Where there is no answer, the cell says so",
        cols=[280, 380, 376],
        header=["The expectation", "choudoufu", "chant"],
        rows=[
            ["Terraform, Ansible and Helm in one governed run",
             "Out of scope",
             "Ops span seventeen lexicons"],
            ["Every change approved before it happens",
             "Re-plans first, exits 3 on drift",
             "The gate is a fact in git"],
            ["Nothing runs off-plan",
             "Holds against drift",
             "Not against an edited root"],
            ["10x scale, thousands of resources",
             "745 against real AWS, at call parity",
             "Synthetic bench to 200"],
            ["Brownfield adoption",
             "`live-adopt`, behind a gate",
             "`carve`, one resource at a time"],
            ["Cost allocation you can trust",
             "The marker is written on create",
             "Nothing"],
            ["One place to see the whole estate",
             "What behold reads",
             "The graph behold renders"],
        ],
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in TABLES:
        print(spec["stem"])
        render(spec["title"], spec["subtitle"], spec["cols"],
               spec["header"], spec["rows"], spec["stem"])


if __name__ == "__main__":
    main()
