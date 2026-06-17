---
name: deploy-mentescriativas
description: >-
  Faz commit no GitHub e deploy do site Mentes Criativas na Cloudflare Workers.
  Use quando o usuário pedir deploy, publicar, subir para produção, commit no
  GitHub, ou atualizar mentescriativas.educar.workers.dev.
disable-model-invocation: true
---

# Deploy Mentes Criativas

Workflow: **commit → push → Cloudflare deploy → validar**.

## Pré-requisitos

- Repositório: `c:\Users\diego\Projetos\mentescriativas`
- Branch padrão: **`master`** (não `main`)
- Remote: `origin` → `https://github.com/dduenhas/mentescriativas.git`
- Autor do commit (não alterar `git config`): `Diego Duenhas <dduenhas@gmail.com>`
- URL produção: `https://mentescriativas.educar.workers.dev`

## Passo 1 — Corrigir bloqueios comuns de commit

Antes de commitar, resolver:

1. **`scripts/sync-r2.mjs` conflito staged/deleted** — arquivo removido; não commitar:
   ```bash
   git add scripts/sync-r2.mjs
   ```
   (com o arquivo ausente, isso registra a remoção no índice)

2. **Não commitar** arquivos de debug de agente:
   - `tools/test-*.mjs`
   - `tools/check-jquery-corruption.py`
   - `tools/inspect-corruption.py`
   - `*.original.pdf`

3. Se `tools/test-*.mjs` estiver staged:
   ```bash
   git restore --staged tools/test-*.mjs tools/check-jquery-corruption.py tools/inspect-corruption.py
   ```

## Passo 2 — Analisar mudanças

Em paralelo:

```bash
git status
git diff
git diff --cached
git log -5 --oneline
```

## Passo 3 — Stage e commit

Incluir apenas mudanças do site, Worker, scripts de deploy e ferramentas de manutenção.

```bash
git add -A
git restore --staged tools/test-*.mjs tools/check-jquery-corruption.py tools/inspect-corruption.py 2>/dev/null || true
git restore --staged "**/*.original.pdf" 2>/dev/null || true
```

Commit (PowerShell — usar `--author` sem mudar git config):

```powershell
git commit --author="Diego Duenhas <dduenhas@gmail.com>" -m "Mensagem concisa em 1-2 frases focada no porquê."
```

Se não houver mudanças para commitar, pular para o deploy.

## Passo 4 — Push

```bash
git push -u origin master
```

Só fazer push quando o usuário pedir deploy/commit para GitHub (este skill sempre inclui push).

## Passo 5 — Deploy Cloudflare

```bash
npm run deploy
```

Isso executa `scripts/upload-large-r2.mjs` (só arquivos em `r2-large-files.txt`) e `wrangler deploy`.

Credenciais: Wrangler já autenticado na máquina do usuário (`wrangler login`).

## Passo 6 — Validar

```bash
curl -sI https://mentescriativas.educar.workers.dev/
curl -sI https://mentescriativas.educar.workers.dev/biblioteca/
```

Confirmar HTTP 200. Informar URL ao usuário.

## O que não fazer

- Nunca `git config` (global ou local)
- Nunca `git push --force` em `master`
- Nunca commitar `.env`, `.dev.vars`, secrets
- Nunca commitar `node_modules/` ou `.wrangler/`

## Estrutura do deploy

| Item | Caminho |
|------|---------|
| Worker | `src/index.ts` |
| Config | `wrangler.jsonc` |
| Assets estáticos | raiz do repo (excluídos via `.assetsignore`) |
| R2 (opcional) | bucket `mentescriativas`, lista `r2-large-files.txt` |
