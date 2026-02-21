from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class HeaderFooterMode(Enum):
    """Modo de tratamento de cabeçalhos e rodapés."""

    KEEP = "keep"  # Manter como estão
    REMOVE = "remove"  # Remover completamente
    CONVERT_TO_HEADER = "convert"  # Converter para cabeçalho/rodapé do Word


class TranscriptionQuality(Enum):
    """Nível de qualidade da transcrição."""

    FAST = "fast"  # Rápido, menos preciso
    BALANCED = "balanced"  # Equilíbrio entre velocidade e qualidade
    HIGH = "high"  # Alta qualidade, mais lento


@dataclass
class ConversionOptions:
    """Opções comuns usadas pelos conversores."""

    start_page: Optional[int] = None  # 1-based
    end_page: Optional[int] = None  # 1-based, inclusive
    verbose: bool = False

    # Opções de cabeçalho e rodapé
    header_mode: HeaderFooterMode = HeaderFooterMode.CONVERT_TO_HEADER
    footer_mode: HeaderFooterMode = HeaderFooterMode.CONVERT_TO_HEADER
    header_margin_ratio: float = 0.10  # 10% superior da página
    footer_margin_ratio: float = 0.10  # 10% inferior da página

    # Opções de transcrição e otimização
    transcription_quality: TranscriptionQuality = TranscriptionQuality.BALANCED
    preserve_formatting: bool = True  # Preservar formatação (negrito, itálico)
    preserve_layout: bool = True  # Tentar preservar layout de colunas
    optimize_tables: bool = True  # Otimizar detecção de tabelas
    merge_paragraphs: bool = True  # Mesclar parágrafos fragmentados
    remove_hyphenation: bool = True  # Remover hifenização de fim de linha
    detect_lists: bool = True  # Detectar e formatar listas

    # Opções de imagem
    extract_images: bool = True
    image_quality: int = 95  # Qualidade JPEG (1-100)
    max_image_width: int = 800  # Largura máxima em pixels

    # Margens customizadas para detecção de cabeçalho/rodapé (em pontos)
    custom_header_height: Optional[float] = None
    custom_footer_height: Optional[float] = None


@dataclass
class ConversionResult:

    success: bool
    output_path: str
    pages_converted: int = 0
    headers_detected: int = 0
    footers_detected: int = 0
    tables_detected: int = 0
    images_extracted: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class BaseConverter(ABC):
    """Interface base para todos os conversores."""

    def __init__(self, options: Optional[ConversionOptions] = None) -> None:
        self.options = options or ConversionOptions()

    @abstractmethod
    def convert(self, pdf_path: str, output_path: str) -> ConversionResult:
        """Converte pdf_path para output_path."""
        raise NotImplementedError

    def _log(self, message: str) -> None:
        """Log de mensagem se verbose estiver ativo."""
        if self.options.verbose:
            print(message)

