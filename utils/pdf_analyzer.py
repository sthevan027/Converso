from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

import fitz  # PyMuPDF


@dataclass
class TextBlock:
    """Representa um bloco de texto extraído do PDF."""

    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    font_name: str = ""
    font_size: float = 0.0
    is_bold: bool = False
    is_italic: bool = False
    block_type: str = "body"  # header, footer, body, title


@dataclass
class PageAnalysis:
    """Análise completa de uma página do PDF."""

    page_num: int
    width: float
    height: float
    header_blocks: list[TextBlock] = field(default_factory=list)
    footer_blocks: list[TextBlock] = field(default_factory=list)
    body_blocks: list[TextBlock] = field(default_factory=list)
    header_text: str = ""
    footer_text: str = ""
    body_text: str = ""


@dataclass
class DocumentAnalysis:
    """Análise completa do documento PDF."""

    pages: list[PageAnalysis] = field(default_factory=list)
    common_header: str = ""
    common_footer: str = ""
    detected_page_numbers: bool = False


class PDFAnalyzer:
    """Analisador avançado de PDF para detecção de estrutura."""

    def __init__(
        self,
        header_margin_ratio: float = 0.10,
        footer_margin_ratio: float = 0.10,
    ):
        self.header_margin_ratio = header_margin_ratio
        self.footer_margin_ratio = footer_margin_ratio

    def analyze_document(
        self,
        pdf_path: str,
        start_page: int = 0,
        end_page: Optional[int] = None,
    ) -> DocumentAnalysis:
        """Analisa o documento PDF completo."""
        doc = fitz.open(pdf_path)
        try:
            analysis = DocumentAnalysis()
            end = end_page if end_page is not None else len(doc)

            for page_num in range(start_page, min(end, len(doc))):
                page = doc[page_num]
                page_analysis = self._analyze_page(page, page_num)
                analysis.pages.append(page_analysis)

            self._detect_common_headers_footers(analysis)
            return analysis
        finally:
            doc.close()

    def _analyze_page(self, page: fitz.Page, page_num: int) -> PageAnalysis:
        """Analisa uma página individual do PDF."""
        rect = page.rect
        width, height = rect.width, rect.height

        header_threshold = height * self.header_margin_ratio
        footer_threshold = height * (1 - self.footer_margin_ratio)

        page_analysis = PageAnalysis(
            page_num=page_num,
            width=width,
            height=height,
        )

        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        for block in blocks:
            if block["type"] != 0:  # Não é texto
                continue

            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue

                    bbox = span.get("bbox", (0, 0, 0, 0))
                    font = span.get("font", "")
                    size = span.get("size", 0)
                    flags = span.get("flags", 0)

                    text_block = TextBlock(
                        text=text,
                        x0=bbox[0],
                        y0=bbox[1],
                        x1=bbox[2],
                        y1=bbox[3],
                        font_name=font,
                        font_size=size,
                        is_bold=bool(flags & 2**4),
                        is_italic=bool(flags & 2**1),
                    )

                    y_center = (bbox[1] + bbox[3]) / 2

                    if y_center < header_threshold:
                        text_block.block_type = "header"
                        page_analysis.header_blocks.append(text_block)
                    elif y_center > footer_threshold:
                        text_block.block_type = "footer"
                        page_analysis.footer_blocks.append(text_block)
                    else:
                        text_block.block_type = "body"
                        page_analysis.body_blocks.append(text_block)

        page_analysis.header_text = self._blocks_to_text(page_analysis.header_blocks)
        page_analysis.footer_text = self._blocks_to_text(page_analysis.footer_blocks)
        page_analysis.body_text = self._blocks_to_text(page_analysis.body_blocks)

        return page_analysis

    def _blocks_to_text(self, blocks: list[TextBlock]) -> str:
        """Converte blocos de texto em string formatada."""
        if not blocks:
            return ""

        sorted_blocks = sorted(blocks, key=lambda b: (b.y0, b.x0))
        lines: list[str] = []
        current_line: list[str] = []
        current_y: float = -1

        for block in sorted_blocks:
            if current_y < 0:
                current_y = block.y0
                current_line.append(block.text)
            elif abs(block.y0 - current_y) < block.font_size * 0.5:
                current_line.append(block.text)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [block.text]
                current_y = block.y0

        if current_line:
            lines.append(" ".join(current_line))

        return "\n".join(lines)

    def _detect_common_headers_footers(self, analysis: DocumentAnalysis) -> None:
        """Detecta cabeçalhos e rodapés comuns entre páginas."""
        if len(analysis.pages) < 2:
            return

        headers = [p.header_text for p in analysis.pages if p.header_text]
        footers = [p.footer_text for p in analysis.pages if p.footer_text]

        if headers:
            analysis.common_header = self._find_common_pattern(headers)

        if footers:
            analysis.common_footer = self._find_common_pattern(footers)
            analysis.detected_page_numbers = self._has_page_numbers(footers)

    def _find_common_pattern(self, texts: list[str]) -> str:
        """Encontra padrão comum entre textos (ignorando números de página)."""
        if not texts:
            return ""

        normalized = []
        for text in texts:
            clean = re.sub(r"\b\d+\b", "{NUM}", text)
            clean = re.sub(r"\s+", " ", clean).strip()
            normalized.append(clean)

        from collections import Counter

        counter = Counter(normalized)
        most_common = counter.most_common(1)

        if most_common and most_common[0][1] >= len(texts) * 0.5:
            return most_common[0][0]
        return ""

    def _has_page_numbers(self, footers: list[str]) -> bool:
        """Verifica se os rodapés contêm números de página sequenciais."""
        numbers = []
        for footer in footers:
            matches = re.findall(r"\b(\d+)\b", footer)
            if matches:
                numbers.append(int(matches[-1]))

        if len(numbers) < 2:
            return False

        sequential = sum(1 for i in range(1, len(numbers)) if numbers[i] == numbers[i - 1] + 1)
        return sequential >= len(numbers) * 0.6


def extract_clean_text(
    pdf_path: str,
    remove_headers: bool = True,
    remove_footers: bool = True,
    start_page: int = 0,
    end_page: Optional[int] = None,
) -> str:
    """Extrai texto limpo do PDF, removendo cabeçalhos e rodapés repetitivos."""
    analyzer = PDFAnalyzer()
    analysis = analyzer.analyze_document(pdf_path, start_page, end_page)

    texts = []
    for page in analysis.pages:
        if remove_headers and analysis.common_header:
            page_text = page.body_text
        else:
            page_text = page.header_text + "\n" + page.body_text if page.header_text else page.body_text

        if not remove_footers or not analysis.common_footer:
            if page.footer_text:
                page_text += "\n" + page.footer_text

        texts.append(page_text.strip())

    return "\n\n---\n\n".join(texts)
