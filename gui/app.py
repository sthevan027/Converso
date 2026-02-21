"""
Aplicação principal do Converso GUI.

Este módulo contém a classe principal que inicializa e gerencia
a aplicação gráfica do conversor de documentos.
"""

from __future__ import annotations

import sys
from pathlib import Path

import customtkinter as ctk   # pyright: ignore[reportMissingImports]

from gui.main_window import MainWindow


class ConversoApp(ctk.CTk):
    """Aplicação principal do Converso."""

    APP_NAME = "Converso - Conversor de Documentos"
    DEFAULT_WIDTH = 700
    DEFAULT_HEIGHT = 600
    MIN_WIDTH = 500
    MIN_HEIGHT = 450

    def __init__(self) -> None:
        super().__init__()

        self._setup_window()
        self._setup_theme()
        self._create_main_window()

    def _setup_window(self) -> None:
        """Configura as propriedades da janela principal."""
        self.title(self.APP_NAME)
        self.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        self._center_window()

        icon_path = Path(__file__).parent / "assets" / "icon.ico"
        if icon_path.exists():
            self.iconbitmap(str(icon_path))

    def _center_window(self) -> None:
        """Centraliza a janela na tela."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.DEFAULT_WIDTH) // 2
        y = (screen_height - self.DEFAULT_HEIGHT) // 2
        self.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}+{x}+{y}")

    def _setup_theme(self) -> None:
        """Configura o tema da aplicação."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def _create_main_window(self) -> None:
        """Cria o conteúdo da janela principal."""
        self.main_window = MainWindow(self)
        self.main_window.pack(fill="both", expand=True, padx=10, pady=10)


def run() -> int:
    """Inicia a aplicação GUI."""
    try:
        app = ConversoApp()
        app.mainloop()
        return 0
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
