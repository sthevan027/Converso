# Converso – Conversor de PDF

Conversor em Python para transformar arquivos **PDF** em outros formatos.

Primeiro foco: **PDF → DOCX (Word)** com boa fidelidade de layout, usando a biblioteca [`pdf2docx`](https://github.com/ArtifexSoftware/pdf2docx.git).

Em seguida, serão adicionados conversores para **HTML** e **Markdown**.

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

- `pdf2docx` – conversão de PDF para DOCX
- `pymupdf` – leitura/extração de conteúdo e layout do PDF (para HTML/MD futuramente)
- `html2text`, `python-docx` – suporte a outros formatos

---

## 4. Usar o conversor (PDF → DOCX)

Com o venv ativo e dependências instaladas, rode:

```powershell
python conversor.py caminho\do\arquivo.pdf --to docx -v
```

### Opções principais

- **`--to` / `-t`**: formato de saída
  - atualmente implementado: `docx`
- **`--output` / `-o`**: caminho do arquivo ou **pasta** de saída  
  - se não informar, gera `seu-arquivo.docx` na mesma pasta do PDF
- **`--start-page`**: página inicial (numeração começa em 1)
- **`--end-page`**: página final (1‑based, inclusiva)
- **`--verbose` / `-v`**: mostra informações detalhadas da conversão

### Exemplos

```powershell
# Converter o PDF inteiro para DOCX
python conversor.py docs\relatorio.pdf --to docx -v

# Converter apenas da página 2 até a 5
python conversor.py docs\relatorio.pdf --to docx --start-page 2 --end-page 5 -v

# Salvar com um nome e pasta específicos
python conversor.py docs\relatorio.pdf --to docx -o "C:\saida\relatorio_convertido.docx" -v
```

---

## 5. Próximos passos (roadmap rápido)

- Implementar conversão **PDF → HTML** usando `PyMuPDF`
- Gerar **Markdown** reaproveitando o HTML
- Adicionar testes automatizados com `pytest`

---