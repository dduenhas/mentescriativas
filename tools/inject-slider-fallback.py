#!/usr/bin/env python3
"""Inject blog post slider fallback CSS/JS on pages with et_pb_post_slider."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS_LINK = (
    '<link rel="stylesheet" id="mc-blog-slider-css" '
    'href="/assets/css/mc-blog-slider.css?ver=1" media="all">'
)
SLIDER_SCRIPT = (
    '<script id="divi-script-library-slider-js" '
    'src="/assets/js/divi/includes/builder-5/visual-builder/build/'
    'script-library-slider.js?ver=5.7.4"></script>'
)
FALLBACK_SCRIPT = (
    '<script id="mc-slider-fallback-js" '
    'src="/assets/js/mc-slider-fallback.js?ver=1"></script>'
)

HEAD_ANCHORS = (
    '<link rel="stylesheet" id="mc-responsive-fixes-css"',
    '<link rel="stylesheet" id="mc-section-monitores-css"',
    '<meta name="viewport"',
    "</head>",
)


def inject_css(text: str) -> tuple[str, bool]:
    if CSS_LINK in text:
        return text, False

    for anchor in HEAD_ANCHORS:
        if anchor in text:
            if anchor == "</head>":
                return text.replace(anchor, CSS_LINK + anchor, 1), True
            idx = text.index(anchor)
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = idx + len(anchor)
            else:
                line_end += 1
            return text[:line_end] + CSS_LINK + text[line_end:], True

    return text, False


def inject_js(text: str) -> tuple[str, bool]:
    if FALLBACK_SCRIPT in text:
        return text, False

    if SLIDER_SCRIPT in text:
        return text.replace(SLIDER_SCRIPT, SLIDER_SCRIPT + FALLBACK_SCRIPT, 1), True

    if "mc-divi-links-fallback-js" in text:
        needle = (
            '<script id="mc-divi-links-fallback-js" '
            'src="/assets/js/mc-divi-links-fallback.js?ver=1"></script>'
        )
        if needle in text:
            return text.replace(needle, needle + FALLBACK_SCRIPT, 1), True

    if "</body>" in text:
        return text.replace("</body>", FALLBACK_SCRIPT + "</body>", 1), True

    return text, False


def patch_html(text: str) -> tuple[str, list[str]]:
    if 'class="et_pb_post_slider' not in text:
        return text, []

    changes: list[str] = []
    patched, css_changed = inject_css(text)
    if css_changed:
        changes.append("injected slider CSS")

    patched, js_changed = inject_js(patched)
    if js_changed:
        changes.append("injected slider JS")

    return patched, changes


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
