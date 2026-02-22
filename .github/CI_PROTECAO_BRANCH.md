## Objetivo

Garantir que nada entra em `main` sem **aprovação** e sem passar pelo **CI**.

## 1) Ativar proteção do branch `main`

No GitHub:

- Vá em `Settings` → `Branches` → `Branch protection rules`
- Clique em **Add rule**
- Em **Branch name pattern**, use: `main`

Marque (recomendado):

- **Require a pull request before merging**
  - **Require approvals**: 1 (ou mais, se o time crescer)
  - **Dismiss stale pull request approvals when new commits are pushed**
- **Require status checks to pass before merging**
  - Selecione o check: **CI / Checks (Python 3.12 • ubuntu-latest)** e **CI / Checks (Python 3.12 • windows-latest)**
  - **Require branches to be up to date before merging**
- **Do not allow bypassing the above settings** (se disponível no seu plano)

## 2) O que o CI valida

O workflow em `.github/workflows/ci.yml` roda em **Push/PR** e executa:

- Instala dependências (`pip install -r requirements.txt`)
- `ruff` (lint básico: `F,E9`)
- `mypy` (type-check com `--ignore-missing-imports`)
- `pytest` (se não houver testes, não falha)
- Smoke test: `python conversor.py --help`

## 3) Issue automática quando falhar no `main`

Quando um push em `main` falhar no CI, o workflow cria uma **Issue** com label `ci-failure` e link direto pro run.

