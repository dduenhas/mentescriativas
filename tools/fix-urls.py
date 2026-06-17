#!/usr/bin/env python3
"""Post-reorganization cleanup: fix broken URLs and paths."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = {".html", ".css", ".js", ".json", ".svg"}


def clean_text(text: str) -> str:
    # Fix mangled asset paths
    text = re.sub(r"(?:\.\./)+/assets/", "/assets/", text)
    text = re.sub(r"\.\./assets/", "/assets/", text)
    text = re.sub(r"(?<![:/])/assets/", "/assets/", text)  # ..//assets -> /assets
    text = text.replace("..//assets/", "/assets/")
    text = text.replace(".//assets/", "/assets/")
    text = text.replace("../assets/", "/assets/")
    text = text.replace("./assets/", "/assets/")

    # Fix triple/double atividades prefix
    while "/atividades/atividades/" in text:
        text = text.replace("/atividades/atividades/", "/atividades/")

    # Fix double trailing slashes in URLs
    text = re.sub(r"(/[^\"'\s)#?]+)//+", r"\1/", text)
    text = re.sub(r"(href=\"/[^\"]+?)//\"", r'\1/"', text)

    # Relative page links -> absolute
    pages = [
        "projeto", "atividades", "biblioteca", "recomendacoes",
        "vibe-coding", "blog", "contato",
    ]
    lessons = [
        "blockly-aula-1", "blockly-aula-2", "blockly-games-aula-3", "blockly-aula-4",
        "microbit-aula-01", "microbit-aula-02", "microbit-aula-03", "microbit-aula-04",
        "scratchjr-aula-1", "blockly-games-sugestao-de-aulas",
    ]
    blog_posts = [
        "a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira",
        "pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao",
        "bncc-competencias-e-habilidades",
        "entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar",
        "stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais",
    ]

    for p in pages:
        for prefix in ["../", "../../", "../../../", "./"]:
            text = text.replace(f'"{prefix}{p}/"', f'"/{p}/"')
            text = text.replace(f"'{prefix}{p}/'", f"'/{p}/'")
            text = text.replace(f'"{prefix}{p}"', f'"/{p}/"')

    for lesson in lessons:
        for prefix in ["../", "../../", "../../../", "./", "/"]:
            old = f'{prefix}atividades/{lesson}/' if prefix != "/" else f"/{lesson}/"
            new = f"/atividades/{lesson}/"
            text = text.replace(f'"{old}"', f'"{new}"')
            text = text.replace(f"'{old}'", f"'{new}'")
        # old root-level lesson URLs
        text = text.replace(f'"/{lesson}/"', f'"/atividades/{lesson}/"')
        text = text.replace(f"'/{lesson}/'", f"'/atividades/{lesson}/'")

    # Old blog date URLs -> new blog slugs
    old_blog_map = {
        "2025/11/a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira": "blog/a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira",
        "2025/10/pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao": "blog/pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao",
        "2025/10/222670-2": "blog/bncc-competencias-e-habilidades",
        "2025/10/entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar": "blog/entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar",
        "2025/10/stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais": "blog/stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais",
    }
    for old, new in old_blog_map.items():
        for prefix in ["../", "../../", "../../../", "./", "/"]:
            text = text.replace(f"{prefix}{old}/", f"/{new}/")
            text = text.replace(f"{prefix}{old}/index.html", f"/{new}/")
        text = text.replace(f"/{old}/", f"/{new}/")

    for post in blog_posts:
        text = text.replace(f'"/blog/{post}/index.html"', f'"/blog/{post}/"')
        text = text.replace(f'"/blog/{post}//"', f'"/blog/{post}/"')

    # Remove broken optimization-detective loader blocks
    text = re.sub(
        r'<script[^>]*src="[^"]*optimization-detective[^"]*"[^>]*></script>',
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'<script type="module"[^>]*>[\s\S]*?optimization-detective[\s\S]*?</script>',
        "",
        text,
        flags=re.I,
    )
    text = text.replace("../wp-content/plugins/optimization-detective/", "")
    text = text.replace("../wp-content/plugins/image-prioritizer/", "")
    text = text.replace("wp-content/plugins/optimization-detective/", "")
    text = text.replace("../wp-content/", "")
    text = text.replace("..//assets/js/divi/", "/assets/js/divi/")

    # Old project path
    text = text.replace(
        "/project/blockly-games-sugestao-de-aulas/",
        "/atividades/blockly-games-sugestao-de-aulas/",
    )

    return text


def main():
    updated = 0
    for fp in ROOT.rglob("*"):
        if not fp.is_file() or fp.suffix.lower() not in EXT:
            continue
        if fp.name.endswith(".min.js"):
            continue
        if "tools" in fp.parts:
            continue
        original = fp.read_text(encoding="utf-8", errors="surrogateescape")
        fixed = clean_text(original)
        if fixed != original:
            fp.write_text(fixed, encoding="utf-8", errors="surrogateescape")
            updated += 1
    print(f"Fixed {updated} files")


if __name__ == "__main__":
    main()
