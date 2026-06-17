#!/usr/bin/env python3
"""Inject shared Divi link fallback on all static HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LINK_SCRIPT = (
    '<script id="divi-script-library-link-js" '
    'src="/assets/js/divi/includes/builder-5/visual-builder/build/'
    'script-library-link.js?ver=5.7.4"></script>'
)
FALLBACK_SCRIPT = (
    '<script id="mc-divi-links-fallback-js" '
    'src="/assets/js/mc-divi-links-fallback.js?ver=1"></script>'
)

INLINE_FALLBACK_IDS = (
    "biblioteca-pdf-links-js",
    "atividades-divi-links-js",
)

INLINE_BLOCK_RE = re.compile(
    r'<script id="(?:' + "|".join(INLINE_FALLBACK_IDS) + r')">.*?</script>\s*',
    re.DOTALL,
)


def patch_html(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    new_text, removed = INLINE_BLOCK_RE.subn("", text)
    if removed:
        changes.append(f"removed {removed} inline fallback(s)")

    if FALLBACK_SCRIPT in new_text:
        text = new_text
    elif LINK_SCRIPT in new_text:
        new_text = new_text.replace(LINK_SCRIPT, LINK_SCRIPT + FALLBACK_SCRIPT, 1)
        changes.append("injected shared fallback script")
        text = new_text
    elif "diviElementLinkData" in new_text or "et_link_options_data" in new_text:
        changes.append("skipped: link script tag not found")

    return text, changes


def main() -> None:
    updated = 0
    for fp in sorted(ROOT.rglob("*.html")):
        if "node_modules" in fp.parts:
            continue
        original = fp.read_text(encoding="utf-8", errors="surrogateescape")
        patched, changes = patch_html(original)
        if patched != original:
            fp.write_text(patched, encoding="utf-8", errors="surrogateescape")
            print(f"{fp.relative_to(ROOT)}: {', '.join(changes)}")
            updated += 1
    print(f"Done: {updated} files updated")


if __name__ == "__main__":
    main()
