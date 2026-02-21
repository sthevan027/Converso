"""
Script para criar PDFs de teste e testes unitários do conversor.
Execute com: pytest tests/create_test_pdf.py -v
"""
from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import fitz  # PyMuPDF
import pytest
from docx import Document

# Adiciona o diretório raiz ao path para importar os módulos
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from conversores.base import ConversionOptions, HeaderFooterMode
from conversores.docx_converter import DocxConverter


# ==============================================================================
# FIXTURES E HELPERS
# ==============================================================================


@pytest.fixture
def temp_dir():
    """Cria diretório temporário para os testes."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Cria um PDF de teste básico e retorna o caminho."""
    pdf_path = os.path.join(temp_dir, "sample.pdf")
    create_simple_pdf(pdf_path)
    return pdf_path


@pytest.fixture
def complex_pdf_path(temp_dir):
    """Cria um PDF complexo com múltiplos elementos."""
    pdf_path = os.path.join(temp_dir, "complex.pdf")
    create_complex_pdf(pdf_path)
    return pdf_path


@pytest.fixture
def multipage_pdf_path(temp_dir):
    """Cria um PDF com múltiplas páginas."""
    pdf_path = os.path.join(temp_dir, "multipage.pdf")
    create_multipage_pdf(pdf_path)
    return pdf_path


# ==============================================================================
# FUNÇÕES DE CRIAÇÃO DE PDFs DE TESTE
# ==============================================================================


def create_simple_pdf(output_path: str) -> None:
    """Cria um PDF simples com texto básico."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4

    # Título
    title_rect = fitz.Rect(50, 50, 545, 90)
    page.insert_textbox(
        title_rect,
        "Documento de Teste Simples",
        fontsize=20,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Parágrafo
    body_rect = fitz.Rect(50, 120, 545, 400)
    page.insert_textbox(
        body_rect,
        """Este é um documento de teste simples para validar o conversor PDF para DOCX.

