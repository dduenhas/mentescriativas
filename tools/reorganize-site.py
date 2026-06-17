#!/usr/bin/env python3
"""
Reorganize Mentes Criativas static export into a clean web-server structure.

Target layout:
  /
  ├── index.html
  ├── projeto/  biblioteca/  recomendacoes/  vibe-coding/  contato/
  ├── atividades/          (hub + lessons)
  ├── blog/                (listing + posts)
  └── assets/
      ├── css/             (Divi et-cache)
      ├── img/             (uploads)
      ├── js/vendor/       (jquery, mediaelement)
      ├── js/divi/         (theme scripts)
      ├── js/a11y/         (wp-accessibility)
      └── fonts/           (Divi icon fonts)
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Pages to move: source dir (relative to ROOT) -> destination dir
PAGE_MOVES: dict[str, str] = {
    "blockly-aula-1": "atividades/blockly-aula-1",
    "blockly-aula-2": "atividades/blockly-aula-2",
    "blockly-games-aula-3": "atividades/blockly-games-aula-3",
    "blockly-aula-4": "atividades/blockly-aula-4",
    "microbit-aula-01": "atividades/microbit-aula-01",
    "microbit-aula-02": "atividades/microbit-aula-02",
    "microbit-aula-03": "atividades/microbit-aula-03",
    "microbit-aula-04": "atividades/microbit-aula-04",
    "scratchjr-aula-1": "atividades/scratchjr-aula-1",
    "project/blockly-games-sugestao-de-aulas": "atividades/blockly-games-sugestao-de-aulas",
    "2025/11/a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira": "blog/a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira",
    "2025/10/pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao": "blog/pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao",
    "2025/10/222670-2": "blog/bncc-competencias-e-habilidades",
    "2025/10/entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar": "blog/entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar",
    "2025/10/stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais": "blog/stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais",
}

# Folders to delete (WordPress cruft / unused)
DELETE_DIRS = [
    "wpa-stats-type",
    "author",
    "category",
    "layout_tag",
    "layout_category",
    "teste",
    "2025",
    "project",
]

DELETE_UNDER_WP_CONTENT = [
    "plugins/wp-file-manager",
    "plugins/speedycache",
    "plugins/wpvivid-backuprestore",
    "plugins/filebird",
    "plugins/web-worker-offloading",
    "plugins/performance-lab",
    "plugins/nocache-bfcache",
    "plugins/embed-optimizer",
    "plugins/image-prioritizer",
    "plugins/optimization-detective",
    "plugins/speculation-rules",
    "plugins/view-transitions",
    "plugins/auto-sizes",
    "plugins/webp-uploads",
    "cache",
]

TEXT_EXTENSIONS = {".html", ".css", ".js", ".json", ".svg", ".xml"}
SKIP_DIRS = {"tools", ".git", "__pycache__", "node_modules"}


def move_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.move(str(src), str(dst))
    print(f"  moved {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        print(f"  SKIP missing {src.relative_to(ROOT)}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"  copied {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def move_assets() -> None:
    print("\n=== Moving assets ===")
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)

    copy_tree(ROOT / "wp-content" / "uploads", assets / "img")
    copy_tree(ROOT / "wp-content" / "et-cache", assets / "css")

    wp_includes = ROOT / "wp-includes"
    if wp_includes.exists():
        copy_tree(wp_includes / "js", assets / "js" / "vendor")

    a11y = ROOT / "wp-content" / "plugins" / "wp-accessibility"
    if a11y.exists():
        if (a11y / "css").exists():
            copy_tree(a11y / "css", assets / "js" / "a11y-css-tmp")
        if (a11y / "js").exists():
            copy_tree(a11y / "js", assets / "js" / "a11y")

    divi = ROOT / "wp-content" / "themes" / "Divi"
    if divi.exists():
        # Keep only runtime paths referenced by HTML
        for sub in [
            "js",
            "core/admin/fonts",
            "core/admin/js",
            "includes/builder-5/visual-builder/build",
        ]:
            src = divi / sub
            dst = assets / "js" / "divi" / sub
            if src.exists():
                copy_tree(src, dst)

        parallax_css = divi / "includes/builder-5/visual-builder/build/module-style-static-background-parallax.css"
        if parallax_css.exists():
            dst = assets / "css" / "module-style-static-background-parallax.css"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(parallax_css, dst)

    # wp-accessibility css -> assets/css
    a11y_css = assets / "js" / "a11y-css-tmp"
    if a11y_css.exists():
        copy_tree(a11y_css, assets / "css" / "a11y")
        shutil.rmtree(a11y_css)


def move_pages() -> None:
    print("\n=== Moving pages ===")
    for src_rel, dst_rel in PAGE_MOVES.items():
        move_dir(ROOT / src_rel, ROOT / dst_rel)


def cleanup() -> None:
    print("\n=== Cleanup ===")
    for rel in DELETE_DIRS:
        path = ROOT / rel
        if path.exists():
            shutil.rmtree(path)
            print(f"  deleted {rel}/")

    for rel in DELETE_UNDER_WP_CONTENT:
        path = ROOT / "wp-content" / rel
        if path.exists():
            shutil.rmtree(path)
            print(f"  deleted wp-content/{rel}")

    wp_content = ROOT / "wp-content"
    if wp_content.exists():
        shutil.rmtree(wp_content)
        print("  deleted wp-content/")

    wp_includes = ROOT / "wp-includes"
    if wp_includes.exists():
        shutil.rmtree(wp_includes)
        print("  deleted wp-includes/")

    spooky = ROOT / "spooky"
    if spooky.exists():
        if spooky.is_dir():
            shutil.rmtree(spooky)
        else:
            spooky.unlink()
        print("  deleted spooky")


def build_url_replacements() -> list[tuple[str, str]]:
    reps: list[tuple[str, str]] = []

    # Old WordPress asset paths (many relative variants -> absolute /assets/)
    asset_patterns = [
        (r"(?:\.\./)+wp-content/uploads/", "/assets/img/"),
        (r"\./wp-content/uploads/", "/assets/img/"),
        (r"wp-content/uploads/", "/assets/img/"),
        (r"(?:\.\./)+wp-content/et-cache/", "/assets/css/"),
        (r"\./wp-content/et-cache/", "/assets/css/"),
        (r"wp-content/et-cache/", "/assets/css/"),
        (r"(?:\.\./)+wp-includes/js/", "/assets/js/vendor/"),
        (r"\./wp-includes/js/", "/assets/js/vendor/"),
        (r"wp-includes/js/", "/assets/js/vendor/"),
        (r"(?:\.\./)+wp-content/plugins/wp-accessibility/css/", "/assets/css/a11y/"),
        (r"\./wp-content/plugins/wp-accessibility/css/", "/assets/css/a11y/"),
        (r"wp-content/plugins/wp-accessibility/css/", "/assets/css/a11y/"),
        (r"(?:\.\./)+wp-content/plugins/wp-accessibility/js/", "/assets/js/a11y/"),
        (r"\./wp-content/plugins/wp-accessibility/js/", "/assets/js/a11y/"),
        (r"wp-content/plugins/wp-accessibility/js/", "/assets/js/a11y/"),
        (r"(?:\.\./)+wp-content/themes/Divi/", "/assets/js/divi/"),
        (r"\./wp-content/themes/Divi/", "/assets/js/divi/"),
        (r"wp-content/themes/Divi/", "/assets/js/divi/"),
        (r"/assets/js/divi/core/admin/fonts/", "/assets/js/divi/core/admin/fonts/"),
        (r"/assets/js/divi/includes/builder-5/visual-builder/build/module-style-static-background-parallax.css", "/assets/css/module-style-static-background-parallax.css"),
    ]
    reps.extend(asset_patterns)

    # Page URL migrations (old -> new), longest first
    page_urls: list[tuple[str, str]] = []
    for src, dst in PAGE_MOVES.items():
        old_url = f"/{src}/"
        new_url = f"/{dst}/"
        page_urls.append((old_url, new_url))
        page_urls.append((f"/{src}/index.html", f"/{dst}/"))
        page_urls.append((f"/{src}", f"/{dst}/"))
        # relative variants
        for prefix in ["./", "../", "../../", "../../../"]:
            depth = prefix.count("../") + (1 if prefix == "./" else 0)
            page_urls.append((f"{prefix}{src}/index.html", f"/{dst}/"))
            page_urls.append((f"{prefix}{src}/", f"/{dst}/"))

    page_urls.sort(key=lambda x: len(x[0]), reverse=True)
    reps.extend(page_urls)

    # Normalize internal page links to root-absolute
    site_pages = [
        "", "projeto", "atividades", "biblioteca", "recomendacoes",
        "vibe-coding", "blog", "contato",
    ]
    site_pages.extend(PAGE_MOVES.values())

    for page in site_pages:
        if page:
            for prefix in ["./", "../", "../../", "../../../"]:
                reps.append((f'{prefix}{page}/index.html', f"/{page}/"))
                reps.append((f'href="{prefix}{page}/"', f'href="/{page}/"'))
                reps.append((f"href='{prefix}{page}/'", f"href='/{page}/'"))
        reps.append(('href="./"', 'href="/"'))
        reps.append(("href='./'", "href='/'"))
        reps.append(('action="./"', 'action="/"'))
        reps.append(("action='./'", "action='/'"))
        for prefix in ["../", "../../", "../../../"]:
            reps.append((f'action="{prefix}"', 'action="/"'))
            reps.append((f"action='{prefix}'", "action='/'"))

    # Fix pluginPath in JS vars
    reps.append(('"pluginPath":"/assets/js/vendor/mediaelement/"', '"pluginPath":"/assets/js/vendor/mediaelement/"'))
    reps.append(('"pluginPath":"../../wp-includes/js/mediaelement/"', '"pluginPath":"/assets/js/vendor/mediaelement/"'))
    reps.append(('"pluginPath":"./wp-includes/js/mediaelement/"', '"pluginPath":"/assets/js/vendor/mediaelement/"'))

    return reps


def update_references() -> None:
    print("\n=== Updating references ===")
    replacements = build_url_replacements()
    count_files = 0

    for fp in ROOT.rglob("*"):
        if not fp.is_file():
            continue
        if any(p in SKIP_DIRS for p in fp.parts):
            continue
        if fp.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if fp.name in {"reorganize-site.py", "fix-static-paths.py", "download-missing-assets.py"}:
            continue

        text = fp.read_text(encoding="utf-8", errors="surrogateescape")
        original = text
        for old, new in replacements:
            text = text.replace(old, new)

        # url(/assets/...) already ok; fix url(/wp-content in CSS
        text = re.sub(
            r"url\((?:\.\./|\./)*wp-content/uploads/",
            "url(/assets/img/",
            text,
        )
        text = re.sub(
            r"url\((?:\.\./|\./)*wp-content/et-cache/",
            "url(/assets/css/",
            text,
        )
        text = re.sub(
            r"url\((?:\.\./|\./)*wp-content/themes/Divi/core/admin/fonts/",
            "url(/assets/js/divi/core/admin/fonts/",
            text,
        )
        text = re.sub(
            r"url\((?:\.\./|\./)*wp-includes/",
            "url(/assets/js/vendor/",
            text,
        )

        if text != original:
            fp.write_text(text, encoding="utf-8", errors="surrogateescape")
            count_files += 1

    print(f"  updated {count_files} files")


def move_dev_tools() -> None:
    print("\n=== Dev tools -> tools/ ===")
    tools = ROOT / "tools"
    tools.mkdir(exist_ok=True)
    for name in [
        "serve-local.py",
        "fix-static-paths.py",
        "download-missing-assets.py",
        "reorganize-site.py",
        "iniciar-site-local.bat",
    ]:
        src = ROOT / name
        if src.exists():
            dst = tools / name
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            print(f"  moved {name} -> tools/")


def write_htaccess() -> None:
    content = """# Mentes Criativas - Apache config
