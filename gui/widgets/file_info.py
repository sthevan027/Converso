"""
Widget de informações do arquivo selecionado.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk


class FileInfo(ctk.CTkFrame):
    """
    Painel que exibe informações detalhadas do arquivo selecionado.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_clear: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self.on_clear = on_clear
        self._create_widgets()
        self._setup_layout()
        self.set_visible(False)

    def _create_widgets(self) -> None:
        """Cria os widgets do painel."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.file_icon = ctk.CTkLabel(
            self.header_frame,
            text="📄",
            font=ctk.CTkFont(size=28),
        )

        self.info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")

        self.filename_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )

        self.path_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60"),
            anchor="w",
            wraplength=450,
        )

        self.details_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
            anchor="w",
        )

        self.clear_button = ctk.CTkButton(
            self.header_frame,
            text="✕",
            width=30,
            height=30,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            text_color=("gray40", "gray60"),
            command=self._on_clear_click,
        )

    def _setup_layout(self) -> None:
        """Configura o layout dos widgets."""
        self.header_frame.pack(fill="x", padx=10, pady=10)

        self.file_icon.pack(side="left", padx=(5, 15))

        self.info_frame.pack(side="left", fill="both", expand=True)
        self.filename_label.pack(anchor="w")
        self.path_label.pack(anchor="w", pady=(2, 0))
        self.details_label.pack(anchor="w", pady=(2, 0))

        self.clear_button.pack(side="right", padx=5)

    def set_file(self, path: Path, file_type: str = "") -> None:
        """Define o arquivo a ser exibido."""
        self.filename_label.configure(text=path.name)

        parent_path = str(path.parent)
        if len(parent_path) > 60:
            parent_path = "..." + parent_path[-57:]
        self.path_label.configure(text=f"📁 {parent_path}")

        size = path.stat().st_size
        size_str = self._format_size(size)
        details = f"{file_type} • {size_str}"
        self.details_label.configure(text=details)

        ext = path.suffix.lower()
        icons = {
            ".pdf": "📕",
            ".docx": "📘",
            ".txt": "📝",
            ".md": "📋",
        }
        self.file_icon.configure(text=icons.get(ext, "📄"))

        self.set_visible(True)

    def _format_size(self, size: int) -> str:
        """Formata o tamanho do arquivo."""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def _on_clear_click(self) -> None:
        """Callback do botão de limpar."""
        if self.on_clear:
            self.on_clear()

    def set_visible(self, visible: bool) -> None:
        """Mostra ou esconde o painel."""
        if visible:
            self.pack(fill="x", pady=(0, 10))
        else:
            self.pack_forget()

    def clear(self) -> None:
        """Limpa as informações do arquivo."""
        self.filename_label.configure(text="")
        self.path_label.configure(text="")
        self.details_label.configure(text="")
        self.set_visible(False)
