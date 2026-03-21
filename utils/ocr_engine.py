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
_ocr_backend = None  # "rapidocr" | "pytesseract"


def _get_ocr():
    """Retorna o motor OCR disponível (RapidOCR ou pytesseract como fallback)."""
    global _ocr_engine, _ocr_backend
    if _ocr_engine is not None:
        return _ocr_engine, _ocr_backend

    try:
        from rapidocr_onnxruntime import RapidOCR
        _ocr_engine = RapidOCR()
        _ocr_backend = "rapidocr"
        return _ocr_engine, _ocr_backend
    except ImportError:
        pass

    try:
        import pytesseract
        _ocr_engine = pytesseract
        _ocr_backend = "pytesseract"
        return _ocr_engine, _ocr_backend
    except ImportError:
        raise ImportError(
            "Nenhum motor OCR instalado. Instale um deles:\n"
            "  pip install rapidocr-onnxruntime   # recomendado\n"
            "  pip install pytesseract            # requer Tesseract instalado no sistema"
        )


def _merge_words_into_lines(
    words: list[tuple[str, float, float, float, float, float]],
) -> list[tuple[str, float, float, float, float, float]]:
    """Agrupa palavras em linhas por proximidade vertical (compatível com pytesseract)."""
    if not words:
        return []

    sorted_words = sorted(words, key=lambda w: (w[2], w[1]))  # y0, x0
    lines: list[tuple[str, float, float, float, float, float]] = []
    line_words: list[tuple[str, float, float, float, float, float]] = [sorted_words[0]]
    line_y_center = (sorted_words[0][2] + sorted_words[0][4]) / 2
    line_height = sorted_words[0][4] - sorted_words[0][2]

    for w in sorted_words[1:]:
        text, x0, y0, x1, y1, conf = w
        w_y_center = (y0 + y1) / 2
        if abs(w_y_center - line_y_center) <= line_height * 0.6:
            line_words.append(w)
        else:
            merged_text = " ".join(t[0] for t in line_words)
            min_x = min(t[1] for t in line_words)
            min_y = min(t[2] for t in line_words)
            max_x = max(t[3] for t in line_words)
            max_y = max(t[4] for t in line_words)
            avg_conf = sum(t[5] for t in line_words) / len(line_words)
            lines.append((merged_text, min_x, min_y, max_x, max_y, avg_conf))
            line_words = [w]
            line_y_center = (y0 + y1) / 2
            line_height = y1 - y0

    if line_words:
        merged_text = " ".join(t[0] for t in line_words)
        min_x = min(t[1] for t in line_words)
        min_y = min(t[2] for t in line_words)
        max_x = max(t[3] for t in line_words)
        max_y = max(t[4] for t in line_words)
        avg_conf = sum(t[5] for t in line_words) / len(line_words)
        lines.append((merged_text, min_x, min_y, max_x, max_y, avg_conf))

    return lines


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

    ocr, backend = _get_ocr()
    scale_x = page.rect.width / pix.width
    scale_y = page.rect.height / pix.height

    if backend == "rapidocr":
        ocr_data, _ = ocr(img)
        if not ocr_data:
            return result

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

    else:  # pytesseract fallback
        import pytesseract
        try:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang="por+eng")
        except Exception:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        n_boxes = len(data["text"])
        words: list[tuple[str, float, float, float, float, float]] = []
        for i in range(n_boxes):
            text = (data["text"][i] or "").strip()
            if not text:
                continue
            x0 = data["left"][i] * scale_x
            y0 = data["top"][i] * scale_y
            w = data["width"][i] * scale_x
            h = data["height"][i] * scale_y
            conf = float(data["conf"][i]) / 100.0 if data["conf"][i] >= 0 else 0.0
            words.append((text, x0, y0, x0 + w, y0 + h, conf))

        for text, x0, y0, x1, y1, conf in _merge_words_into_lines(words):
            result.text_lines.append(OCRLine(text=text, bbox=(x0, y0, x1, y1), confidence=conf))

    lines_sorted = sorted(result.text_lines, key=lambda l: (l.bbox[1], l.bbox[0]))
    result.full_text = "\n".join(l.text for l in lines_sorted)

    return result
