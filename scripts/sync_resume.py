#!/usr/bin/env python3
"""Copy the resume PDF into static/ so the home page can offer it as a download.

The resume is built in the resume_2026 repo:

    pandoc resume.md --section-divs -o resume.pdf \
        --pdf-engine=weasyprint --css=resume.css

Then, from this repo:

    just sync

Override the source with RESUME_SRC when it moves. The destination name is
what the visitor's browser saves, so it carries a full name rather than
"resume.pdf".
"""

import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SRC = (
    REPO.parent.parent.parent
    / "resume_2026"
    / "personas"
    / "infra-platform-engineer"
    / "resume.pdf"
)
DEST = REPO / "static" / "alex-artigues-resume.pdf"


def main():
    src = Path(os.environ.get("RESUME_SRC", DEFAULT_SRC))
    if not src.is_file():
        sys.exit(
            f"sync_resume: source not found at {src}\n"
            f"Build the PDF first, or set RESUME_SRC if it has moved."
        )

    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, DEST)

    kb = DEST.stat().st_size / 1024
    print(f"sync_resume: {src} -> {DEST.relative_to(REPO)} ({kb:.0f} KB)")


if __name__ == "__main__":
    main()
