"""
Widget de área de arrastar e soltar arquivos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk


class DropZone(ctk.CTkFrame):
    """
    Área de arrastar e soltar para seleção de arquivos.
    
    Exibe uma área visual onde o usuário pode arrastar arquivos
    ou clicar para abrir o diálogo de seleção.
    """

    DEFAULT_TEXT = "📁 Clique para selecionar um arquivo"
    FILE_SELECTED_TEXT = "📄 {filename}\n(clique para alterar)"

    def __init__(
        self,
        master: ctk.CTkFrame,
        on_file_dropped: Optional[Callable[[str], None]] = None,
        on_click: Optional[Callable[[], None]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            height=150,
            corner_radius=15,
            border_width=2,
            border_color=("gray70", "gray30"),
            **kwargs,
        )

        self.on_file_dropped = on_file_dropped
        self.on_click = on_click
        self._enabled = True
        self._file_selected = False

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Cria os elementos visuais da drop zone."""
        self.pack_propagate(False)

        self.label = ctk.CTkLabel(
            self,
            text=self.DEFAULT_TEXT,
            font=ctk.CTkFont(size=15),
            text_color=("gray40", "gray60"),
            justify="center",
        )
        self.label.pack(expand=True)

    def _bind_events(self) -> None:
        """Configura os eventos de interação."""
        self.bind("<Button-1>", self._on_click)
        self.label.bind("<Button-1>", self._on_click)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.label.bind("<Enter>", self._on_enter)
        self.label.bind("<Leave>", self._on_leave)

    def _on_click(self, event=None) -> None:
        """Manipula o clique na área."""
        if self._enabled and self.on_click:
            self.on_click()

    def _on_enter(self, event=None) -> None:
        """Manipula a entrada do mouse na área."""
        if self._enabled:
            self.configure(border_color=("dodgerblue", "dodgerblue3"))
            self.configure(cursor="hand2")

    def _on_leave(self, event=None) -> None:
        """Manipula a saída do mouse da área."""
        color = ("green", "green") if self._file_selected else ("gray70", "gray30")
        self.configure(border_color=color)
        self.configure(cursor="")

    def set_file_selected(self, selected: bool, filename: str = "") -> None:
        """Define o estado de arquivo selecionado."""
        self._file_selected = selected
        if selected and filename:
            display_name = filename if len(filename) <= 40 else f"{filename[:37]}..."
            self.label.configure(
                text=self.FILE_SELECTED_TEXT.format(filename=display_name),
                text_color=("gray20", "gray80"),
            )
            self.configure(border_color=("green", "green"))
        else:
            self.label.configure(
                text=self.DEFAULT_TEXT,
                text_color=("gray40", "gray60"),
            )
            self.configure(border_color=("gray70", "gray30"))

    def set_enabled(self, enabled: bool) -> None:
        """Habilita ou desabilita a drop zone."""
        self._enabled = enabled
        if not enabled:
            self.configure(border_color=("gray80", "gray20"))
            self.label.configure(text_color=("gray70", "gray40"))
        else:
            self._on_leave()

    def reset(self) -> None:
        """Reseta a drop zone para o estado inicial."""
        self._file_selected = False
        self._enabled = True
        self.label.configure(
            text=self.DEFAULT_TEXT,
            text_color=("gray40", "gray60"),
        )
        self.configure(border_color=("gray70", "gray30"))
