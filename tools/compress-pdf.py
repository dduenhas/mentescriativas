#!/usr/bin/env python3
"""Compress large PDF for web (PyMuPDF)."""
import sys
from pathlib import Path

import fitz

INPUT = Path(__file__).resolve().parent.parent / "assets/img/2025/10/04_Eu-robo.pdf"
OUTPUT = INPUT.with_name("04_Eu-robo-compressed.pdf")
BACKUP = INPUT.with_name("04_Eu-robo.original.pdf")


def compress(input_path: Path, output_path: Path, dpi: int, quality: int) -> float:
    src = fitz.open(input_path)
    dst = fitz.open()
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    total = src.page_count

    for i, page in enumerate(src):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = pix.tobytes("jpeg", jpg_quality=quality)
        page_rect = fitz.Rect(0, 0, pix.width, pix.height)
        new_page = dst.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(page_rect, stream=img)
        if (i + 1) % 30 == 0 or i + 1 == total:
            print(f"  {i + 1}/{total} pages...")

    dst.save(output_path, garbage=4, deflate=True, clean=True, pretty=False)
    src.close()
    dst.close()
    return output_path.stat().st_size / (1024 * 1024)


def main() -> None:
    if not INPUT.exists():
        print(f"Missing: {INPUT}")
        sys.exit(1)

    orig_mb = INPUT.stat().st_size / (1024 * 1024)
    print(f"Original: {orig_mb:.1f} MB ({fitz.open(INPUT).page_count} pages)\n")

    attempts = [
        (150, 80),
        (120, 75),
        (100, 70),
        (96, 65),
    ]

    best_path = None
    best_mb = orig_mb
    best_cfg = None

    for dpi, quality in attempts:
        print(f"Trying {dpi} dpi, JPEG quality {quality}...")
        mb = compress(INPUT, OUTPUT, dpi, quality)
        print(f"  -> {mb:.1f} MB\n")
        if mb < best_mb:
            best_mb = mb
            best_cfg = (dpi, quality)
        if mb <= 20:
            break

    if best_cfg is None:
        print("Compression failed.")
        sys.exit(1)

    if not BACKUP.exists():
        INPUT.rename(BACKUP)
        print(f"Backup: {BACKUP.name}")

    OUTPUT.rename(INPUT)
    print(f"Replaced with {best_mb:.1f} MB ({best_cfg[0]} dpi, q={best_cfg[1]})")
    if best_mb <= 25:
        print("Under 25 MB — can use Workers Static Assets (no R2 needed).")
    else:
        print("Still over 25 MB — keep R2 fallback for this file.")


if __name__ == "__main__":
    main()
