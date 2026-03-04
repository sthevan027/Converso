# Converso – Conversor de Documentos

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=fff)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Conversor em Python para transformar documentos entre PDF, DOCX, TXT e Markdown com alta fidelidade.

---

## 📋 Conversões suportadas

| Entrada | Saída | Descrição |
|---------|-------|-----------|
| **PDF** | DOCX | Conversão com detecção de estrutura |
| **DOCX** | PDF | Preserva formatação e estilos |
| **TXT** | PDF | Texto para PDF formatado |
| **MD** | PDF | Markdown para PDF |

## 🚀 Como rodar

### Pré-requisitos

- Python 3.10+
- Windows (testado no PowerShell)

### Instalação rápida

```bash
# Clone o repositório
git clone https://github.com/sthevan027/Converso.git
cd Converso

# Crie e ative o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# ou
.\.venv\Scripts\activate.bat   # CMD

# Instale as dependências
pip install -r requirements.txt
```

### Uso via linha de comando

```bash
# PDF para DOCX
python conversor.py documento.pdf -v

# DOCX para PDF
python conversor.py documento.docx -v

# TXT ou Markdown para PDF
python conversor.py arquivo.txt -v
python conversor.py README.md -v
```

### Interface gráfica (GUI)

```bash
# Usando o launcher (recomendado)
.\run_converso.bat

# Ou manualmente
python run_gui.py
```

### Gerar executável .exe

```bash
.\build_exe.bat
# O .exe será criado em dist/Converso.exe
```

## 🛠️ Tecnologias

| Biblioteca | Uso |
|------------|-----|
| pymupdf | Análise e extração de PDF |
| python-docx | Documentos Word |
| pdf2docx | Conversão PDF→DOCX |
| customtkinter | Interface gráfica |
| PyInstaller | Gerar .exe |

## 📦 Opções principais

| Opção | Descrição |
|-------|-----------|
| `--to` / `-t` | Formato de saída (docx, pdf) |
| `--output` / `-o` | Arquivo ou pasta de saída |
| `--start-page` | Página inicial |
| `--end-page` | Página final |
| `--verbose` / `-v` | Saída detalhada |
| `--quality` | fast, balanced, high |
| `--no-images` | Não extrair imagens |

## 📁 Estrutura

```
Converso/
├── conversor.py          # Script principal
├── run_gui.py            # Launcher da GUI
├── run_converso.bat      # Script de execução
├── build_exe.bat         # Build do executável
├── converso.spec         # Config PyInstaller
├── requirements.txt
├── conversores/          # Módulos de conversão
├── gui/                  # Interface gráfica
├── utils/
└── tests/
```

---

**Desenvolvido por [Sthevan Santos](https://github.com/sthevan027)**
