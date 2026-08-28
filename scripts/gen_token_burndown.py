#!/usr/bin/env python3
"""Draw the hero for the knr-ops/Crossplane token post: knr-ops vs Crossplane,
per task type, with chant alongside as a quieter third bar.

    python3 scripts/gen_token_burndown.py [path-to-iac-cd-bench]

Writes both themes into static/img/:

    knr-ops-token-burndown-cover.svg        dark
    knr-ops-token-burndown-cover-light.svg  light

The post's headline is knr-ops beating Crossplane on the four task types
where an agent does the work (comprehend, generate, modify, debug) -- it
loses the other two, and chant beats both overall, which is the post's
buried lede, not its headline. chant is drawn here too, but at regular
weight in its own muted-from-the-lead-pair green, third in each cluster
rather than first: visible enough to foreshadow the lede, not loud enough
to read as the chart's actual claim. knr-ops stays the one bold, accented
bar, because it's what the title says beats Crossplane.

Same rule as gen_bench_table.py: the numbers come from the result set the
post cites (coverage-v10, Claude Haiku 4.5, k=3), read straight out of the
run JSONs rather than typed in by hand.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "img"
STEM = "knr-ops-token-burndown-cover"
RESULTS_DIR = "results/claude-haiku-4-5-coverage-v10"

#: Stack id, legend label, and per-theme fill key. Order is draw order within
#: each cluster: knr-ops leads (the headline), Crossplane follows (what it
#: beats), chant trails (the buried lede).
STACKS = [
    ("knr-ops", "knr-ops", "knr"),
    ("crossplane", "Crossplane", "cp"),
    ("chant", "chant", "chant"),
]
TASKS = [
    ("T1-comprehend", "comprehend"),
    ("T2-generate", "generate"),
    ("T3-modify", "modify"),
    ("T4-debug", "debug"),
]

THEMES = {
    "": dict(bg="#0d1117", fg="#e6edf3", dim="#8b949e",
             knr="#58a6ff", knr_text="#58a6ff",
             cp="#30363d", cp_text="#8b949e",
             chant="#3d7a57", chant_text="#7fb894",
             rule="#21262d"),
    "-light": dict(bg="#ffffff", fg="#1c2128", dim="#57606a",
                    knr="#1f6feb", knr_text="#1f6feb",
                    cp="#d0d7de", cp_text="#57606a",
                    chant="#a8dcbc", chant_text="#2f7a4d",
                    rule="#eaeef2"),
}

CHART_LEFT = 160
CHART_RIGHT = 1140
CHART_TOP = 220
CHART_BOTTOM = 560
BAR_W = 44
BAR_GAP = 8


def avg_tokens(results: Path) -> dict[tuple[str, str], int]:
    """Average input+output tokens per run, keyed by (stack, task)."""
    wanted = {s for s, *_ in STACKS}
    totals: dict[tuple[str, str], list[int]] = defaultdict(list)
    for path in results.glob("*/*/*run*.json"):
        r = json.loads(path.read_text())
        stack = r.get("stack")
        if stack not in wanted:
            continue
        tok = r.get("tokens") or {}
        inp, out = tok.get("input"), tok.get("output")
        if inp is None and out is None:
            continue
        totals[(stack, r["task"])].append((inp or 0) + (out or 0))
    return {k: round(sum(vals) / len(vals)) for k, vals in totals.items()}


def draw(avg: dict[tuple[str, str], int], theme: str) -> str:
    t = THEMES[theme]
    values = [avg[(s, task_id)] for task_id, _ in TASKS for s, *_ in STACKS if (s, task_id) in avg]
    top_val = max(values) * 1.12
    scale = (CHART_BOTTOM - CHART_TOP) / top_val

    n = len(TASKS)
    k = len(STACKS)
    cluster_w = k * BAR_W + (k - 1) * BAR_GAP
    span = CHART_RIGHT - CHART_LEFT
    cluster_gap = (span - n * cluster_w) / (n + 1)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"'
        ' font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="1280" height="720" fill="{t["bg"]}"/>',
        f'<text x="640" y="70" font-size="18" font-weight="700" letter-spacing="5"'
        f' fill="{t["dim"]}" text-anchor="middle">TOKEN CONSUMPTION, PER RUN</text>',
        f'<text x="640" y="122" font-size="46" font-weight="800" fill="{t["fg"]}"'
        ' text-anchor="middle">knr-ops beats Crossplane on the token bill</text>',
        f'<text x="640" y="158" font-size="19" fill="{t["dim"]}" text-anchor="middle">'
        "the four task types where an agent does the work &#183; k=3</text>",
    ]

    # Legend
    lx = 370
    for stack_id, label, key in STACKS:
        svg.append(f'<rect x="{lx}" y="182" width="18" height="18" rx="3" fill="{t[key]}"/>')
        svg.append(f'<text x="{lx + 26}" y="197" font-size="16" fill="{t["fg"]}">{label}</text>')
        lx += 26 + 8.5 * len(label) + 34

    svg.append(
        f'<line x1="{CHART_LEFT}" y1="{CHART_BOTTOM}" x2="{CHART_RIGHT}" y2="{CHART_BOTTOM}"'
        f' stroke="{t["rule"]}" stroke-width="1"/>'
    )

    for i, (task_id, label) in enumerate(TASKS):
        cx = CHART_LEFT + cluster_gap * (i + 1) + cluster_w * i
        for j, (stack_id, _, key) in enumerate(STACKS):
            val = avg.get((stack_id, task_id))
            if val is None:
                continue
            h = val * scale
            x = cx + j * (BAR_W + BAR_GAP)
            y = CHART_BOTTOM - h
            fill = t[key]
            text_fill = t[f"{key}_text"] if f"{key}_text" in t else t["fg"]
            weight = "700" if stack_id == "knr-ops" else "500"
            svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{BAR_W}" height="{h:.1f}" rx="4" fill="{fill}"/>')
            svg.append(
                f'<text x="{x + BAR_W / 2:.1f}" y="{y - 10:.1f}" font-size="15" font-weight="{weight}"'
                f' fill="{text_fill}" text-anchor="middle">{val:,}</text>'
            )
        svg.append(
            f'<text x="{cx + cluster_w / 2:.1f}" y="{CHART_BOTTOM + 34}" font-size="19"'
            f' font-weight="600" fill="{t["fg"]}" text-anchor="middle">{label}</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg) + "\n"


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Documents/checkouts/iac-cd-bench"
    results = root / RESULTS_DIR
    if not results.is_dir():
        print(f"no results under {results}", file=sys.stderr)
        return 1

    avg = avg_tokens(results)
    if not avg:
        print("no runs with token counts found", file=sys.stderr)
        return 1

    for theme in THEMES:
        path = OUT / f"{STEM}{theme}.svg"
        path.write_text(draw(avg, theme))
        print(f"  ok  {path.name}")

    print("\nknr-ops / crossplane / chant, per task:")
    for task_id, label in TASKS:
        row = "  ".join(f"{s}={avg.get((s, task_id), 0):,}" for s, *_ in STACKS)
        print(f"  {label:<12} {row}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
