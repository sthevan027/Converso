from __future__ import annotations

from pathlib import Path
from typing import Optional


def build_output_path(
    input_pdf: str,
    output: Optional[str],
    target_ext: str,
) -> Path:
    """
    Calcula o caminho de saída.

    - Se `output` for um caminho de arquivo, usa esse caminho (ajustando a extensão).
    - Se `output` for um diretório, cria o mesmo nome do PDF com a nova extensão dentro dele.
    - Se `output` for None, usa o mesmo diretório do PDF com a nova extensão.
    """
    input_path = Path(input_pdf)
    if not input_path.is_file():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {input_path}")

    if not target_ext.startswith("."):
        target_ext = "." + target_ext

    if output:
        out_path = Path(output)
        if out_path.is_dir():
            return out_path / (input_path.stem + target_ext)
        # Trata como arquivo
        if out_path.suffix.lower() != target_ext.lower():
            out_path = out_path.with_suffix(target_ext)
        return out_path

    # Mesmo diretório do PDF
    return input_path.with_suffix(target_ext)

