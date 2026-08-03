#!/usr/bin/env python3
"""Draw the aws-bench scenario 1 board from chant-bench's published results.

    python3 scripts/gen_bench_table.py [path-to-chant-bench]

Writes both themes into static/img/:

    aws-bench-s1-wrap-table-metrics.svg        dark
    aws-bench-s1-wrap-table-metrics-light.svg  light

These were hand-drawn SVGs, and by the third re-run they disagreed with the
board they were describing — an arm had been added that the picture did not
have, and every figure in it came from a run set two generations old. The post
around them says the results live where they are generated, which was true of
everything except its own headline image.

So the numbers come from the same result sets the site renders, under the same
rule: an arm is judged on its most recent runs that passed every gate, all of
them are shown in the correct column, and the middle one sets the figures it is
ranked on. Adding an arm or re-running the matrix changes the picture by
re-running this.

chant is listed first and marked unranked rather than being placed by its score.
It is the tool the author builds, and putting it at the top of a table it would
top anyway reads as a thumb on the scale; saying so is cheaper than pretending
the ranking is disinterested. The crowns mark the best of the rest per column.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "img"
STEM = "aws-bench-s1-wrap-table-metrics"

#: Display name and swatch per arm, in the order the table lists them after
#: chant. An arm absent from the results is skipped rather than drawn empty.
#:
#: `alchemy-effect` is deliberately not here. It is published on chant-bench and
#: this picture is the six-arm board the post was written around; adding a row
#: would change what the post argues, which is an editorial call and not one a
#: drawing script should make on its own. Add the tuple when the post is ready
#: for it.
ARMS = [
    ("chant", "chant", "#68d391", None),
    ("bare", "no tool", "#8b949e", "aws cli"),
    ("pulumi", "pulumi", "#ef7fc4", None),
    ("terraform", "terraform", "#b183e0", None),
    ("cdk", "aws cdk", "#ffa657", None),
    ("alchemy", "alchemy", "#e3b341", None),
]

THEMES = {
    "": dict(bg="#0d1117", fg="#e6edf3", dim="#8b949e", rule="#30363d", crown="#e3b341"),
    "-light": dict(bg="#ffffff", fg="#1c2128", dim="#57606a", rule="#d0d7de", crown="#9a6700"),
}

ROW_H = 54
TOP = 158


def valid(r: dict) -> bool:
    g = r.get("gates", {})
    return bool(g.get("audit")) and bool(g.get("complete")) and not g.get("tool_missing")


#: How many recent runs an arm is judged on, matching chant-bench.
REPLICATES = 3


def headline(results: Path) -> dict[str, list[dict]]:
    """Each arm's most recent valid runs, newest first.

    A list rather than one run, because one run does not decide anything here:
    at three attempts a question these arms move about three trials in 24 with
    nothing changed. The site ranks on the middle of the set and prints all of
    it, and this picture has to agree with the site or it is worse than no
    picture.
    """
    by_arm: dict[str, list[dict]] = {}
    for path in results.glob("*.json"):
        r = json.loads(path.read_text())
        if r.get("scenario") == "ec2-multiregion" and valid(r):
            by_arm.setdefault(r["arm"], []).append(r)
    out = {}
    for arm, runs in by_arm.items():
        runs.sort(key=lambda r: (r["run"].get("finished_at") or "", r["run"]["id"]), reverse=True)
        out[arm] = runs[:REPLICATES]
    return out


def middle(runs: list[dict], get) -> float | None:
    """The median of `get` over an arm's replicate set."""
    vals = sorted(v for v in (get(r) for r in runs) if isinstance(v, (int, float)))
    return vals[len(vals) // 2] if vals else None


def crown(x: float, y: float, t: dict) -> str:
    return (
        f'<g transform="translate({x:g} {y:g}) scale(0.4)">\n'
        f'<path d="M-22,12 L-22,-5 L-10,2 L0,-13 L10,2 L22,-5 L22,12 Z" fill="{t["crown"]}"'
        f' stroke="{t["bg"]}" stroke-width="2.5" stroke-linejoin="round"/>\n'
        + "".join(
            f'<circle cx="{cx}" cy="{cy}" r="2.8" fill="{t["crown"]}"'
            f' stroke="{t["bg"]}" stroke-width="1.6"/>\n'
            for cx, cy in ((-22, -7), (0, -15), (22, -7))
        )
        + "</g>\n"
    )


def wins_cell(x: float, y: float, labels: list[str], t: dict) -> str:
    """`cost ♛ · input ♛` — a label then a crown, repeated."""
    out, cursor = "", x
    for i, label in enumerate(labels):
        if i:
            out += f'<text x="{cursor:g}" y="{y:g}" font-size="16" fill="{t["dim"]}">·</text>\n'
            cursor += 13
        out += f'<text x="{cursor:g}" y="{y:g}" font-size="16" fill="{t["dim"]}">{label}</text>\n'
        cursor += 8.2 * len(label) + 5
        out += crown(cursor + 10, y - 6, t)
        cursor += 30
    return out


def draw(runs: dict[str, dict], theme: str) -> str:
    t = THEMES[theme]
    rows = [(a, label, colour, note) for a, label, colour, note in ARMS if a in runs]
    ranked = [r for r in rows if r[0] != "chant"]

    def cost_per_correct(arm: str) -> float:
        return middle(runs[arm], lambda r: r["effort"]["cost_usd"] / r["score"]["pass_rate"])

    ranked.sort(key=lambda r: cost_per_correct(r[0]))
    rows = [r for r in rows if r[0] == "chant"] + ranked

    # Best of the rest, per column. chant is excluded: it is marked "wins all"
    # rather than competing for crowns it would take in every column.
    field = [a for a, *_ in ranked]
    tin = lambda a: middle(runs[a], lambda r: r["effort"]["tokens_in"])       # noqa: E731
    tout = lambda a: middle(runs[a], lambda r: r["effort"]["tokens_out"])     # noqa: E731
    got = lambda a: middle(runs[a], lambda r: r["score"]["passed"])           # noqa: E731
    best = {
        "cost": min(field, key=cost_per_correct),
        "input": min(field, key=tin),
        "output": min(field, key=tout),
        "correct": max(field, key=got),
    }

    height = TOP + ROW_H * len(rows) + 30
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}"'
        ' font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="1200" height="{height}" fill="{t["bg"]}"/>',
        f'<text x="600" y="48" font-size="24" font-weight="800" fill="{t["fg"]}"'
        ' text-anchor="middle">aws-bench scenario 1 · ranked by cost per correct answer</text>',
        f'<text x="600" y="78" font-size="15" fill="{t["dim"]}" text-anchor="middle">'
        "eight questions · k=3 · tokens per question</text>",
    ]
    for x, label, anchor in (
        (60, "configuration", ""), (400, "correct", "end"), (530, "$ / correct", "end"),
        (650, "input", "end"), (765, "output", "end"), (810, "wins", ""),
    ):
        a = f' text-anchor="{anchor}"' if anchor else ""
        svg.append(
            f'<text x="{x}" y="128" font-size="18" font-weight="700" fill="{t["dim"]}"{a}>{label}</text>'
        )
    svg.append(crown(872, 122, t).rstrip())
    svg.append(f'<line x1="40" y1="140" x2="1160" y2="140" stroke="{t["rule"]}" stroke-width="1"/>')

    for i, (arm, label, colour, note) in enumerate(rows):
        y = TOP + ROW_H * i + 14
        mine = arm == "chant"
        weight = "700" if mine else "500"
        value_fill = colour if mine else t["fg"]

        svg.append(f'<rect x="60" y="{y - 14}" width="14" height="14" rx="3" fill="{colour}"/>')
        svg.append(
            f'<text x="84" y="{y}" font-size="20" font-weight="700" fill="{colour}">{label}</text>'
        )
        if note:
            svg.append(f'<text x="180" y="{y}" font-size="14" fill="{t["dim"]}">{note}</text>')
        # Every run in the set for the score, the middle one for the rest. The
        # spread is the point: 22 · 24 · 22 and 13 · 18 · 15 are different kinds
        # of result and a single number hides that.
        scores = " · ".join(str(x["score"]["passed"]) for x in runs[arm])
        # The score cell carries three numbers now, so it draws a step smaller
        # than the single figures beside it and drops the "/24" the header and
        # subtitle already imply.
        for x, text in (
            (400, scores),
            (530, f'${cost_per_correct(arm):.3f}'),
            (650, f'{tin(arm) / 1000:.0f}k'),
            (765, f'{tout(arm) / 1000:.1f}k'),
        ):
            svg.append(
                f'<text x="{x}" y="{y}" font-size="20" font-weight="{weight}"'
                f' fill="{value_fill}" text-anchor="end">{text}</text>'
            )

        if mine:
            svg.append(
                f'<text x="810" y="{y}" font-size="20" fill="{t["dim"]}">unranked · wins all</text>'
            )
        else:
            won = [k for k, a in best.items() if a == arm]
            if won:
                svg.append(wins_cell(810, y, won, t).rstrip())
            else:
                svg.append(f'<text x="810" y="{y}" font-size="20" fill="{t["dim"]}">—</text>')

    svg.append("</svg>")
    return "\n".join(svg) + "\n"


def main() -> int:
    bench = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "checkouts/intentius/chant-bench"
    results = bench / "results"
    if not results.is_dir():
        print(f"no results/ under {bench}", file=sys.stderr)
        return 1

    runs = headline(results)
    if not runs:
        print("no valid runs found", file=sys.stderr)
        return 1

    for theme in THEMES:
        path = OUT / f"{STEM}{theme}.svg"
        path.write_text(draw(runs, theme))
        print(f"  ok  {path.name}")
    print("\nruns per arm (newest first):")
    for arm, rs in sorted(runs.items()):
        scores = " · ".join(f"{x['score']['passed']}" for x in rs)
        print(f"  {arm:<16} {scores:<16} of {rs[0]['score']['trials']}   ({', '.join(x['run']['id'] for x in rs)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