DirectoryIndex index.html

# Cache static assets
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType application/pdf "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

# Redirect old WordPress URLs to new structure
<IfModule mod_rewrite.c>
  RewriteEngine On

  # Activity pages moved under /atividades/
  RewriteRule ^blockly-aula-1/?$ /atividades/blockly-aula-1/ [R=301,L]
  RewriteRule ^blockly-aula-2/?$ /atividades/blockly-aula-2/ [R=301,L]
  RewriteRule ^blockly-games-aula-3/?$ /atividades/blockly-games-aula-3/ [R=301,L]
  RewriteRule ^blockly-aula-4/?$ /atividades/blockly-aula-4/ [R=301,L]
  RewriteRule ^microbit-aula-0([1-4])/?$ /atividades/microbit-aula-0$1/ [R=301,L]
  RewriteRule ^scratchjr-aula-1/?$ /atividades/scratchjr-aula-1/ [R=301,L]

  # Blog posts moved from /2025/ to /blog/
  RewriteRule ^2025/[0-9]+/(.+?)/?$ /blog/$1/ [R=301,L]
  RewriteRule ^2025/10/222670-2/?$ /blog/bncc-competencias-e-habilidades/ [R=301,L]

  # WordPress cruft -> home or blog
  RewriteRule ^(author|category|wpa-stats-type|layout_tag|layout_category)/ - [R=301,L,/]
  RewriteRule ^project/blockly-games-sugestao-de-aulas/?$ /atividades/blockly-games-sugestao-de-aulas/ [R=301,L]

  # Serve directories without trailing index.html in URL
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteCond %{REQUEST_FILENAME}/index.html -f
  RewriteRule ^(.+[^/])$ /$1/ [R=301,L]
