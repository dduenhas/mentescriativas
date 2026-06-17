#!/usr/bin/env python3
"""Download missing wp-includes and plugin assets from the live WordPress site."""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://diegoduenhas.com.br/mentescriativas"

PATTERNS = [
    re.compile(r'["\'](?:\.\./|\./)*((?:wp-includes|wp-content/plugins/wp-accessibility)/[^"\'?#]+)', re.I),
]


def collect_paths() -> set[str]:
    paths: set[str] = set()
    for fp in ROOT.rglob("*.html"):
        text = fp.read_text(encoding="utf-8", errors="ignore")
        for pat in PATTERNS:
            for m in pat.finditer(text):
                paths.add(m.group(1))
    # mediaelement sprites often referenced from CSS
    paths.update(
        {
            "wp-includes/js/mediaelement/mejs-controls.svg",
        }
    )
    return paths


def download(path: str) -> bool:
    local = ROOT / path
    if local.exists():
        return True
    url = f"{BASE_URL}/{path}"
    local.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        local.write_bytes(data)
        print(f"  OK  {path}")
        return True
    except Exception as exc:
        print(f"  FAIL {path}: {exc}")
        return False


def main():
    paths = sorted(collect_paths())
    print(f"Downloading {len(paths)} assets from {BASE_URL}...\n")
    ok = fail = 0
    for path in paths:
        if download(path):
            ok += 1
        else:
            fail += 1
    print(f"\nDone: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
