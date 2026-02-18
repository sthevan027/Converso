from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConversionOptions:
    """Opções comuns usadas pelos conversores."""

    start_page: Optional[int] = None  # 1-based
    end_page: Optional[int] = None  # 1-based, inclusive
    verbose: bool = False


class BaseConverter(ABC):
    """Interface base para todos os conversores."""

    def __init__(self, options: Optional[ConversionOptions] = None) -> None:
        self.options = options or ConversionOptions()

    @abstractmethod
    def convert(self, pdf_path: str, output_path: str) -> None:
        """Converte pdf_path para output_path."""
        raise NotImplementedError

