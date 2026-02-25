from __future__ import annotations

import io
from dataclasses import dataclass, field

import fitz  # PyMuPDF
from PIL import Image


@dataclass
class OCRResult:
    """Resultado do OCR para uma página."""

    text_lines: list[OCRLine] = field(default_factory=list)
    full_text: str = ""
    is_scanned: bool = False


@dataclass
class OCRLine:
    """Linha de texto detectada por OCR."""

    text: str
    bbox: tuple[float, float, float, float]  # x0, y0, x1, y1
    confidence: float = 0.0


_ocr_engine = None


def _get_ocr():
    global _ocr_engine
    if _ocr_engine is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_engine = RapidOCR()
    return _ocr_engine


def is_scanned_page(page: fitz.Page, min_text_len: int = 20) -> bool:
    """Verifica se uma página é escaneada (imagem sem texto nativo)."""
    native_text = page.get_text().strip()
    if len(native_text) >= min_text_len:
        return False

    images = page.get_images(full=True)
    if not images:
        return False

    blocks = page.get_text("dict")["blocks"]
    img_blocks = [b for b in blocks if b["type"] == 1]
    return len(img_blocks) > 0


def ocr_page(page: fitz.Page, dpi: int = 300) -> OCRResult:
    """Executa OCR em uma página do PDF e retorna o resultado."""
    result = OCRResult(is_scanned=is_scanned_page(page))

    if not result.is_scanned:
        return result

    pix = page.get_pixmap(dpi=dpi)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))

    ocr = _get_ocr()
    ocr_data, _ = ocr(img)

    if not ocr_data:
        return result

    scale_x = page.rect.width / pix.width
    scale_y = page.rect.height / pix.height

    for item in ocr_data:
        bbox_points, text, confidence = item
        px0 = min(p[0] for p in bbox_points)
        py0 = min(p[1] for p in bbox_points)
        px1 = max(p[0] for p in bbox_points)
        py1 = max(p[1] for p in bbox_points)

        x0 = px0 * scale_x
        y0 = py0 * scale_y
        x1 = px1 * scale_x
        y1 = py1 * scale_y

        result.text_lines.append(OCRLine(
            text=text,
            bbox=(x0, y0, x1, y1),
            confidence=confidence,
        ))

    lines_sorted = sorted(result.text_lines, key=lambda l: (l.bbox[1], l.bbox[0]))
    result.full_text = "\n".join(l.text for l in lines_sorted)

    return result
