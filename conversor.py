from __future__ import annotations

import argparse
import sys
from typing import Dict, Type

from conversores.base import BaseConverter, ConversionOptions
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
    return parser.parse_args(argv)


def get_converter_class(target: str) -> Type[BaseConverter]:
    try:
        return CONVERTERS[target]
    except KeyError:
        raise ValueError(f"Formato de saída não suportado ainda: {target}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    options = ConversionOptions(
        start_page=args.start_page,
        end_page=args.end_page,
        verbose=args.verbose,
    )

    try:
        converter_cls = get_converter_class(args.target)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output_path = build_output_path(args.input_pdf, args.output, args.target)

    converter = converter_cls(options=options)
    try:
        converter.convert(args.input_pdf, str(output_path))
    except Exception as exc:  # noqa: BLE001
        if args.verbose:
            raise
        print(f"Erro ao converter arquivo: {exc}", file=sys.stderr)
        return 1

    if args.verbose:
        print(f"Arquivo gerado em: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

