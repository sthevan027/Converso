from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from utils.pdf_analyzer import PDFAnalyzer, PageAnalysis, TextBlock

from .base import (
    BaseConverter,
    ConversionOptions,
    ConversionResult,
    HeaderFooterMode,
)


class DocxConverter(BaseConverter):
    """Conversor avançado de PDF para DOCX com detecção de estrutura."""

    def __init__(self, options: Optional[ConversionOptions] = None) -> None:
        super().__init__(options)
        self._analyzer = PDFAnalyzer(
            header_margin_ratio=self.options.header_margin_ratio,
            footer_margin_ratio=self.options.footer_margin_ratio,
        )
        self._result: ConversionResult = None  # type: ignore

    def convert(self, pdf_path: str, output_path: str) -> ConversionResult:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_file():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_file}")

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        self._result = ConversionResult(
            success=False,
            output_path=str(output_file),
        )

        start, end = self._resolve_page_range()

        self._log(f"[DOCX] Analisando '{pdf_file}'...")

        try:
            doc = fitz.open(str(pdf_file))
            analysis = self._analyzer.analyze_document(
                str(pdf_file),
                start_page=(start - 1) if start else 0,
                end_page=end if end else None,
            )

            self._log(f"[DOCX] Convertendo {len(analysis.pages)} páginas...")

            word_doc = Document()
            self._setup_document(word_doc, doc)

            for page_analysis in analysis.pages:
                self._convert_page(word_doc, doc, page_analysis, analysis)
                self._result.pages_converted += 1

            if analysis.common_header:
                self._result.headers_detected = len(analysis.pages)
            if analysis.common_footer:
                self._result.footers_detected = len(analysis.pages)

            word_doc.save(str(output_file))
            doc.close()

            self._result.success = True
            self._log(f"[DOCX] Arquivo gerado: {output_file}")

        except Exception as e:
            self._result.errors.append(str(e))
            raise

        return self._result

    def _setup_document(self, word_doc: Document, pdf_doc: fitz.Document) -> None:
        """Configura o documento Word com base no PDF."""
        if len(pdf_doc) > 0:
            page = pdf_doc[0]
            width_pt = page.rect.width
            height_pt = page.rect.height

            section = word_doc.sections[0]

            if width_pt > height_pt:
                section.orientation = WD_ORIENT.LANDSCAPE
                section.page_width = Pt(height_pt)
                section.page_height = Pt(width_pt)
            else:
                section.orientation = WD_ORIENT.PORTRAIT
                section.page_width = Pt(width_pt)
                section.page_height = Pt(height_pt)

            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)

    def _convert_page(
        self,
        word_doc: Document,
        pdf_doc: fitz.Document,
        page_analysis: PageAnalysis,
        doc_analysis,
    ) -> None:
        """Converte uma página do PDF para o documento Word."""
        page = pdf_doc[page_analysis.page_num]

        if self.options.header_mode == HeaderFooterMode.CONVERT_TO_HEADER:
            if page_analysis.header_text and doc_analysis.common_header:
                self._add_word_header(word_doc, page_analysis.header_text)

        if self.options.extract_images:
            self._extract_and_add_images(word_doc, page, page_analysis)

        self._add_body_content(word_doc, page_analysis)

        if self.options.footer_mode == HeaderFooterMode.CONVERT_TO_HEADER:
            if page_analysis.footer_text and doc_analysis.common_footer:
                self._add_word_footer(word_doc, page_analysis.footer_text)

        if page_analysis.page_num < len(pdf_doc) - 1:
            word_doc.add_page_break()

    def _add_body_content(self, word_doc: Document, page_analysis: PageAnalysis) -> None:
        """Adiciona o conteúdo do corpo da página."""
        if not page_analysis.body_blocks:
            return

        sorted_blocks = sorted(page_analysis.body_blocks, key=lambda b: (b.y0, b.x0))

        paragraphs = self._group_into_paragraphs(sorted_blocks)

        for para_blocks in paragraphs:
            if not para_blocks:
                continue

            text = self._blocks_to_paragraph_text(para_blocks)
            if not text.strip():
                continue

            if self.options.remove_hyphenation:
                text = self._remove_hyphenation(text)

            if self.options.merge_paragraphs:
                text = self._clean_paragraph(text)

            para = word_doc.add_paragraph()

            if self._is_title_block(para_blocks):
                self._apply_title_style(para, para_blocks[0])
            else:
                self._apply_paragraph_style(para, para_blocks)

            run = para.add_run(text)
            self._apply_text_formatting(run, para_blocks)

    def _group_into_paragraphs(self, blocks: list[TextBlock]) -> list[list[TextBlock]]:
        """Agrupa blocos de texto em parágrafos lógicos."""
        if not blocks:
            return []

        paragraphs: list[list[TextBlock]] = []
        current_para: list[TextBlock] = []
        last_y: float = -1
        last_font_size: float = 0

        for block in blocks:
            if last_y < 0:
                current_para.append(block)
                last_y = block.y1
                last_font_size = block.font_size
                continue

            line_spacing = block.y0 - last_y
            threshold = max(last_font_size, block.font_size) * 1.8

            if line_spacing > threshold:
                if current_para:
                    paragraphs.append(current_para)
                current_para = [block]
            else:
                current_para.append(block)

            last_y = block.y1
            last_font_size = block.font_size

        if current_para:
            paragraphs.append(current_para)

        return paragraphs

    def _blocks_to_paragraph_text(self, blocks: list[TextBlock]) -> str:
        """Converte blocos em texto de parágrafo."""
        if not blocks:
            return ""

        lines: list[list[TextBlock]] = []
        current_line: list[TextBlock] = []
        last_y: float = -1

        for block in sorted(blocks, key=lambda b: (b.y0, b.x0)):
            if last_y < 0 or abs(block.y0 - last_y) < block.font_size * 0.7:
                current_line.append(block)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = [block]
            last_y = block.y0

        if current_line:
            lines.append(current_line)

        text_lines = []
        for line in lines:
            sorted_line = sorted(line, key=lambda b: b.x0)
            line_text = " ".join(b.text for b in sorted_line)
            text_lines.append(line_text)

        return "\n".join(text_lines)

    def _remove_hyphenation(self, text: str) -> str:
        """Remove hifenização de fim de linha."""
        return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    def _clean_paragraph(self, text: str) -> str:
        """Limpa e normaliza o texto do parágrafo."""
        text = re.sub(r"\n(?![A-Z•\-\d])", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _is_title_block(self, blocks: list[TextBlock]) -> bool:
        """Verifica se os blocos representam um título."""
        if not blocks:
            return False

        avg_size = sum(b.font_size for b in blocks) / len(blocks)
        has_bold = any(b.is_bold for b in blocks)
        short_text = len(self._blocks_to_paragraph_text(blocks)) < 100

        return (avg_size > 14 or has_bold) and short_text

    def _apply_title_style(self, para, first_block: TextBlock) -> None:
        """Aplica estilo de título ao parágrafo."""
        if first_block.font_size >= 18:
            para.style = "Heading 1"
        elif first_block.font_size >= 14:
            para.style = "Heading 2"
        else:
            para.style = "Heading 3"

    def _apply_paragraph_style(self, para, blocks: list[TextBlock]) -> None:
        """Aplica estilo ao parágrafo baseado na análise."""
        if blocks:
            first_block = blocks[0]

            if first_block.x0 > 100:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def _apply_text_formatting(self, run, blocks: list[TextBlock]) -> None:
        """Aplica formatação de texto (negrito, itálico, fonte)."""
        if not blocks or not self.options.preserve_formatting:
            return

        first_block = blocks[0]

        has_bold = any(b.is_bold for b in blocks)
        has_italic = any(b.is_italic for b in blocks)

        run.bold = has_bold
        run.italic = has_italic

        if first_block.font_size > 0:
            run.font.size = Pt(min(first_block.font_size, 24))

    def _extract_and_add_images(
        self,
        word_doc: Document,
        page: fitz.Page,
        page_analysis: PageAnalysis,
    ) -> None:
        """Extrai e adiciona imagens da página."""
        image_list = page.get_images(full=True)

        for img_info in image_list:
            try:
                xref = img_info[0]
                base_image = page.parent.extract_image(xref)

                if base_image:
                    image_bytes = base_image["image"]
                    image_stream = io.BytesIO(image_bytes)

                    max_width = Inches(self.options.max_image_width / 96)

                    word_doc.add_picture(image_stream, width=max_width)
                    self._result.images_extracted += 1

            except Exception as e:
                self._result.warnings.append(f"Erro ao extrair imagem: {e}")

    def _add_word_header(self, word_doc: Document, header_text: str) -> None:
        """Adiciona cabeçalho ao documento Word."""
        section = word_doc.sections[-1]
        header = section.header
        para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()

        clean_text = re.sub(r"\{NUM\}", "", header_text).strip()
        if clean_text:
            para.text = clean_text
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def _add_word_footer(self, word_doc: Document, footer_text: str) -> None:
        """Adiciona rodapé ao documento Word."""
        section = word_doc.sections[-1]
        footer = section.footer
        para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()

        clean_text = re.sub(r"\{NUM\}", "", footer_text).strip()
        if clean_text:
            para.text = clean_text
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        self._add_page_number_field(para)

    def _add_page_number_field(self, para) -> None:
        """Adiciona campo de número de página."""
        run = para.add_run()
        fld_char_begin = OxmlElement("w:fldChar")
        fld_char_begin.set(qn("w:fldCharType"), "begin")

        instr_text = OxmlElement("w:instrText")
        instr_text.text = "PAGE"

        fld_char_end = OxmlElement("w:fldChar")
        fld_char_end.set(qn("w:fldCharType"), "end")

        run._r.append(fld_char_begin)
        run._r.append(instr_text)
        run._r.append(fld_char_end)

    def _resolve_page_range(self) -> tuple[Optional[int], Optional[int]]:
        """Garante que o range de páginas seja coerente (1-based)."""
        start = self.options.start_page
        end = self.options.end_page

        if start is not None and start <= 0:
            raise ValueError("start_page deve ser >= 1")
        if end is not None and end <= 0:
            raise ValueError("end_page deve ser >= 1")
        if start is not None and end is not None and end < start:
            raise ValueError("end_page não pode ser menor que start_page")

        return start, end
