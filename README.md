# Converso – Conversor de PDF

Conversor avançado em Python para transformar arquivos **PDF** em outros formatos com alta fidelidade.

**PDF → DOCX (Word)** com detecção inteligente de estrutura, cabeçalhos, rodapés e otimização de transcrição.

Em seguida, serão adicionados conversores para **HTML** e **Markdown**.

---

## Funcionalidades

- **Detecção automática de cabeçalhos e rodapés** - Identifica e converte para cabeçalho/rodapé nativo do Word
- **Preservação de formatação** - Mantém negrito, itálico e estilos de fonte
- **Mesclagem inteligente de parágrafos** - Une parágrafos fragmentados automaticamente
- **Remoção de hifenização** - Remove hífens de quebra de linha
- **Extração de imagens** - Extrai e incorpora imagens do PDF
- **Detecção de títulos** - Identifica e aplica estilos de Heading automaticamente
- **Qualidade configurável** - Modos fast, balanced e high para diferentes necessidades

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

## 4. Usar o conversor (PDF → DOCX)

Com o venv ativo e dependências instaladas, rode:

```powershell
python conversor.py caminho\do\arquivo.pdf --to docx -v
```

### Opções principais

| Opção | Descrição |
|-------|-----------|
| `--to` / `-t` | Formato de saída (atualmente: `docx`) |
| `--output` / `-o` | Caminho do arquivo ou pasta de saída |
| `--start-page` | Página inicial (1-based) |
| `--end-page` | Página final (1-based, inclusiva) |
| `--verbose` / `-v` | Mostra informações detalhadas |

### Opções de cabeçalho e rodapé

| Opção | Descrição |
|-------|-----------|
| `--header-mode` | `keep`, `remove` ou `convert` (padrão: convert) |
| `--footer-mode` | `keep`, `remove` ou `convert` (padrão: convert) |
| `--header-margin` | Proporção da página para cabeçalho (padrão: 0.10) |
| `--footer-margin` | Proporção da página para rodapé (padrão: 0.10) |

### Opções de qualidade e formatação

| Opção | Descrição |
|-------|-----------|
| `--quality` / `-q` | `fast`, `balanced` ou `high` (padrão: balanced) |
| `--no-formatting` | Desativa preservação de formatação |
| `--no-layout` | Desativa preservação de layout |
| `--no-merge-paragraphs` | Desativa mesclagem de parágrafos |
| `--keep-hyphenation` | Mantém hifenização de fim de linha |

### Opções de imagem

| Opção | Descrição |
|-------|-----------|
| `--no-images` | Não extrai imagens do PDF |
| `--image-quality` | Qualidade JPEG, 1-100 (padrão: 95) |
| `--max-image-width` | Largura máxima em pixels (padrão: 800) |

### Exemplos

```powershell
# Conversão básica com detalhes
python conversor.py docs\relatorio.pdf --to docx -v

# Alta qualidade com todas as otimizações
python conversor.py docs\relatorio.pdf --to docx --quality high -v

# Converter apenas da página 2 até a 5
python conversor.py docs\relatorio.pdf --to docx --start-page 2 --end-page 5 -v

# Remover cabeçalhos e rodapés completamente
python conversor.py docs\relatorio.pdf --to docx --header-mode remove --footer-mode remove -v

# Conversão rápida sem imagens
python conversor.py docs\relatorio.pdf --to docx --quality fast --no-images -v

# Ajustar margem de cabeçalho para 15% da página
python conversor.py docs\relatorio.pdf --to docx --header-margin 0.15 -v

# Salvar com um nome e pasta específicos
python conversor.py docs\relatorio.pdf --to docx -o "C:\saida\relatorio_convertido.docx" -v
```

---

## 5. Próximos passos (roadmap rápido)

- Implementar conversão **PDF → HTML** usando `PyMuPDF`
- Gerar **Markdown** reaproveitando o HTML
- Adicionar testes automatizados com `pytest`
- Melhorar detecção de tabelas
- OCR para PDFs escaneados

---