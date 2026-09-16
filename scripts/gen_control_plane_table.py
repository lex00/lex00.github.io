#!/usr/bin/env python3
"""Draw the summary table in the infecting-abstractions post as an SVG.

    python3 scripts/gen_control_plane_table.py

Writes both themes into static/img/:

    what-each-answer-leaves.svg / -light.svg

Same reason as the expectations tables: the theme's table CSS is a scorecard.
`td:nth-child(n+3)` is `white-space: nowrap`, and `th` is too, so a header or a
third column holding a sentence runs off the page. Both of the columns here
hold phrases, so the table gets drawn rather than marked up.

Rendering is `gen_expectations_tables.render`, imported rather than copied, so
the two tables cannot drift apart on type size, wrapping or palette.

Columns must sum to 1036 (the 1100 canvas less both margins); render() refuses
otherwise instead of letting the last column run off the edge.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_expectations_tables import render  # noqa: E402

TABLE = dict(
    stem="what-each-answer-leaves",
    title="",
    subtitle="",
    cols=[290, 336, 410],
    header=["Where opinions live", "What it invents", "What you operate"],
    rows=[
        ["Kro · Crossplane · Kratix", "a CRD and a controller", "a cluster"],
        ["Helm · Timoni · Score", "a values format", "a format and a state file"],
        ["ConfigHub", "desired state as rows", "a store kept correct"],
        ["chant", "nothing", "the platform's own spec"],
    ],
)


def main() -> None:
    print(TABLE["stem"])
    render(TABLE["title"], TABLE["subtitle"], TABLE["cols"],
           TABLE["header"], TABLE["rows"], TABLE["stem"])


if __name__ == "__main__":
    main()
