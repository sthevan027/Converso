# Converso – Conversor de Documentos

Conversor avançado em Python para transformar documentos entre diferentes formatos com alta fidelidade.

## Conversões Suportadas

| Entrada | Saída | Descrição |
| ------- | ----- | --------- |
| **PDF** | DOCX | Conversão completa com detecção de estrutura |
| **DOCX** | PDF | Preserva formatação e estilos |
| **TXT** | PDF | Texto simples para PDF formatado |
| **MD** | PDF | Markdown para PDF com títulos |

---

## Funcionalidades

### PDF → DOCX

- **Detecção automática de cabeçalhos e rodapés** - Identifica e converte para cabeçalho/rodapé nativo do Word
- **Preservação de formatação** - Mantém negrito, itálico e estilos de fonte
- **Mesclagem inteligente de parágrafos** - Une parágrafos fragmentados automaticamente
- **Remoção de hifenização** - Remove hífens de quebra de linha
- **Extração de imagens** - Extrai e incorpora imagens do PDF
- **Detecção de títulos** - Identifica e aplica estilos de Heading automaticamente

### DOCX/TXT/MD → PDF

- **Preservação de estilos** - Headings, negrito, itálico
- **Quebra de texto automática** - Ajusta ao tamanho A4
- **Suporte a Markdown** - Converte `#`, `##`, `###` para títulos
- **Paginação automática** - Cria novas páginas conforme necessário

---

## Pré‑requisitos

- Python 3.10 ou superior instalado
- Windows (testado no PowerShell)

---

## 1. Abrir o projeto

No PowerShell:

```powershell
cd "C:\Users\sthevan\OneDrive\Documentos\projeto\Converso"
```

---

## 2. Criar e ativar o ambiente virtual

Se ainda não existir o ambiente:

```powershell
python -m venv .venv
```

### Ativar no PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Se estiver usando **CMD**:

```cmd
.\.venv\Scripts\activate.bat
```

Se deu certo, o prompt deve ficar parecido com:

```text
(.venv) PS C:\Users\sthevan\OneDrive\Documentos\projeto\Converso>
```

---

## 3. Instalar as dependências

Com o ambiente **ativado**:

```powershell
pip install -r requirements.txt
```

As principais bibliotecas usadas:

- `pymupdf` – análise e extração avançada de PDF
- `python-docx` – criação de documentos Word
- `pdf2docx` – conversão complementar de PDF para DOCX
- `html2text` – suporte a outros formatos

---

## 4. Usar o conversor

Com o venv ativo e dependências instaladas, rode:

```powershell
# PDF para DOCX (detecta automaticamente)
python conversor.py documento.pdf -v

# DOCX para PDF (detecta automaticamente)
python conversor.py documento.docx -v

# TXT para PDF
python conversor.py texto.txt -v

# Markdown para PDF
python conversor.py arquivo.md -v
```

### Opções principais

| Opção | Descrição |
| ----- | --------- |
| `--to` / `-t` | Formato de saída (`docx`, `pdf`). Detecta automaticamente se omitido |
| `--output` / `-o` | Caminho do arquivo ou pasta de saída |
| `--start-page` | Página inicial (1-based) |
| `--end-page` | Página final (1-based, inclusiva) |
| `--verbose` / `-v` | Mostra informações detalhadas |

### Opções de cabeçalho e rodapé

| Opção | Descrição |
| ----- | --------- |
| `--header-mode` | `keep`, `remove` ou `convert` (padrão: convert) |
| `--footer-mode` | `keep`, `remove` ou `convert` (padrão: convert) |
| `--header-margin` | Proporção da página para cabeçalho (padrão: 0.10) |
| `--footer-margin` | Proporção da página para rodapé (padrão: 0.10) |

### Opções de qualidade e formatação

| Opção | Descrição |
| ----- | --------- |
| `--quality` / `-q` | `fast`, `balanced` ou `high` (padrão: balanced) |
| `--no-formatting` | Desativa preservação de formatação |
| `--no-layout` | Desativa preservação de layout |
| `--no-merge-paragraphs` | Desativa mesclagem de parágrafos |
| `--keep-hyphenation` | Mantém hifenização de fim de linha |

### Opções de imagem

| Opção | Descrição |
| ----- | --------- |
| `--no-images` | Não extrai imagens do PDF |
| `--image-quality` | Qualidade JPEG, 1-100 (padrão: 95) |
| `--max-image-width` | Largura máxima em pixels (padrão: 800) |

### Exemplos

```powershell
# === PDF para DOCX ===

# Conversão básica (detecta formato automaticamente)
python conversor.py docs\relatorio.pdf -v

# Alta qualidade com todas as otimizações
python conversor.py docs\relatorio.pdf --to docx --quality high -v

# Converter apenas da página 2 até a 5
python conversor.py docs\relatorio.pdf --start-page 2 --end-page 5 -v

# Remover cabeçalhos e rodapés
python conversor.py docs\relatorio.pdf --header-mode remove --footer-mode remove -v

# Conversão rápida sem imagens
python conversor.py docs\relatorio.pdf --quality fast --no-images -v

# === DOCX para PDF ===

# Conversão básica (detecta formato automaticamente)
python conversor.py docs\documento.docx -v

# Especificar arquivo de saída
python conversor.py docs\documento.docx -o "C:\saida\documento_final.pdf" -v

# === TXT para PDF ===

python conversor.py notas.txt -v

# === Markdown para PDF ===

python conversor.py README.md -o documentacao.pdf -v
```

---

## 5. Próximos passos (roadmap rápido)

- Implementar conversão **PDF → HTML** usando `PyMuPDF`
- Gerar **Markdown** reaproveitando o HTML
- Adicionar testes automatizados com `pytest`
- Melhorar detecção de tabelas
- OCR para PDFs escaneados
- Melhorar conversão DOCX → PDF com suporte a imagens
