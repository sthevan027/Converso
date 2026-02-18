from __future__ import annotations

from pathlib import Path
from typing import Optional

from pdf2docx import Converter  # type: ignore

from .base import BaseConverter, ConversionOptions


class DocxConverter(BaseConverter):
    """Conversor de PDF para DOCX baseado em pdf2docx."""

    def __init__(self, options: Optional[ConversionOptions] = None) -> None:
        super().__init__(options)

    def convert(self, pdf_path: str, output_path: str) -> None:
        pdf_file = Path(pdf_path)
        if not pdf_file.is_file():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_file}")

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        start, end = self._resolve_page_range()

        if self.options.verbose:
            print(f"[DOCX] Convertendo '{pdf_file}' -> '{output_file}' (páginas {start or 1} até {end or 'fim'})")

        cv = Converter(str(pdf_file))
        try:
            # pdf2docx usa index de página baseado em 0.
            start_idx = (start - 1) if start is not None else 0
            end_idx = (end - 1) if end is not None else None
            cv.convert(str(output_file), start=start_idx, end=end_idx)
        finally:
            cv.close()

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

