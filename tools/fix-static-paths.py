#!/usr/bin/env python3
"""Fix absolute paths in Simply Static export for local serving."""
from __future__ import annotations

import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
TEXT_EXTENSIONS = {".html", ".css", ".js", ".json", ".svg", ".xml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}

OLD_URLS = (
    "https://diegoduenhas.com.br/mentescriativas",
    "http://diegoduenhas.com.br/mentescriativas",
)

# Matches root-absolute internal paths (not protocol-relative //)
ABS_PATH = re.compile(
    r"(?<![:/])/(?!/)"
    r"(?P<path>wp-content/[^\"'\s)>]+"
    r"|wp-includes/[^\"'\s)>]+"
    r"|projeto/?"
    r"|atividades/?"
    r"|biblioteca/?"
    r"|recomendacoes/?"
    r"|contato/?"
    r"|blog/?"
    r"|vibe-coding/?"
    r"|teste/?"
    r"|blockly[\w-]*/?"
    r"|microbit[\w-]*/?"
    r"|scratchjr[\w-]*/?"
    r"|project/[^\"'\s)>]+"
    r"|category/[^\"'\s)>]+"
    r"|author/[^\"'\s)>]+"
    r"|layout_tag/[^\"'\s)>]+"
    r"|layout_category/[^\"'\s)>]+"
    r"|2025/[^\"'\s)>]+"
    r"|wpa-stats-type/[^\"'\s)>]+"
    r"|\?p=\d+)"
    r"(?P<query>\?[^\"'\s)>]*)?"
    r"(?P<hash>#[^\"'\s)>]*)?"
)

MENTES_PREFIX = re.compile(r"/mentescriativas(?=/|$)")


def file_depth(path: Path) -> int:
    return len(path.relative_to(ROOT).parts) - 1


def rel_from_depth(depth: int, posix_path: str) -> str:
    prefix = "../" * depth if depth else "./"
    return f"{prefix}{posix_path.lstrip('/')}"


def absolutize_match(path: str, query: str = "", hash_: str = "") -> str:
    return f"/{path}{query}{hash_}"


def replace_abs_path(match: re.Match, depth: int) -> str:
    full = absolutize_match(match.group("path"), match.group("query") or "", match.group("hash") or "")
    return rel_from_depth(depth, full[1:])


def fix_root_only(content: str) -> str:
    for url in OLD_URLS:
        content = content.replace(url, "")
        content = content.replace(url + "/", "/")
    content = MENTES_PREFIX.sub("", content)
    return content


def fix_absolute_paths(content: str, depth: int) -> tuple[str, int]:
    changes = 0

    def sub_fn(m: re.Match) -> str:
        nonlocal changes
        changes += 1
        return replace_abs_path(m, depth)

    updated = ABS_PATH.sub(sub_fn, content)
    return updated, changes


def fix_home_links(content: str, depth: int) -> tuple[str, int]:
    """href="/" or action="/" -> relative home."""
    changes = 0
    home = rel_from_depth(depth, "").rstrip("/") + "/" if depth else "./"

    for attr in ("href", "action"):
        pattern = re.compile(rf'({attr}\s*=\s*["\'])/(["\'])', re.I)
        new_content, n = pattern.subn(rf"\1{home}\2", content)
        if n:
            changes += n
            content = new_content

    return content, changes


def fix_directory_links(content: str) -> tuple[str, int]:
    """Ensure trailing-slash links work when opened without a server."""
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        quote = m.group(1)
        path = m.group(2)
        if path.endswith("/") and not path.endswith("//"):
            changes += 1
            return f"{quote}{path}index.html{quote}"
        return m.group(0)

    # href="../projeto/" -> href="../projeto/index.html"
    pattern = re.compile(r'(?<=href=)(["\'])((?:\.\./|\./)[^"\']+/)(["\'])')
    content, n = pattern.subn(lambda m: f'{m.group(1)}{m.group(2)}index.html{m.group(3)}', content)
    changes += n

    # href="./blog/" at root
    pattern2 = re.compile(r'(?<=href=)(["\'])(\./[^"\']+/)(["\'])')
    content, n2 = pattern2.subn(lambda m: f'{m.group(1)}{m.group(2)}index.html{m.group(3)}', content)
    changes += n2

    return content, changes


def process_file(path: Path, dry_run: bool = False) -> int:
    depth = file_depth(path)
    try:
        original = path.read_text(encoding="utf-8", errors="surrogateescape")
    except OSError:
        return 0

    content = fix_root_only(original)
    content, c1 = fix_absolute_paths(content, depth)
    content, c2 = fix_home_links(content, depth)

    if path.suffix.lower() == ".html":
        content, c3 = fix_directory_links(content)
    else:
        c3 = 0

    total = c1 + c2 + c3
    if total and content != original and not dry_run:
        path.write_text(content, encoding="utf-8", errors="surrogateescape")
    return total


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    total_files = 0
    total_changes = 0

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.name in {"fix-static-paths.py", "serve-local.py"}:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        n = process_file(path, dry_run)
        if n:
            total_files += 1
            total_changes += n
            print(f"  {path.relative_to(ROOT)}: {n} fixes")

    mode = " (dry run)" if dry_run else ""
    print(f"\nDone{mode}: {total_files} files, {total_changes} replacements")


if __name__ == "__main__":
    main()
