#!/usr/bin/env python3
"""Repair JS files broken by overly broad URL cleanup."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    (
        '.replace(/^\\/,"")^\\/,"")',
        '.replace(/^\\/,"")',
    ),
    (
        "pathname.replace(/^\\/,\"\")==this.pathname.replace(/",
        "pathname.replace(/^\\/,\"\")==this.pathname.replace(/^\\/,\"\")",
    ),
]


def main() -> None:
    updated = 0
    for fp in ROOT.rglob("*.js"):
        if "node_modules" in fp.parts or "tools" in fp.parts:
            continue
        text = fp.read_text(encoding="utf-8", errors="surrogateescape")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            fp.write_text(text, encoding="utf-8", errors="surrogateescape")
            print(f"fixed {fp.relative_to(ROOT)}")
            updated += 1
    print(f"Done: {updated} files")


if __name__ == "__main__":
    main()
