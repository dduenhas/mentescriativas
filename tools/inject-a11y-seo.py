#!/usr/bin/env python3
"""Inject SEO, a11y, and performance head/body fixes on all static HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://mentescriativas.educar.workers.dev"
MARKER = "mc-a11y-seo-bundle"

FONT_PRELOAD = (
    '<link rel="preload" href="/assets/fonts/worksans/worksans-latin.woff2" '
    'as="font" type="font/woff2" crossorigin>'
)
FONTS_CSS = (
    '<link rel="stylesheet" id="mc-fonts-css" '
    'href="/assets/css/mc-fonts.css?ver=1" media="all">'
)
A11Y_CSS = (
    '<link rel="stylesheet" id="mc-a11y-seo-css" '
    'href="/assets/css/mc-a11y-seo.css?ver=1" media="all">'
)
RUNTIME_JS = (
    '<script id="mc-runtime-fixes-js" '
    'src="/assets/js/mc-runtime-fixes.js?ver=1"></script>'
)
A11Y_JS = (
    '<script id="mc-a11y-fixes-js" '
    'src="/assets/js/mc-a11y-fixes.js?ver=1"></script>'
)
TOGGLE_JS = (
    '<script id="mc-toggle-fallback-js" '
    'src="/assets/js/mc-toggle-fallback.js?ver=1"></script>'
)
TOGGLE_SCRIPT_RE = re.compile(
    r'(<script id="divi-script-library-toggle-js"[^>]*></script>)',
    re.I,
)

GOOGLE_FONTS_RE = re.compile(
    r'<link[^>]+id="et-builder-googlefonts-cached-css"[^>]*>\s*',
    re.I,
)
FONT_DNS_RE = re.compile(
    r'<link rel="dns-prefetch" href="//fonts\.(?:googleapis|gstatic)\.com">\s*',
    re.I,
)
VIEWPORT_RE = re.compile(
    r'<meta name="viewport" content="[^"]*">',
    re.I,
)
CANONICAL_RE = re.compile(
    r'(<link rel="canonical" href=")([^"]*)(")',
    re.I,
)
TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.I)
META_DESC_RE = re.compile(
    r'<meta name="description" content="[^"]*">\s*',
    re.I,
)


def page_url(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{SITE}/"
    return f"{SITE}/{rel.replace('/index.html', '/')}"


def meta_description(title: str) -> str:
    text = title.strip()
    if " | Mentes Criativas" in text:
        text = text.split(" | Mentes Criativas", 1)[0].strip()
    if not text or text == "Mentes Criativas":
        return (
            "Projeto Mentes Criativas: aprendizagem ativa, cultura maker e "
            "pensamento computacional nas escolas de São João da Boa Vista/SP."
        )
    return f"{text}. Projeto educacional Mentes Criativas — UNIFEOB e DME."


def inject_head_bundle(text: str) -> str:
    bundle = f"<!-- {MARKER} -->\n{FONT_PRELOAD}\n{FONTS_CSS}\n{A11Y_CSS}\n"
    if MARKER in text:
        return text
    anchor = '<meta name="viewport"'
    if anchor in text:
        return text.replace(anchor, bundle + anchor, 1)
    return text.replace("</head>", bundle + "</head>", 1)


def inject_scripts(text: str) -> str:
    if 'id="mc-runtime-fixes-js"' in text:
        return text
    anchor = '<script data-wp-strategy="defer" defer id="wp-accessibility-js"'
    if anchor in text:
        return text.replace(anchor, RUNTIME_JS + A11Y_JS + anchor, 1)
    return text.replace("</body>", RUNTIME_JS + A11Y_JS + "</body>", 1)


def inject_toggle_fallback(text: str) -> str:
    if 'id="mc-toggle-fallback-js"' in text:
        return text
    return TOGGLE_SCRIPT_RE.sub(r"\1" + TOGGLE_JS, text, count=1)


def patch_html(text: str, html_path: Path) -> tuple[str, bool]:
    original = text
    url = page_url(html_path)

    text = GOOGLE_FONTS_RE.sub("", text)
    text = FONT_DNS_RE.sub("", text)
    text = VIEWPORT_RE.sub(
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        text,
        count=1,
    )
    text = CANONICAL_RE.sub(rf"\1{url}\3", text, count=1)

    title_match = TITLE_RE.search(text)
    if title_match:
        desc = meta_description(title_match.group(1))
        desc_tag = f'<meta name="description" content="{desc}">\n'
        if META_DESC_RE.search(text):
            text = META_DESC_RE.sub(desc_tag, text, count=1)
        elif title_match:
            text = text.replace(
                title_match.group(0),
                title_match.group(0) + "\n" + desc_tag.rstrip(),
                1,
            )

    text = inject_head_bundle(text)
    text = inject_scripts(text)
    text = inject_toggle_fallback(text)

    text = text.replace(
        "mc-responsive-fixes.css?ver=1",
        "mc-responsive-fixes.css?ver=2",
    )
    text = text.replace(
        "mc-section-monitores.css?ver=3",
        "mc-section-monitores.css?ver=4",
    )

    return text, text != original


def main() -> None:
    updated = 0
    for fp in sorted(ROOT.rglob("*.html")):
        if "node_modules" in fp.parts or "tools" in fp.parts:
            continue
        original = fp.read_text(encoding="utf-8", errors="surrogateescape")
        patched, changed = patch_html(original, fp)
        if changed:
            fp.write_text(patched, encoding="utf-8", errors="surrogateescape")
            print(f"updated {fp.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} files")


if __name__ == "__main__":
    main()