O conversor deve ser capaz de extrair este texto corretamente e preservar a estrutura básica do documento.""",
        fontsize=12,
        align=fitz.TEXT_ALIGN_JUSTIFY,
    )

    doc.save(output_path)
    doc.close()


def create_complex_pdf(output_path: str) -> None:
    """Cria um PDF complexo com diferentes elementos."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    # Cabeçalho
    header_rect = fitz.Rect(50, 20, 545, 45)
    page.insert_textbox(
        header_rect,
        "Empresa XYZ - Relatório Técnico",
        fontsize=10,
        align=fitz.TEXT_ALIGN_CENTER,
    )
    page.draw_line(fitz.Point(50, 50), fitz.Point(545, 50), width=0.5)

    # Título principal
    title_rect = fitz.Rect(50, 60, 545, 100)
    page.insert_textbox(
        title_rect,
        "Relatório de Análise Completa",
        fontsize=22,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Subtítulo
    subtitle_rect = fitz.Rect(50, 110, 545, 140)
    page.insert_textbox(
        subtitle_rect,
        "1. Introdução",
        fontsize=16,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    # Texto com parágrafos
    body_text = """Este relatório apresenta uma análise detalhada dos resultados obtidos durante o período de avaliação. Os dados foram coletados utilizando metodologias padronizadas e validadas pela comunidade científica.

A análise contempla os seguintes aspectos principais:
• Desempenho do sistema em diferentes cenários
• Comparação com benchmarks estabelecidos
• Identificação de pontos de melhoria
• Recomendações para otimização

Os resultados demonstram que o sistema atende aos requisitos estabelecidos, com margem de segurança adequada para operação em ambiente de produção."""

    body_rect = fitz.Rect(50, 150, 545, 450)
    page.insert_textbox(
        body_rect,
        body_text,
        fontsize=11,
        align=fitz.TEXT_ALIGN_JUSTIFY,
    )

    # Segundo subtítulo
    subtitle2_rect = fitz.Rect(50, 460, 545, 490)
    page.insert_textbox(
        subtitle2_rect,
        "2. Metodologia",
        fontsize=16,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    methodology_text = """A metodologia utilizada segue as diretrizes estabelecidas pela norma ISO 9001:2015, garantindo rastreabilidade e reprodutibilidade dos resultados. Os testes foram conduzidos em ambiente controlado, com temperatura entre 20°C e 25°C e umidade relativa de 50% ± 10%.

Foram realizadas 100 iterações para cada cenário de teste, permitindo análise estatística robusta com intervalo de confiança de 95%."""

    method_rect = fitz.Rect(50, 500, 545, 700)
    page.insert_textbox(
        method_rect,
        methodology_text,
        fontsize=11,
        align=fitz.TEXT_ALIGN_JUSTIFY,
    )

    # Linha do rodapé
    page.draw_line(fitz.Point(50, 780), fitz.Point(545, 780), width=0.5)

    # Rodapé
    footer_rect = fitz.Rect(50, 790, 545, 820)
    page.insert_textbox(
        footer_rect,
        "Página 1 de 1 | Confidencial | Data: 21/02/2026",
        fontsize=9,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    doc.save(output_path)
    doc.close()


def create_multipage_pdf(output_path: str, num_pages: int = 5) -> None:
    """Cria um PDF com múltiplas páginas para teste de paginação."""
    doc = fitz.open()

    for page_num in range(1, num_pages + 1):
        page = doc.new_page(width=595, height=842)

        # Cabeçalho consistente
        header_rect = fitz.Rect(50, 25, 545, 50)
        page.insert_textbox(
            header_rect,
            "Documento Multi-Páginas - Teste de Conversão",
            fontsize=10,
            align=fitz.TEXT_ALIGN_CENTER,
        )
        page.draw_line(fitz.Point(50, 55), fitz.Point(545, 55), width=0.5)

        # Título da página
        if page_num == 1:
            title_rect = fitz.Rect(50, 70, 545, 110)
            page.insert_textbox(
                title_rect,
                "Manual de Testes do Conversor PDF",
                fontsize=20,
                align=fitz.TEXT_ALIGN_CENTER,
            )
            y_start = 130
        else:
            y_start = 70

        # Capítulo
        chapter_rect = fitz.Rect(50, y_start, 545, y_start + 30)
        page.insert_textbox(
            chapter_rect,
            f"Capítulo {page_num}: Seção de Teste {page_num}",
            fontsize=14,
            align=fitz.TEXT_ALIGN_LEFT,
        )

        # Conteúdo variado por página
        content = _get_page_content(page_num)
        body_rect = fitz.Rect(50, y_start + 40, 545, 750)
        page.insert_textbox(
            body_rect,
            content,
            fontsize=11,
            align=fitz.TEXT_ALIGN_JUSTIFY,
        )

        # Rodapé
        page.draw_line(fitz.Point(50, 780), fitz.Point(545, 780), width=0.5)
        footer_rect = fitz.Rect(50, 790, 545, 820)
        page.insert_textbox(
            footer_rect,
            f"Página {page_num} de {num_pages} | Documento de Teste",
            fontsize=9,
            align=fitz.TEXT_ALIGN_CENTER,
        )

    doc.save(output_path)
    doc.close()


def _get_page_content(page_num: int) -> str:
    """Retorna conteúdo específico para cada página."""
    contents = {
        1: """Bem-vindo ao manual de testes do conversor PDF para DOCX. Este documento foi criado para validar todas as funcionalidades do sistema de conversão.

O conversor suporta as seguintes características:
• Extração de texto com preservação de formatação
• Detecção automática de cabeçalhos e rodapés
• Reconhecimento de estrutura de parágrafos
• Identificação de listas e itens
• Manutenção da hierarquia de títulos

Este documento serve como base para testes automatizados e validação manual do sistema.""",
        2: """Esta seção detalha os aspectos técnicos da conversão de documentos PDF para o formato DOCX.

Processo de Conversão:
1. Análise do documento PDF de entrada
2. Extração de blocos de texto com metadados
3. Identificação de regiões de cabeçalho e rodapé
4. Agrupamento de blocos em parágrafos lógicos
5. Aplicação de estilos e formatação
6. Geração do documento DOCX final

O processo é otimizado para manter a fidelidade visual enquanto produz documentos editáveis e acessíveis.""",
        3: """Nesta seção apresentamos casos de teste específicos para validação do conversor.

Cenário 1: Texto Simples
Documentos contendo apenas parágrafos de texto sem formatação especial devem ser convertidos mantendo a estrutura de parágrafos original.

Cenário 2: Texto Formatado
Textos com negrito, itálico e diferentes tamanhos de fonte devem ter a formatação preservada na conversão.

Cenário 3: Listas
Listas com marcadores e listas numeradas devem ser identificadas e convertidas para o formato apropriado do Word.""",
        4: """Esta seção aborda o tratamento de casos especiais durante a conversão.

Hifenização:
Palavras divididas no final de linhas por hifens devem ser reunidas automaticamente. Por exem-
plo, esta palavra deve aparecer inteira no documento final.

Cabeçalhos e Rodapés Repetitivos:
O sistema detecta automaticamente conteúdo que se repete em todas as páginas e pode convertê-lo para cabeçalhos/rodapés nativos do Word.

Margens e Layout:
As margens do documento original são respeitadas, e o layout geral é preservado dentro das limitações do formato DOCX.""",
        5: """Seção final com considerações sobre qualidade e limitações.

Limitações Conhecidas:
• Layouts de múltiplas colunas têm suporte limitado
• Elementos gráficos complexos podem não ser preservados
• Fontes não-padrão podem ser substituídas

Recomendações:
Para melhores resultados, utilize documentos PDF com estrutura clara e fontes padrão. Revise sempre o documento convertido para garantir a qualidade desejada.

Agradecemos por utilizar nosso conversor!""",
    }
    return contents.get(page_num, f"Conteúdo genérico para a página {page_num}.")


def create_pdf_with_table(output_path: str) -> None:
    """Cria um PDF com tabela simulada."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    # Título
    title_rect = fitz.Rect(50, 50, 545, 90)
    page.insert_textbox(
        title_rect,
        "Relatório com Tabela de Dados",
        fontsize=18,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Tabela simulada com linhas
    table_data = [
        ["ID", "Nome", "Valor", "Status"],
        ["001", "Item Alpha", "R$ 150,00", "Ativo"],
        ["002", "Item Beta", "R$ 250,00", "Inativo"],
        ["003", "Item Gamma", "R$ 350,00", "Ativo"],
        ["004", "Item Delta", "R$ 450,00", "Pendente"],
    ]

    y_start = 120
    row_height = 25
    col_widths = [60, 150, 100, 80]

    # Desenha a tabela
    for row_idx, row in enumerate(table_data):
        x = 70
        y = y_start + row_idx * row_height

        # Linha horizontal
        page.draw_line(
            fitz.Point(70, y),
            fitz.Point(70 + sum(col_widths), y),
            width=0.5 if row_idx > 0 else 1,
        )

        for col_idx, cell in enumerate(row):
            cell_rect = fitz.Rect(x, y + 5, x + col_widths[col_idx] - 5, y + row_height)
            fontsize = 10 if row_idx > 0 else 11
            page.insert_textbox(
                cell_rect,
                cell,
                fontsize=fontsize,
                align=fitz.TEXT_ALIGN_LEFT,
            )
            x += col_widths[col_idx]

    # Linha final da tabela
    final_y = y_start + len(table_data) * row_height
    page.draw_line(fitz.Point(70, final_y), fitz.Point(70 + sum(col_widths), final_y), width=0.5)

    doc.save(output_path)
    doc.close()


def create_pdf_with_lists(output_path: str) -> None:
    """Cria um PDF com diferentes tipos de listas."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    # Título
    title_rect = fitz.Rect(50, 50, 545, 90)
    page.insert_textbox(
        title_rect,
        "Documento com Listas",
        fontsize=18,
        align=fitz.TEXT_ALIGN_CENTER,
    )

    # Lista com bullets
    bullet_section = """Lista de Características:

• Fácil de usar
• Interface intuitiva
• Alta performance
• Baixo consumo de memória
• Compatível com múltiplos formatos"""

    bullet_rect = fitz.Rect(50, 110, 545, 280)
    page.insert_textbox(
        bullet_rect,
        bullet_section,
        fontsize=12,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    # Lista numerada
    numbered_section = """Passos para Instalação:

1. Baixe o instalador do site oficial
2. Execute o arquivo de instalação
3. Aceite os termos de uso
4. Escolha o diretório de instalação
5. Aguarde a conclusão
6. Reinicie o computador se necessário"""

    numbered_rect = fitz.Rect(50, 300, 545, 500)
    page.insert_textbox(
        numbered_rect,
        numbered_section,
        fontsize=12,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    # Lista com sub-itens
    nested_section = """Estrutura do Projeto:

- src/
  - components/
  - utils/
  - services/
- tests/
  - unit/
  - integration/
- docs/"""

    nested_rect = fitz.Rect(50, 520, 545, 720)
    page.insert_textbox(
        nested_rect,
        nested_section,
        fontsize=12,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    doc.save(output_path)
    doc.close()


def create_test_pdf(output_path: str = "tests/test_document.pdf") -> None:
    """Cria um PDF de teste completo com cabeçalho, rodapé, títulos e texto.
    
    Esta é a função principal para criar um documento de teste padrão.
    """
    doc = fitz.open()

    for page_num in range(1, 4):
        page = doc.new_page(width=595, height=842)  # A4

        # Cabeçalho
        header_rect = fitz.Rect(50, 30, 545, 60)
        page.insert_textbox(
            header_rect,
            "Empresa ABC - Documento de Teste",
            fontsize=10,
            align=fitz.TEXT_ALIGN_CENTER,
        )

        # Linha separadora do cabeçalho
        page.draw_line(fitz.Point(50, 65), fitz.Point(545, 65), width=0.5)

        # Título principal (apenas na primeira página)
        if page_num == 1:
            title_rect = fitz.Rect(50, 80, 545, 120)
            page.insert_textbox(
                title_rect,
                "Relatório de Testes do Conversor PDF",
                fontsize=18,
                align=fitz.TEXT_ALIGN_CENTER,
            )
            y_start = 140
        else:
            y_start = 80

        # Subtítulo
        subtitle_rect = fitz.Rect(50, y_start, 545, y_start + 30)
        page.insert_textbox(
            subtitle_rect,
            f"Capítulo {page_num}: Seção de Teste",
            fontsize=14,
            align=fitz.TEXT_ALIGN_LEFT,
        )

        # Corpo do texto
        body_text = """
Este é um parágrafo de teste para verificar a conversão de PDF para Word. 
O texto deve ser extraído corretamente, mantendo a formatação e estrutura 
do documento original.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod 
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim 
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
commodo consequat.

Características importantes do conversor:
- Detecção automática de cabeçalhos
- Identificação de rodapés
- Preservação de formatação
- Extração de imagens
- Mesclagem de parágrafos

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum 
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non 
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""
        body_rect = fitz.Rect(50, y_start + 40, 545, 750)
        page.insert_textbox(
            body_rect,
            body_text.strip(),
            fontsize=11,
            align=fitz.TEXT_ALIGN_JUSTIFY,
        )

        # Linha separadora do rodapé
        page.draw_line(fitz.Point(50, 780), fitz.Point(545, 780), width=0.5)

        # Rodapé
        footer_rect = fitz.Rect(50, 790, 545, 820)
        page.insert_textbox(
            footer_rect,
            f"Página {page_num} de 3 | Confidencial",
            fontsize=9,
            align=fitz.TEXT_ALIGN_CENTER,
        )

    doc.save(output_path)
    doc.close()
    print(f"PDF de teste criado: {output_path}")


# ==============================================================================
# TESTES UNITÁRIOS
# ==============================================================================


class TestPDFCreation:
    """Testes para verificar a criação dos PDFs de teste."""

    def test_create_simple_pdf(self, temp_dir):
        """Testa criação de PDF simples."""
        pdf_path = os.path.join(temp_dir, "simple.pdf")
        create_simple_pdf(pdf_path)

        assert os.path.exists(pdf_path)
        doc = fitz.open(pdf_path)
        assert len(doc) == 1
        text = doc[0].get_text()
        assert "Documento de Teste Simples" in text
        doc.close()

    def test_create_complex_pdf(self, temp_dir):
        """Testa criação de PDF complexo."""
        pdf_path = os.path.join(temp_dir, "complex.pdf")
        create_complex_pdf(pdf_path)

        assert os.path.exists(pdf_path)
        doc = fitz.open(pdf_path)
        assert len(doc) == 1
        text = doc[0].get_text()
        assert "Relatório de Análise Completa" in text
        assert "Introdução" in text
        assert "Metodologia" in text
        doc.close()

    def test_create_multipage_pdf(self, temp_dir):
        """Testa criação de PDF com múltiplas páginas."""
        pdf_path = os.path.join(temp_dir, "multipage.pdf")
        create_multipage_pdf(pdf_path, num_pages=3)

        assert os.path.exists(pdf_path)
        doc = fitz.open(pdf_path)
        assert len(doc) == 3
        doc.close()

    def test_create_pdf_with_table(self, temp_dir):
        """Testa criação de PDF com tabela."""
        pdf_path = os.path.join(temp_dir, "table.pdf")
        create_pdf_with_table(pdf_path)

        assert os.path.exists(pdf_path)
        doc = fitz.open(pdf_path)
        text = doc[0].get_text()
        assert "Item Alpha" in text
        assert "R$ 150,00" in text
        doc.close()

    def test_create_pdf_with_lists(self, temp_dir):
        """Testa criação de PDF com listas."""
        pdf_path = os.path.join(temp_dir, "lists.pdf")
        create_pdf_with_lists(pdf_path)

        assert os.path.exists(pdf_path)
        doc = fitz.open(pdf_path)
        text = doc[0].get_text()
        assert "Fácil de usar" in text
        assert "Baixe o instalador" in text
        doc.close()


class TestDocxConverter:
    """Testes para o conversor DOCX."""

    def test_converter_basic(self, sample_pdf_path, temp_dir):
        """Testa conversão básica de PDF para DOCX."""
        output_path = os.path.join(temp_dir, "output.docx")
        converter = DocxConverter()

        result = converter.convert(sample_pdf_path, output_path)

        assert result.success
        assert os.path.exists(output_path)
        assert result.pages_converted > 0

    def test_converter_preserves_text(self, sample_pdf_path, temp_dir):
        """Verifica que o texto é preservado na conversão."""
        output_path = os.path.join(temp_dir, "output.docx")
        converter = DocxConverter()

        converter.convert(sample_pdf_path, output_path)

        doc = Document(output_path)
        full_text = "\n".join([p.text for p in doc.paragraphs])

        assert "documento de teste" in full_text.lower()
        assert "conversor" in full_text.lower()

    def test_converter_with_options(self, complex_pdf_path, temp_dir):
        """Testa conversão com opções customizadas."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(
            verbose=True,
            preserve_formatting=True,
            merge_paragraphs=True,
            remove_hyphenation=True,
        )
        converter = DocxConverter(options)

        result = converter.convert(complex_pdf_path, output_path)

        assert result.success
        assert os.path.exists(output_path)

    def test_converter_header_mode_keep(self, multipage_pdf_path, temp_dir):
        """Testa modo de manter cabeçalhos no corpo."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(
            header_mode=HeaderFooterMode.KEEP,
            footer_mode=HeaderFooterMode.KEEP,
        )
        converter = DocxConverter(options)

        result = converter.convert(multipage_pdf_path, output_path)

        assert result.success

    def test_converter_header_mode_remove(self, multipage_pdf_path, temp_dir):
        """Testa remoção de cabeçalhos e rodapés."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(
            header_mode=HeaderFooterMode.REMOVE,
            footer_mode=HeaderFooterMode.REMOVE,
        )
        converter = DocxConverter(options)

        result = converter.convert(multipage_pdf_path, output_path)

        assert result.success

    def test_converter_page_range(self, multipage_pdf_path, temp_dir):
        """Testa conversão de range específico de páginas."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(
            start_page=2,
            end_page=3,
        )
        converter = DocxConverter(options)

        result = converter.convert(multipage_pdf_path, output_path)

        assert result.success
        assert result.pages_converted == 2

    def test_converter_file_not_found(self, temp_dir):
        """Testa erro quando arquivo não existe."""
        converter = DocxConverter()

        with pytest.raises(FileNotFoundError):
            converter.convert("arquivo_inexistente.pdf", "output.docx")

    def test_converter_creates_output_directory(self, sample_pdf_path, temp_dir):
        """Testa que o conversor cria o diretório de saída."""
        output_path = os.path.join(temp_dir, "subdir", "nested", "output.docx")
        converter = DocxConverter()

        result = converter.convert(sample_pdf_path, output_path)

        assert result.success
        assert os.path.exists(output_path)


class TestConversionOptions:
    """Testes para as opções de conversão."""

    def test_default_options(self):
        """Testa valores padrão das opções."""
        options = ConversionOptions()

        assert options.start_page is None
        assert options.end_page is None
        assert options.verbose is False
        assert options.header_mode == HeaderFooterMode.CONVERT_TO_HEADER
        assert options.footer_mode == HeaderFooterMode.CONVERT_TO_HEADER
        assert options.preserve_formatting is True
        assert options.extract_images is True
        assert options.merge_paragraphs is True

    def test_custom_options(self):
        """Testa opções customizadas."""
        options = ConversionOptions(
            start_page=1,
            end_page=5,
            verbose=True,
            header_margin_ratio=0.15,
            footer_margin_ratio=0.12,
            image_quality=80,
            max_image_width=600,
        )

        assert options.start_page == 1
        assert options.end_page == 5
        assert options.verbose is True
        assert options.header_margin_ratio == 0.15
        assert options.footer_margin_ratio == 0.12
        assert options.image_quality == 80
        assert options.max_image_width == 600

    def test_invalid_page_range(self, sample_pdf_path, temp_dir):
        """Testa validação de range de páginas inválido."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(
            start_page=5,
            end_page=2,  # end < start é inválido
        )
        converter = DocxConverter(options)

        with pytest.raises(ValueError):
            converter.convert(sample_pdf_path, output_path)

    def test_negative_page_number(self, sample_pdf_path, temp_dir):
        """Testa validação de número de página negativo."""
        output_path = os.path.join(temp_dir, "output.docx")
        options = ConversionOptions(start_page=-1)
        converter = DocxConverter(options)

        with pytest.raises(ValueError):
            converter.convert(sample_pdf_path, output_path)


class TestConversionResult:
    """Testes para o resultado da conversão."""

    def test_result_attributes(self, sample_pdf_path, temp_dir):
        """Verifica atributos do resultado da conversão."""
        output_path = os.path.join(temp_dir, "output.docx")
        converter = DocxConverter()

        result = converter.convert(sample_pdf_path, output_path)

        assert hasattr(result, "success")
        assert hasattr(result, "output_path")
        assert hasattr(result, "pages_converted")
        assert hasattr(result, "headers_detected")
        assert hasattr(result, "footers_detected")
        assert hasattr(result, "images_extracted")
        assert hasattr(result, "warnings")
        assert hasattr(result, "errors")

    def test_result_output_path(self, sample_pdf_path, temp_dir):
        """Verifica que output_path no resultado corresponde ao arquivo criado."""
        output_path = os.path.join(temp_dir, "output.docx")
        converter = DocxConverter()

        result = converter.convert(sample_pdf_path, output_path)

        assert result.output_path == output_path


# ==============================================================================
# EXECUÇÃO DIRETA
# ==============================================================================


def create_all_test_pdfs(output_dir: str = "tests") -> None:
    """Cria todos os PDFs de teste no diretório especificado."""
    os.makedirs(output_dir, exist_ok=True)

    files = {
        "test_document.pdf": create_test_pdf,
        "simple_document.pdf": create_simple_pdf,
        "complex_document.pdf": create_complex_pdf,
        "multipage_document.pdf": lambda p: create_multipage_pdf(p, 5),
        "table_document.pdf": create_pdf_with_table,
        "list_document.pdf": create_pdf_with_lists,
    }

    for filename, creator in files.items():
        filepath = os.path.join(output_dir, filename)
        creator(filepath)
        print(f"Criado: {filepath}")

    print(f"\nTodos os {len(files)} PDFs de teste foram criados em '{output_dir}/'")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Criar PDFs de teste para o conversor")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Cria todos os tipos de PDFs de teste",
    )
    parser.add_argument(
        "--output-dir",
        default="tests",
        help="Diretório de saída (padrão: tests)",
    )
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Executa os testes após criar os PDFs",
    )

    args = parser.parse_args()

    if args.all:
        create_all_test_pdfs(args.output_dir)
    else:
        create_test_pdf(os.path.join(args.output_dir, "test_document.pdf"))

    if args.run_tests:
        import subprocess

        subprocess.run(["pytest", __file__, "-v"])
