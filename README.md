# Mentes Criativas

Site estático do projeto educacional **Mentes Criativas** — repositório de informações sobre cultura maker, pensamento computacional, STEM/STEAM e atividades práticas para sala de aula.

Origem: exportação estática do WordPress (tema Divi) via plugin Simply Static, reorganizada para deploy em servidor web com estrutura de pastas limpa e caminhos absolutos (`/assets/...`).

**Site original (WordPress):** [diegoduenhas.com.br/mentescriativas](https://diegoduenhas.com.br/mentescriativas)

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Mapa de páginas](#mapa-de-páginas)
- [Requisitos](#requisitos)
- [Como rodar localmente](#como-rodar-localmente)
- [Deploy em servidor](#deploy-em-servidor)
- [Redirects de URLs antigas](#redirects-de-urls-antigas)
- [Ferramentas de manutenção](#ferramentas-de-manutenção)
- [Limitações conhecidas](#limitações-conhecidas)
- [Licença e créditos](#licença-e-créditos)

---

## Sobre o projeto

O **Mentes Criativas** é um projeto educacional focado em:

- Introdução à **cultura maker** e educação criativa
- **Pensamento computacional** além da programação
- Atividades com **Blockly.Games**, **Micro:bit** e **ScratchJr**
- Conteúdos sobre **STEM/STEAM**, BNCC e interdisciplinaridade
- **Biblioteca** de recursos e **recomendações** pedagógicas

Este repositório contém a versão **100% estática** do site (~177 MB, 23 páginas HTML, 1.100+ arquivos), pronta para hospedagem em Apache, Nginx, GitHub Pages (com adaptações) ou qualquer servidor de arquivos estáticos.

### Stack técnica

| Componente | Detalhe |
|------------|---------|
| HTML | Páginas exportadas do WordPress + Divi 5.7.4 |
| CSS | Estilos inline + cache Divi em `assets/css/` |
| JavaScript | jQuery 3.7.1, scripts Divi, WP Accessibility |
| Fontes | Work Sans (Google Fonts), ETmodules, Font Awesome |
| Imagens | WebP, AVIF, PNG, PDFs em `assets/img/` |

---

## Estrutura de pastas

```
mentescriativas/
├── index.html                 # Página inicial
├── projeto/                   # Apresentação do projeto
├── atividades/                # Hub + aulas práticas
│   ├── index.html
│   ├── blockly-aula-1/ … blockly-aula-4/
│   ├── blockly-games-aula-3/
│   ├── blockly-games-sugestao-de-aulas/
│   ├── microbit-aula-01/ … microbit-aula-04/
│   └── scratchjr-aula-1/
├── biblioteca/
├── recomendacoes/
├── vibe-coding/
├── contato/
├── blog/
│   ├── index.html             # Listagem de artigos
│   └── [slug-do-artigo]/      # Posts individuais
├── assets/                    # Recursos estáticos (não versionar separadamente)
│   ├── css/                   # Folhas Divi (et-cache)
│   ├── img/                   # Uploads (imagens, PDFs, Lottie JSON)
│   └── js/
│       ├── vendor/            # jQuery, MediaElement
│       ├── divi/              # Scripts e fontes do tema
│       └── a11y/              # WP Accessibility
├── tools/                     # Scripts Python (desenvolvimento local)
├── .htaccess                  # Apache: cache + redirects
├── nginx.conf.example         # Snippet Nginx
├── iniciar-site-local.bat     # Atalho Windows
└── README.md
```

### O que **não** enviar ao servidor de produção

A pasta `tools/` é apenas para desenvolvimento e manutenção local. No deploy, envie todo o restante **exceto** `tools/`, `.git/` e este README (opcional).

---

## Mapa de páginas

### Seções principais

| URL | Conteúdo |
|-----|----------|
| `/` | Home — visão geral, slider de artigos, proposta do projeto |
| `/projeto/` | O Projeto Mentes Criativas |
| `/atividades/` | Hub de atividades educacionais |
| `/biblioteca/` | Biblioteca de recursos |
| `/recomendacoes/` | Recomendações pedagógicas |
| `/vibe-coding/` | Vibe Coding |
| `/blog/` | Blog |
| `/contato/` | Contato |

### Atividades (`/atividades/`)

| URL | Título |
|-----|--------|
| `/atividades/blockly-aula-1/` | Blockly – aula 1 |
| `/atividades/blockly-aula-2/` | Blockly – aula 2 |
| `/atividades/blockly-games-aula-3/` | Blockly – aula 3 |
| `/atividades/blockly-aula-4/` | Blockly – aula 4 |
| `/atividades/blockly-games-sugestao-de-aulas/` | Blockly.Games – Sugestão de aulas |
| `/atividades/microbit-aula-01/` … `04/` | Micro:bit – aulas 01 a 04 |
| `/atividades/scratchjr-aula-1/` | ScratchJr – aula 1 |

### Artigos do blog (`/blog/`)

| URL | Título |
|-----|--------|
| `/blog/a-importancia-do-pensamento-computacional-pc-na-educacao-brasileira/` | A importância do Pensamento Computacional na educação brasileira |
| `/blog/pensamento-computacional-em-sala-de-aula-muito-alem-da-programacao/` | Pensamento computacional em sala de aula |
| `/blog/bncc-competencias-e-habilidades/` | BNCC: competências vs habilidades |
| `/blog/entre-fronteiras-o-dialogo-e-o-deslimite-entre-o-interdisciplinar-e-o-transdisciplinar/` | Interdisciplinar vs transdisciplinar |
| `/blog/stem-e-steam-qual-e-a-diferenca-entre-esses-dois-movimentos-educacionais/` | STEM e STEAM |

---

## Requisitos

### Para visualizar localmente

- **Python 3.8+** (para o servidor local incluído), **ou**
- Qualquer servidor HTTP estático (Apache, Nginx, `npx serve`, etc.)

### Para deploy

- Servidor web com suporte a arquivos estáticos
- **Apache:** `mod_rewrite` e `mod_expires` (recomendado — `.htaccess` incluído)
- **Nginx:** usar `nginx.conf.example` como base
- Conexão com internet (fontes Google Fonts carregadas via CDN)

---

## Como rodar localmente

### Opção 1 — Servidor Python (recomendado)

**Windows:** dê duplo clique em `iniciar-site-local.bat` ou execute:

```bash
python tools/serve-local.py
```

O script abre o navegador em `http://localhost:8080/`. Se a porta 8080 estiver ocupada, tenta automaticamente 8081, 8082, etc.

### Opção 2 — Outros servidores

```bash
# Node.js
npx serve .

# PHP
php -S localhost:8080
```

Aponte a raiz do servidor para a pasta do projeto (onde está o `index.html`).

### Opção 3 — Abrir HTML direto (limitado)

É possível abrir `index.html` no navegador, mas **animações Lottie** e alguns scripts podem falhar por restrições `file://` do navegador. Use o servidor local para experiência completa.

---

## Deploy em servidor

### 1. Upload dos arquivos

Envie via FTP/SFTP ou Git deploy todo o conteúdo da raiz do projeto para o **document root** do domínio, **exceto** a pasta `tools/`.

Exemplo de destino:

```
/public_html/          ← Apache/cPanel
/var/www/mentescriativas/   ← VPS Nginx
```

### 2. Apache (cPanel, hospedagem compartilhada)

O arquivo `.htaccess` na raiz já configura:

- `DirectoryIndex index.html`
- Cache de 1 ano para CSS, JS, imagens e fontes
- Redirects 301 das URLs antigas do WordPress

Certifique-se de que `AllowOverride All` está habilitado para o diretório.

### 3. Nginx

Inclua o conteúdo de `nginx.conf.example` no bloco `server` do seu site:

```nginx
server {
    listen 80;
    server_name seudominio.com.br;
    root /var/www/mentescriativas;

    include /caminho/para/nginx.conf.example;
}
```

### 4. GitHub Pages (opcional)

GitHub Pages serve sites estáticos, mas **não processa `.htaccess`**. Para subpath (`usuario.github.io/mentescriativas/`), seria necessário ajustar caminhos absolutos `/assets/` — recomendado usar domínio próprio na raiz ou serviços como Netlify/Cloudflare Pages.

---

## Redirects de URLs antigas

Após a reorganização, URLs do WordPress original redirecionam automaticamente (301):

| URL antiga | URL nova |
|------------|----------|
| `/blockly-aula-1/` | `/atividades/blockly-aula-1/` |
| `/microbit-aula-01/` | `/atividades/microbit-aula-01/` |
| `/2025/10/222670-2/` | `/blog/bncc-competencias-e-habilidades/` |
| `/2025/11/a-importancia-do-pensamento-.../` | `/blog/a-importancia-do-pensamento-.../` |
| `/project/blockly-games-sugestao-de-aulas/` | `/atividades/blockly-games-sugestao-de-aulas/` |

---

## Ferramentas de manutenção

Scripts em `tools/` para reexportação ou correções futuras:

| Script | Função |
|--------|--------|
| `serve-local.py` | Servidor HTTP local |
| `fix-static-paths.py` | Corrige caminhos após novo export Simply Static |
| `fix-urls.py` | Limpa URLs quebradas pós-reorganização |
| `reorganize-site.py` | Reaplica estrutura `assets/` + movimentação de páginas |
| `download-missing-assets.py` | Baixa `wp-includes` e plugins ausentes do site original |

### Fluxo após reexportar do WordPress

```bash
python tools/fix-static-paths.py
python tools/download-missing-assets.py
python tools/reorganize-site.py
python tools/fix-urls.py
python tools/serve-local.py
```

---

## Limitações conhecidas

Funcionalidades que **não funcionam** na versão estática (comportamento esperado):

| Recurso | Motivo |
|---------|--------|
| Busca do menu | Dependia de PHP/WordPress (`?s=`) |
| Formulário de contato | Requer backend para envio de e-mail |
| Feeds RSS (`/feed/`) | Endpoints WordPress não exportados |
| API REST (`/wp-json/`) | Backend WordPress ausente |
| Comentários | Sistema dinâmico do WordPress |

Links residuais para `/feed/`, `/wp-json/` e `/xmlrpc.php` no `<head>` são metadados do export e **não afetam** a aparência do site.

---

## Licença e créditos

- **Conteúdo pedagógico:** Projeto Mentes Criativas
- **Tema visual:** [Divi](https://www.elegantthemes.com/gallery/divi/) (Elegant Themes) — uso sujeito à licença do tema
- **Exportação estática:** [Simply Static](https://wordpress.org/plugins/simply-static/) (WordPress)
- **Acessibilidade:** [WP Accessibility](https://wordpress.org/plugins/wp-accessibility/)
- **Manutenção e reorganização deste repositório:** Diego Duenhas — [dduenhas@gmail.com](mailto:dduenhas@gmail.com)

---

## Contato

- **E-mail:** dduenhas@gmail.com
- **Site WordPress (origem):** https://diegoduenhas.com.br/mentescriativas