</IfModule>
"""
    (ROOT / ".htaccess").write_text(content, encoding="utf-8")
    print("\n=== Wrote .htaccess ===")


def write_nginx_conf() -> None:
    content = """# Mentes Criativas - Nginx snippet (include in server block)
location /assets/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Redirects from old WordPress structure
location = /blockly-aula-1 { return 301 /atividades/blockly-aula-1/; }
location = /blockly-aula-2 { return 301 /atividades/blockly-aula-2/; }
location = /blockly-games-aula-3 { return 301 /atividades/blockly-games-aula-3/; }
location = /blockly-aula-4 { return 301 /atividades/blockly-aula-4/; }
location ~ ^/microbit-aula-0([1-4])/?$ { return 301 /atividades/microbit-aula-0$1/; }
location ~ ^/2025/[0-9]+/(.+)/?$ { return 301 /blog/$1/; }
location = /2025/10/222670-2 { return 301 /blog/bncc-competencias-e-habilidades/; }

location / {
    try_files $uri $uri/ $uri/index.html =404;
}
"""
    (ROOT / "nginx.conf.example").write_text(content, encoding="utf-8")
    print("  wrote nginx.conf.example")


def update_bat() -> None:
    bat = ROOT / "tools" / "iniciar-site-local.bat"
    if bat.exists():
        bat.write_text(
            "@echo off\r\n"
            "cd /d \"%~dp0..\"\r\n"
            "echo Iniciando servidor em http://localhost:8080/\r\n"
            "python tools/serve-local.py\r\n",
            encoding="utf-8",
        )

    serve = ROOT / "tools" / "serve-local.py"
    if serve.exists():
        text = serve.read_text(encoding="utf-8")
        text = text.replace(
            "ROOT = Path(__file__).resolve().parent",
            "ROOT = Path(__file__).resolve().parent.parent",
        )
        serve.write_text(text, encoding="utf-8")


def main() -> None:
    print("Reorganizing Mentes Criativas static site...")
    move_assets()
    move_pages()
    cleanup()
    update_references()
    move_dev_tools()
    write_htaccess()
    write_nginx_conf()
    update_bat()
    print("\nDone! New structure ready for web server deployment.")
    print("Run: python tools/serve-local.py")


if __name__ == "__main__":
    main()
