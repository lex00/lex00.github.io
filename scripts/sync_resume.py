#!/usr/bin/env python3
"""Build content/_index.md from the résumé markdown.

The résumé lives in the resume_2026 repo and is the single source of truth.
This copies it in and adds the three things the web version has that the PDF
does not: the receipts cards, the run-it-yourself block, and shortcode wrappers
that give the entry sections their hairline separators.

    just sync

Override the source with RESUME_SRC when it moves.
"""

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SRC = (
    REPO.parent.parent.parent
    / "resume_2026"
    / "personas"
    / "infra-platform-engineer"
    / "resume.md"
)
DEST = REPO / "content" / "_index.md"

# Sections whose paragraphs each stand alone, and so get separators.
ENTRY_SECTIONS = {"Also mine", "Before this"}

FRONT_MATTER = """---
title: "Alex Artigues"
description: "Infrastructure engineer. Currently building choudoufu, IAM-governed state for OpenTofu."
---

"""


def split_sections(body):
    """Split markdown into [(heading_or_None, text)] on `## ` boundaries."""
    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    out = [(None, parts[0])]
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def main():
    src = Path(os.environ.get("RESUME_SRC", DEFAULT_SRC))
    if not src.is_file():
        sys.exit(
            f"sync_resume: source not found at {src}\n"
            f"Set RESUME_SRC to the résumé markdown if it has moved."
        )

    sections = split_sections(src.read_text())
    chunks = []

    for heading, text in sections:
        if heading is None:
            # Everything above the first `## `: the name and contact line.
            chunks.append(text.rstrip())
            continue

        text = text.strip()

        # A trailing `---` belongs between sections, not inside the wrapper.
        trailing_rule = ""
        if text.endswith("---"):
            text = text[: -len("---")].rstrip()
            trailing_rule = "\n\n---"

        if heading in ENTRY_SECTIONS:
            text = "{{< entries >}}\n" + text + "\n{{< /entries >}}"

        chunks.append(f"## {heading}\n\n{text}{trailing_rule}")

        # The demo and the cards sit between the choudoufu pitch and the rest.
        if heading.startswith("choudoufu"):
            chunks.append("{{< rundemo >}}")
            chunks.append("{{< receipts >}}")

    DEST.write_text(FRONT_MATTER + "\n\n".join(chunks) + "\n")
    print(f"sync_resume: {src} -> {DEST.relative_to(REPO)}")


if __name__ == "__main__":
    main()
