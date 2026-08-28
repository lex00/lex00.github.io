#!/usr/bin/env python3
"""Draw the two data tables in the knr-ops/Crossplane token post as SVG
figures instead of markdown tables, matching gen_bench_table.py's row/rule
style.

    python3 scripts/gen_token_tables.py [path-to-iac-cd-bench]

Writes both themes into static/img/:

    knr-ops-token-tasks.svg / -light.svg     knr-ops vs Crossplane, per task
    knr-ops-token-overall.svg / -light.svg   all seven stacks, avg tokens/run

Same rule as the other generators here: the numbers come from the result set
the post cites (coverage-v10, Claude Haiku 4.5, k=3), read from the run
JSONs rather than typed in by hand.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "img"
RESULTS_DIR = "results/claude-haiku-4-5-coverage-v10"

TASKS = [
    ("T1-comprehend", "comprehend"),
    ("T2-generate", "generate"),
    ("T3-modify", "modify"),
    ("T4-debug", "debug"),
]
STACKS_OVERALL = [
    ("chant", "chant", True),
    ("pulumi-typescript", "pulumi-typescript", False),
    ("crossplane", "Crossplane", False),
    ("bare", "bare", False),
    ("knr-ops", "knr-ops", False),
    ("pulumi-python", "pulumi-python", False),
    ("terraform", "terraform", False),
]

THEMES = {
    "": dict(bg="#0d1117", fg="#e6edf3", dim="#8b949e", knr="#58a6ff",
             chant="#68d391", rule="#30363d"),
    "-light": dict(bg="#ffffff", fg="#1c2128", dim="#57606a", knr="#1f6feb",
                    chant="#1a9850", rule="#d0d7de"),
}

ROW_H = 54
TOP = 128


def load(results: Path) -> dict[tuple[str, str], int]:
    """Average input+output tokens per run, keyed by (stack, task)."""
    totals: dict[tuple[str, str], list[int]] = defaultdict(list)
    for path in results.glob("*/*/*run*.json"):
        r = json.loads(path.read_text())
        tok = r.get("tokens") or {}
        inp, out = tok.get("input"), tok.get("output")
        if inp is None and out is None:
            continue
        totals[(r["stack"], r["task"])].append((inp or 0) + (out or 0))
    return {k: round(sum(vals) / len(vals)) for k, vals in totals.items()}


def draw_tasks(avg: dict[tuple[str, str], int], theme: str) -> str:
    t = THEMES[theme]
    height = TOP + ROW_H * len(TASKS) + 30
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {height}"'
        ' font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="900" height="{height}" fill="{t["bg"]}"/>',
    ]
    for x, label, anchor in (
        (40, "task", ""), (420, "knr-ops", "end"),
        (620, "Crossplane", "end"), (820, "knr-ops saves", "end"),
    ):
        a = f' text-anchor="{anchor}"' if anchor else ""
        svg.append(f'<text x="{x}" y="88" font-size="18" font-weight="700" fill="{t["dim"]}"{a}>{label}</text>')
    svg.append(f'<line x1="40" y1="100" x2="860" y2="100" stroke="{t["rule"]}" stroke-width="1"/>')

    for i, (task_id, label) in enumerate(TASKS):
        y = TOP + ROW_H * i
        k = avg[("knr-ops", task_id)]
        c = avg[("crossplane", task_id)]
        save = 0 if c == 0 else round((c - k) / c * 100)
        save_text = "~0%" if abs(k - c) <= 1 else f"{save}%"
        svg.append(f'<text x="40" y="{y}" font-size="20" font-weight="600" fill="{t["fg"]}">{label}</text>')
        svg.append(f'<text x="420" y="{y}" font-size="20" font-weight="700" fill="{t["knr"]}" text-anchor="end">{k:,}</text>')
        svg.append(f'<text x="620" y="{y}" font-size="20" fill="{t["fg"]}" text-anchor="end">{c:,}</text>')
        svg.append(f'<text x="820" y="{y}" font-size="20" font-weight="700" fill="{t["knr"]}" text-anchor="end">{save_text}</text>')
        if i < len(TASKS) - 1:
            svg.append(f'<line x1="40" y1="{y + 22}" x2="860" y2="{y + 22}" stroke="{t["rule"]}" stroke-width="1" stroke-opacity="0.5"/>')

    svg.append("</svg>")
    return "\n".join(svg) + "\n"


def draw_overall(avg_by_stack: dict[str, int], theme: str) -> str:
    t = THEMES[theme]
    rows = sorted(STACKS_OVERALL, key=lambda r: avg_by_stack[r[0]])
    height = TOP + ROW_H * len(rows) + 30
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 {height}"'
        ' font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="700" height="{height}" fill="{t["bg"]}"/>',
        f'<text x="40" y="88" font-size="18" font-weight="700" fill="{t["dim"]}">stack</text>',
        f'<text x="660" y="88" font-size="18" font-weight="700" fill="{t["dim"]}" text-anchor="end">avg tokens / run</text>',
        f'<line x1="40" y1="100" x2="660" y2="100" stroke="{t["rule"]}" stroke-width="1"/>',
    ]
    for i, (stack_id, label, mine) in enumerate(rows):
        y = TOP + ROW_H * i
        val = avg_by_stack[stack_id]
        fill = t["chant"] if mine else t["fg"]
        weight = "700" if mine else "500"
        svg.append(f'<text x="40" y="{y}" font-size="20" font-weight="{weight}" fill="{fill}">{label}</text>')
        svg.append(f'<text x="660" y="{y}" font-size="20" font-weight="{weight}" fill="{fill}" text-anchor="end">{val:,}</text>')
        if i < len(rows) - 1:
            svg.append(f'<line x1="40" y1="{y + 22}" x2="660" y2="{y + 22}" stroke="{t["rule"]}" stroke-width="1" stroke-opacity="0.5"/>')

    svg.append("</svg>")
    return "\n".join(svg) + "\n"


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Documents/checkouts/iac-cd-bench"
    results = root / RESULTS_DIR
    if not results.is_dir():
        print(f"no results under {results}", file=sys.stderr)
        return 1

    avg = load(results)
    if not avg:
        print("no runs with token counts found", file=sys.stderr)
        return 1

    overall: dict[str, list[int]] = defaultdict(list)
    for (stack, _task), v in avg.items():
        overall[stack].append(v)
    avg_by_stack = {s: round(sum(v) / len(v)) for s, v in overall.items()}

    for theme in THEMES:
        (OUT / f"knr-ops-token-tasks{theme}.svg").write_text(draw_tasks(avg, theme))
        (OUT / f"knr-ops-token-overall{theme}.svg").write_text(draw_overall(avg_by_stack, theme))
        print(f"  ok  knr-ops-token-tasks{theme}.svg")
        print(f"  ok  knr-ops-token-overall{theme}.svg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
