from __future__ import annotations

import argparse
import sys
from typing import Dict, Type

from conversores.base import (
    BaseConverter,
    ConversionOptions,
    HeaderFooterMode,
    TranscriptionQuality,
)
from conversores.docx_converter import DocxConverter
from utils.file_utils import build_output_path


CONVERTERS: Dict[str, Type[BaseConverter]] = {
    "docx": DocxConverter,
    # "html": HtmlConverter,  # será registrado quando implementarmos
    # "md": MdConverter,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Conversor de PDF para múltiplos formatos (DOCX, HTML, Markdown).",
    )
    parser.add_argument("input_pdf", help="Caminho do arquivo PDF de entrada.")
    parser.add_argument(
        "--to",
        "-t",
        dest="target",
        choices=["docx", "html", "md"],
        default="docx",
        help="Formato de saída desejado (padrão: docx).",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        default=None,
        help="Caminho do arquivo ou diretório de saída. Se omitido, usa o mesmo diretório do PDF.",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=None,
        help="Página inicial (1-based) a ser convertida.",
    )
    parser.add_argument(
        "--end-page",
        type=int,
        default=None,
        help="Página final (1-based, inclusiva) a ser convertida.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Exibe informações detalhadas durante a conversão.",
    )

    # Opções de cabeçalho e rodapé
    parser.add_argument(
        "--header-mode",
        choices=["keep", "remove", "convert"],
        default="convert",
        help="Como tratar cabeçalhos: keep (manter), remove (remover), convert (converter para Word).",
    )
    parser.add_argument(
        "--footer-mode",
        choices=["keep", "remove", "convert"],
        default="convert",
        help="Como tratar rodapés: keep (manter), remove (remover), convert (converter para Word).",
    )
    parser.add_argument(
        "--header-margin",
        type=float,
        default=0.10,
        help="Proporção da página considerada como área de cabeçalho (padrão: 0.10 = 10%%).",
    )
    parser.add_argument(
        "--footer-margin",
        type=float,
        default=0.10,
        help="Proporção da página considerada como área de rodapé (padrão: 0.10 = 10%%).",
    )

    # Opções de qualidade de transcrição
    parser.add_argument(
        "--quality",
        "-q",
        choices=["fast", "balanced", "high"],
        default="balanced",
        help="Qualidade da transcrição: fast (rápido), balanced (equilibrado), high (alta qualidade).",
    )

    # Opções de formatação
    parser.add_argument(
        "--no-formatting",
        action="store_true",
        help="Desativa preservação de formatação (negrito, itálico).",
    )
    parser.add_argument(
        "--no-layout",
        action="store_true",
        help="Desativa preservação de layout de colunas.",
    )
    parser.add_argument(
        "--no-merge-paragraphs",
        action="store_true",
        help="Desativa mesclagem de parágrafos fragmentados.",
    )
    parser.add_argument(
        "--keep-hyphenation",
        action="store_true",
        help="Mantém hifenização de fim de linha.",
    )

    # Opções de imagem
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Não extrai imagens do PDF.",
    )
    parser.add_argument(
        "--image-quality",
        type=int,
        default=95,
        help="Qualidade das imagens JPEG (1-100, padrão: 95).",
    )
    parser.add_argument(
        "--max-image-width",
        type=int,
        default=800,
        help="Largura máxima das imagens em pixels (padrão: 800).",
    )

    return parser.parse_args(argv)


def get_converter_class(target: str) -> Type[BaseConverter]:
    try:
        return CONVERTERS[target]
    except KeyError:
        raise ValueError(f"Formato de saída não suportado ainda: {target}")


def _parse_header_footer_mode(mode: str) -> HeaderFooterMode:
    """Converte string para enum HeaderFooterMode."""
    mapping = {
        "keep": HeaderFooterMode.KEEP,
        "remove": HeaderFooterMode.REMOVE,
        "convert": HeaderFooterMode.CONVERT_TO_HEADER,
    }
    return mapping.get(mode, HeaderFooterMode.CONVERT_TO_HEADER)


def _parse_quality(quality: str) -> TranscriptionQuality:
    """Converte string para enum TranscriptionQuality."""
    mapping = {
        "fast": TranscriptionQuality.FAST,
        "balanced": TranscriptionQuality.BALANCED,
        "high": TranscriptionQuality.HIGH,
    }
    return mapping.get(quality, TranscriptionQuality.BALANCED)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    options = ConversionOptions(
        start_page=args.start_page,
        end_page=args.end_page,
        verbose=args.verbose,
        # Opções de cabeçalho e rodapé
        header_mode=_parse_header_footer_mode(args.header_mode),
        footer_mode=_parse_header_footer_mode(args.footer_mode),
        header_margin_ratio=args.header_margin,
        footer_margin_ratio=args.footer_margin,
        # Qualidade de transcrição
        transcription_quality=_parse_quality(args.quality),
        # Formatação
        preserve_formatting=not args.no_formatting,
        preserve_layout=not args.no_layout,
        merge_paragraphs=not args.no_merge_paragraphs,
        remove_hyphenation=not args.keep_hyphenation,
        # Imagens
        extract_images=not args.no_images,
        image_quality=args.image_quality,
        max_image_width=args.max_image_width,
    )

    try:
        converter_cls = get_converter_class(args.target)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output_path = build_output_path(args.input_pdf, args.output, args.target)

    converter = converter_cls(options=options)
    try:
        result = converter.convert(args.input_pdf, str(output_path))

        if args.verbose:
            print(f"\n=== Resultado da Conversão ===")
            print(f"Arquivo gerado: {result.output_path}")
            print(f"Páginas convertidas: {result.pages_converted}")
            print(f"Cabeçalhos detectados: {result.headers_detected}")
            print(f"Rodapés detectados: {result.footers_detected}")
            print(f"Imagens extraídas: {result.images_extracted}")
            if result.warnings:
                print(f"Avisos: {len(result.warnings)}")
                for w in result.warnings[:5]:
                    print(f"  - {w}")

    except Exception as exc:  # noqa: BLE001
        if args.verbose:
            raise
        print(f"Erro ao converter arquivo: {exc}", file=sys.stderr)
        return 1

    if not args.verbose:
        print(f"Arquivo gerado em: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

