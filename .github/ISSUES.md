# Issues Planejadas

## Como Criar as Issues no GitHub

1. Acesse: https://github.com/sthevan027/Converso/issues/new
2. Copie o conteúdo dos arquivos abaixo
3. Cole no campo de descrição da issue

---

## Issue 1: Interface Gráfica (GUI)

**Título:** Interface Gráfica (GUI) para o Conversor

**Labels:** `enhancement`, `gui`, `feature`

**Conteúdo:** Copiar de `.github/ISSUE_TEMPLATE/feature_gui.md`

### Resumo das Fases:
1. **Estrutura Base** - Framework e pastas
2. **Tela Principal** - Drag & drop, seleção de arquivo
3. **Opções de Configuração** - Configurações avançadas
4. **Conversão e Feedback** - Progresso e notificações
5. **Melhorias de UX** - Tema, histórico, lote

---

## Issue 2: Melhoria na Lógica

**Título:** Melhoria na Lógica de Conversão

**Labels:** `enhancement`, `optimization`

**Conteúdo:** Copiar de `.github/ISSUE_TEMPLATE/feature_melhorias.md`

### Resumo das Fases:
1. **Detecção de Estrutura** - Cabeçalhos, rodapés, títulos
2. **Extração de Texto** - OCR, colunas, listas
3. **Tabelas** - Detecção avançada, células mescladas
4. **Imagens** - Posição, SVG, otimização
5. **DOCX para PDF** - Links, imagens, estilos
6. **Performance** - Paralelo, cache, memória
7. **Qualidade** - Testes, métricas, validação

---

## Instalação do GitHub CLI (Opcional)

Para criar issues via terminal, instale o GitHub CLI:

```powershell
# Via winget
winget install GitHub.cli

# Ou via Chocolatey
choco install gh

# Depois autentique
gh auth login
```

Após instalar, execute:
```powershell
gh issue create --title "Interface Grafica (GUI)" --body-file .github/ISSUE_TEMPLATE/feature_gui.md
gh issue create --title "Melhoria na Logica" --body-file .github/ISSUE_TEMPLATE/feature_melhorias.md
```
