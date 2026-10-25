#!/usr/bin/env python3
"""Draw the two figures in resource-level-concurrency-for-terraform.

    python3 scripts/gen_concurrency_diagrams.py

  - concurrency-lock-scope: what one apply locks, a state file against a
    record per resource;
  - concurrency-scorecard: the three detail tables as one grid of marks.

Palette, page width and PNG export come from the table scripts, so these sit
with the table images: dark PNG to static/img/, light PNG and both SVGs to
~/Documents/blogs/resource-level-concurrency-for-terraform/.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_expectations_tables as tables  # noqa: E402
import gen_vendor_power_tables as vp  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "static/img"
BLOG = Path.home() / "Documents/blogs/resource-level-concurrency-for-terraform"

W = tables.WIDTH
M = tables.MARGIN
SANS = tables.SANS
MONO = tables.MONO

#: Apply A and apply B get their own colour on top of the table palette.
EXTRA = {
    "": dict(a="#79c0ff", b="#d29922", chip="#161b22", warn="#d29922"),
    "-light": dict(a="#0550ae", b="#9a6700", chip="#f6f8fa", warn="#9a6700"),
}

vp.URL = "lex00.github.io/posts/resource-level-concurrency-for-terraform"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=20, fill="#000", weight=400, anchor="start", mono=False):
    fam = f' font-family="{MONO}"' if mono else ""
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{wt}{fam} '
            f'text-anchor="{anchor}">{esc(s)}</text>\n')


def padlock(x, y, colour, bg):
    """A padlock 22 wide and 26 tall, top-left at x, y."""
    return (f'<path d="M{x + 5} {y + 12} v-4 a6 6 0 0 1 12 0 v4" fill="none" '
            f'stroke="{colour}" stroke-width="2.5"/>\n'
            f'<rect x="{x}" y="{y + 11}" width="22" height="15" rx="3" fill="{colour}"/>\n'
            f'<circle cx="{x + 11}" cy="{y + 18}" r="2.2" fill="{bg}"/>\n')


def chip(x, y, name, t, e, who=""):
    """A resource, outlined in the colour of the apply touching it."""
    stroke = {"a": e["a"], "b": e["b"], "ab": t["bad"]}.get(who, t["rule"])
    width = 3 if who else 1.5
    return (f'<rect x="{x}" y="{y}" width="96" height="44" rx="8" fill="{e["chip"]}" '
            f'stroke="{stroke}" stroke-width="{width}"/>\n'
            + text(x + 48, y + 29, name, 19, t["fg"], anchor="middle", mono=True))


#: Two estates, as in the demos: network on the first row, app on the second.
RESOURCES = ["vpc", "subnet", "lb", "db", "queue", "dns"]
TOUCHED = {"db": "a", "subnet": "b"}


def bullet(x, y, colour, line, t, note=""):
    out = (f'<circle cx="{x + 8}" cy="{y - 6}" r="7" fill="{colour}"/>\n'
           + text(x + 24, y, line, 19, t["fg"]))
    if note:
        out += text(x + 24, y + 28, note, 17, t["dim"])
    return out


def lock_scope(t, e, title="") -> tuple[str, int]:
    top = 64 if title else 0
    h = 520 + top
    half = (W - 2 * M) // 2
    lx, rx = M, M + half + 24
    p = [f'<rect width="{W}" height="{h}" fill="{t["bg"]}"/>\n']
    if title:
        p.append(text(M, 52, title, tables.TITLE, t["fg"], 700))

    # Left: one state file, one lock, around everything.
    p.append(text(lx, top + 46, "Terraform or OpenTofu", 24, t["fg"], 600))
    p.append(text(lx, top + 76, "one lock, so two applies can't overwrite one file", 18, t["dim"]))
    box_w = 3 * 96 + 4 * 16
    p.append(f'<rect x="{lx}" y="{top + 104}" width="{box_w}" height="{2 * 44 + 3 * 16 + 30}" '
             f'rx="12" fill="none" stroke="{t["fg"]}" stroke-width="2"/>\n')
    p.append(text(lx + 16, top + 128, "state file", 17, t["dim"]))
    p.append(padlock(lx + box_w - 38, top + 90, t["fg"], t["bg"]))
    for i, r in enumerate(RESOURCES):
        cx = lx + 16 + (i % 3) * 112
        cy = top + 142 + (i // 3) * 60
        p.append(chip(cx, cy, r, t, e, TOUCHED.get(r, "")))
    y = top + 330
    p.append(bullet(lx, y, e["a"], "Apply A changes db and takes the lock", t))
    p.append(bullet(lx, y + 40, e["b"], "Apply B changes subnet and waits", t,
                    "though it touches nothing A does"))
    p.append(bullet(lx, y + 108, t["dim"], "A killed apply holds an S3, GCS or azurerm lock", t,
                    "until someone runs force-unlock"))

    # Right: a record per resource, in two estates, with no lock around either.
    p.append(text(rx, top + 46, "choudoufu", 24, t["fg"], 600))
    p.append(text(rx, top + 76, "applies only collide on the same resource", 18, t["dim"]))
    for row, estate in enumerate(("network", "app")):
        ey = top + 100 + row * 98
        p.append(f'<rect x="{rx}" y="{ey}" width="{box_w}" height="88" rx="10" fill="none" '
                 f'stroke="{t["dim"]}" stroke-width="1.5" stroke-dasharray="6 5"/>\n')
        p.append(text(rx + 14, ey + 22, f"estate {estate}", 15, t["dim"]))
        for i, r in enumerate(RESOURCES[row * 3:row * 3 + 3]):
            p.append(chip(rx + 16 + i * 112, ey + 32, r, t, e, TOUCHED.get(r, "")))
    p.append(bullet(rx, y, e["a"], "Apply A changes db and lands", t))
    p.append(bullet(rx, y + 40, e["b"], "Apply B changes subnet and lands", t))
    p.append(bullet(rx, y + 80, t["bad"], "A stale saved plan on db is refused, naming db", t))
    p.append(bullet(rx, y + 120, t["dim"], "A killed apply leaves nothing to release", t))

    p.append(f'<line x1="{M + half + 4}" y1="{top + 30}" x2="{M + half + 4}" y2="{h - 30}" '
             f'stroke="{t["rule"]}" stroke-width="1"/>\n')
    return "".join(p), h


#: (setup, group, [one plan, changed value, new id, approved plan], applies)
#: A mark is "y", "n" or "p" (partly), with a note under it.
ROWS = [
    ("Stock backends", None),
    ("Terraform or OpenTofu", [("n", "per root"), ("n", "last applied"), ("n", "not yet in state"), ("p", "per root")], "one per root"),
    ("Terragrunt run --all", [("n", "per unit"), ("n", "last applied"), ("p", "as a mock"), ("n", "mock kept")], "one per unit"),
    ("Atmos --affected", [("n", "per component"), ("n", "last applied"), ("p", "as a mock"), ("p", "new value is drift")], "one per component"),
    ("terragucci waves", [("p", "one note"), ("y", "planned outputs"), ("p", "plans again"), ("y", "digest")], "one per wave"),
    ("terragucci waves.compose", [("y", ""), ("y", ""), ("y", ""), ("y", "")], "one"),
    ("choudoufu live backend", None),
    ("terragucci waves.compose", [("y", ""), ("y", ""), ("y", ""), ("y", "")], "one"),
    ("Terragrunt run --all", [("y", ""), ("y", ""), ("y", ""), ("y", "with --out-dir")], "one, saved plans"),
    ("Atmos --affected", [("y", "with dependents"), ("y", ""), ("y", ""), ("y", "verify: warn")], "one per component"),
]

COLUMNS = ["One plan for\nevery root", "A changed value\nreaches readers",
           "A new ID\nreaches readers", "The approved\nplan applies", "Applies"]


def mark(kind, cx, cy, t, e):
    if kind == "y":
        return (f'<path d="M{cx - 9} {cy} l6 7 l12 -14" fill="none" stroke="{t["good"]}" '
                f'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>\n')
    if kind == "n":
        return (f'<path d="M{cx - 7} {cy - 7} l14 14 M{cx + 7} {cy - 7} l-14 14" '
                f'stroke="{t["bad"]}" stroke-width="3.5" stroke-linecap="round"/>\n')
    return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{e["warn"]}" stroke-width="3"/>\n'
            f'<path d="M{cx} {cy - 9} a9 9 0 0 1 0 18 z" fill="{e["warn"]}"/>\n')


def scorecard(t, e, title="") -> tuple[str, int]:
    first = 270
    col = (W - 2 * M - first) // 5
    row_h, group_h = 62, 46
    top = 96
    h = top + sum(group_h if r[1] is None else row_h for r in ROWS) + 70
    p = [f'<rect width="{W}" height="{h}" fill="{t["bg"]}"/>\n']
    for i, name in enumerate(COLUMNS):
        cx = M + first + i * col + col // 2
        for j, line in enumerate(name.split("\n")):
            p.append(text(cx, 40 + j * 24, line, 18, t["dim"], 600, "middle"))
    y = top
    for r in ROWS:
        if r[1] is None:
            p.append(f'<line x1="{M}" y1="{y + 4}" x2="{W - M}" y2="{y + 4}" stroke="{t["rule"]}"/>\n')
            p.append(text(M, y + 34, r[0], 18, t["dim"], 600))
            y += group_h
            continue
        name, marks, applies = r
        p.append(text(M + 14, y + 36, name, 20, t["fg"]))
        for i, (kind, note) in enumerate(marks):
            cx = M + first + i * col + col // 2
            cy = y + (24 if note else 31)
            p.append(mark(kind, cx, cy, t, e))
            if note:
                p.append(text(cx, y + 54, note, 15, t["dim"], anchor="middle"))
        cx = M + first + 4 * col + col // 2
        p.append(text(cx, y + 36, applies, 17, t["fg"], anchor="middle"))
        y += row_h
    lx = M
    ly = h - 26
    for kind, label in (("y", "yes"), ("p", "partly"), ("n", "no")):
        p.append(mark(kind, lx + 10, ly - 6, t, e))
        p.append(text(lx + 28, ly, label, 17, t["dim"]))
        lx += 110
    return "".join(p), h


#: Each case: a title, then per column the network and app plan lines and a
#: note. A line starting "~" or "+" is drawn as a plan diff.
CASES = [
    ("Change a value: network's port goes from 8080 to 8090", [
        ("~ port = 8080 -> 8090", "No changes.", "n", "app read 8080 from state"),
        ("applied", "~ port = 8080 -> 8090", "n", "in a plan nobody reviewed"),
        ("~ port = 8080 -> 8090", "~ port = 8080 -> 8090", "y", "one plan, one apply"),
    ]),
    ("Create something: network adds a subnet, app puts a worker in it", [
        ("+ subnet", '+ subnet_id = "subnet-mock"', "p", "a mock stands in"),
        ("applied", '+ subnet_id = "subnet-0f3c9"', "n", "not the plan you approved"),
        ("+ subnet", "+ subnet_id = (known after apply)", "y", "the plan you approved applies"),
    ]),
]

FLOW_COLUMNS = ["Pull request, stock backend", "Apply, stock backend",
                "Pull request, choudoufu live backend"]


def plan_box(x, y, w, root, line, t, e):
    colour = {"~": e["warn"], "+": t["good"]}.get(line[:1], t["dim"])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="8" fill="{e["chip"]}" '
            f'stroke="{t["rule"]}" stroke-width="1.5"/>\n'
            + text(x + 12, y + 22, root, 15, t["dim"])
            + text(x + 12, y + 48, line, 15, colour, mono=True))


def review_flow(t, e, title="") -> tuple[str, int]:
    top = 64 if title else 0
    gap = 24
    col = (W - 2 * M - 2 * gap) // 3
    # Each case repeats the column heads, so its three columns read on their own.
    case_h = 36 + 34 + 62 + 12 + 62 + 46
    h = top + 20 + len(CASES) * (case_h + 24) + 10
    p = [f'<rect width="{W}" height="{h}" fill="{t["bg"]}"/>\n']
    if title:
        p.append(text(M, 52, title, tables.TITLE, t["fg"], 700))
    y = top + 20
    for n, (heading, cols) in enumerate(CASES):
        if n:
            p.append(f'<line x1="{M}" y1="{y - 12}" x2="{W - M}" y2="{y - 12}" stroke="{t["rule"]}"/>\n')
        p.append(text(M, y + 28, heading, 20, t["fg"], 600))
        for i, name in enumerate(FLOW_COLUMNS):
            p.append(text(M + i * (col + gap), y + 62, name, 16, t["dim"], 600))
        for i, (net, app, kind, note) in enumerate(cols):
            x = M + i * (col + gap)
            by = y + 76
            p.append(plan_box(x, by, col, "network", net, t, e))
            p.append(plan_box(x, by + 74, col, "app", app, t, e))
            p.append(mark(kind, x + 10, by + 162, t, e))
            p.append(text(x + 30, by + 168, note, 17, t["fg"]))
        y += case_h + 24
    return "".join(p), h


TITLE = "Resource-level concurrency for Terraform"


def main() -> None:
    BLOG.mkdir(parents=True, exist_ok=True)
    # Untitled on the site, where the post names it; the light copy stands
    # alone, so the lock diagram carries the post's title there.
    for stem, draw, title in (("concurrency-lock-scope", lock_scope, TITLE),
                              ("concurrency-scorecard", scorecard, ""),
                              ("concurrency-review-flow", review_flow, "")):
        for suffix, t in tables.THEMES.items():
            body, h = draw(t, EXTRA[suffix], title if suffix else "")
            svg = BLOG / f"{stem}{suffix}.svg"
            svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" '
                           f'font-family="{SANS}">\n<rect width="{W}" height="{h}" fill="{t["bg"]}"/>\n'
                           f'{body}</svg>\n')
            dest = SITE / f"{stem}.png" if suffix == "" else BLOG / f"{stem}{suffix}.png"
            vp.png(svg, dest, vp.add_footer(svg, t))
            print(f"  wrote {dest}")


if __name__ == "__main__":
    main()
