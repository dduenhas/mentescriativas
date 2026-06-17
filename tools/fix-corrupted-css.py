#!/usr/bin/env python3
"""Repair CSS gradients broken by overly broad URL cleanup."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    (
        ".et_pb_section_10{background-image:linear-gradient(180deg,100%)!important;background-repeat:no-repeat!important}",
        "",
    ),
    (
        ".preset--module--divi-section--c35cf80c-97b8-4940-a56e-23517027c17a{background-image:linear-gradient(180deg,rgba(255,255,255,0) 80%,#000000 80% 100%)!important;background-repeat:no-repeat!important}",
        ".preset--module--divi-section--c35cf80c-97b8-4940-a56e-23517027c17a{background-image:none!important}",
    ),
]


def main() -> None:
    updated = 0
    for fp in ROOT.rglob("*.css"):
        if "node_modules" in fp.parts:
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
