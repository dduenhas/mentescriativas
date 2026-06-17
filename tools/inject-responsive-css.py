#!/usr/bin/env python3
"""Inject global responsive CSS fixes on all static HTML pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RESPONSIVE_LINK = (
    '<link rel="stylesheet" id="mc-responsive-fixes-css" '
    'href="/assets/css/mc-responsive-fixes.css?ver=1" media="all">'
)

ANCHORS = (
    '<link rel="stylesheet" id="mc-section-monitores-css"',
    '<meta name="viewport"',
    "</head>",
)


def patch_html(text: str) -> tuple[str, bool]:
    if RESPONSIVE_LINK in text:
        return text, False

    for anchor in ANCHORS:
        if anchor in text:
            if anchor == "</head>":
                return text.replace(anchor, RESPONSIVE_LINK + anchor, 1), True
            idx = text.index(anchor)
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = idx + len(anchor)
            else:
                line_end += 1
            return text[:line_end] + RESPONSIVE_LINK + text[line_end:], True

    return text, False


def main() -> None:
    updated = 0
    for fp in sorted(ROOT.rglob("*.html")):
        if "node_modules" in fp.parts:
            continue
        original = fp.read_text(encoding="utf-8", errors="surrogateescape")
        patched, changed = patch_html(original)
        if changed:
            fp.write_text(patched, encoding="utf-8", errors="surrogateescape")
            print(f"updated {fp.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} files")


if __name__ == "__main__":
    main()
