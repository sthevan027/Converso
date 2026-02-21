"""
Widget de cabeçalho da aplicação.
"""

from __future__ import annotations

import customtkinter as ctk  # pyright: ignore[reportMissingImports]


class Header(ctk.CTkFrame):
    """
    Cabeçalho da aplicação com título e subtítulo.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        title: str = "Converso",
        subtitle: str = "Conversor de Documentos",
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)

        self._create_widgets(title, subtitle)

    def _create_widgets(self, title: str, subtitle: str) -> None:
        """Cria os widgets do cabeçalho."""
        self.icon_label = ctk.CTkLabel(
            self,
            text="📄",
            font=ctk.CTkFont(size=36),
        )
        self.icon_label.pack(side="left", padx=(0, 15))

        self.text_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.text_frame.pack(side="left", fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.text_frame,
            text=title,
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w",
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            self.text_frame,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60"),
            anchor="w",
        )
        self.subtitle_label.pack(anchor="w")
