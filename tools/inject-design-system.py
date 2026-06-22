#!/usr/bin/env python3
"""Inject mc-design-system.css on all static HTML pages (loads last among mc-* CSS)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "mc-design-system-css"
DESIGN_CSS = (
    '<link rel="stylesheet" id="mc-design-system-css" '
    'href="/assets/css/mc-design-system.css?ver=1" media="all">'
)

ANCHORS = [
    "mc-blog-slider-css",
    "mc-section-monitores-css",
    "mc-responsive-fixes-css",
    "mc-a11y-seo-css",
    "mc-fonts-css",
]

LINK_RE = re.compile(
    r'(<link rel="stylesheet" id="([^"]+)"[^>]*>)',
    re.I,
)


def inject_design_system(text: str) -> str:
    if MARKER in text:
        return text

    last_match = None
    for match in LINK_RE.finditer(text):
        link_id = match.group(2)
        if link_id in ANCHORS or link_id.startswith("mc-"):
            last_match = match

    if last_match:
        insert_at = last_match.end()
        return text[:insert_at] + DESIGN_CSS + text[insert_at:]

    bundle = f"<!-- {MARKER} -->\n{DESIGN_CSS}\n"
    if "<!-- mc-a11y-seo-bundle -->" in text:
        return text.replace(
            "<!-- mc-a11y-seo-bundle -->",
            f"<!-- mc-a11y-seo-bundle -->\n{DESIGN_CSS}",
            1,
        )
    return text.replace("</head>", bundle + "</head>", 1)


def main() -> None:
    updated = 0
    for fp in sorted(ROOT.rglob("*.html")):
        if "node_modules" in fp.parts or "tools" in fp.parts or "backup" in fp.parts:
            continue
        original = fp.read_text(encoding="utf-8", errors="surrogateescape")
        patched = inject_design_system(original)
        if patched != original:
            fp.write_text(patched, encoding="utf-8", errors="surrogateescape")
            print(f"updated {fp.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} files")


if __name__ == "__main__":
    main()
