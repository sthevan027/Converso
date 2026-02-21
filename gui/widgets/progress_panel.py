"""
Painel de progresso, log e feedback da conversão.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import subprocess
import sys
import os

import customtkinter as ctk


class ProgressPanel(ctk.CTkFrame):
    """
    Painel completo de feedback da conversão.
    
    Inclui barra de progresso, log de mensagens em tempo real,
    e botões de ação pós-conversão.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, fg_color=("gray92", "gray17"), corner_radius=10, **kwargs)

        self._visible = False
        self._output_path: Optional[Path] = None
        self._create_widgets()
        self._setup_layout()
        self.set_visible(False)

    def _create_widgets(self) -> None:
        """Cria os widgets do painel."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.status_icon = ctk.CTkLabel(
            self.header_frame,
            text="⏳",
            font=ctk.CTkFont(size=20),
        )

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="Preparando...",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        )

        self.percentage_label = ctk.CTkLabel(
            self.header_frame,
            text="0%",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("dodgerblue", "dodgerblue"),
        )

        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=6,
            corner_radius=3,
            progress_color=("dodgerblue", "dodgerblue"),
        )
        self.progress_bar.set(0)

        self.log_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="📋 Log",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
            anchor="w",
        )

        self.log_textbox = ctk.CTkTextbox(
            self.log_frame,
            height=100,
            font=ctk.CTkFont(size=11, family="Consolas"),
            fg_color=("gray88", "gray20"),
            text_color=("gray30", "gray70"),
            corner_radius=6,
            state="disabled",
        )

        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.result_icon = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=32),
        )

        self.result_label = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=14),
        )

        self.result_details = ctk.CTkLabel(
            self.result_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.open_file_button = ctk.CTkButton(
            self.buttons_frame,
            text="📄 Abrir Arquivo",
            font=ctk.CTkFont(size=13),
            height=35,
            command=self._open_file,
        )

        self.open_folder_button = ctk.CTkButton(
            self.buttons_frame,
            text="📂 Abrir Pasta",
            font=ctk.CTkFont(size=13),
            height=35,
            fg_color="transparent",
            border_width=1,
            command=self._open_folder,
        )

        self.close_button = ctk.CTkButton(
            self.buttons_frame,
            text="✕",
            width=35,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            text_color=("gray40", "gray60"),
            command=self._close_panel,
        )

    def _setup_layout(self) -> None:
        """Configura o layout do painel."""
        self.header_frame.pack(fill="x", padx=15, pady=(15, 10))
        self.status_icon.pack(side="left", padx=(0, 10))
        self.status_label.pack(side="left", fill="x", expand=True)
        self.percentage_label.pack(side="right")

        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))

        self.log_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.log_label.pack(anchor="w", pady=(0, 5))
        self.log_textbox.pack(fill="x")

        self.result_frame.pack(fill="x", padx=15, pady=(5, 10))
        self.result_icon.pack(anchor="center")
        self.result_label.pack(anchor="center", pady=(5, 0))
        self.result_details.pack(anchor="center")

        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.close_button.pack(side="right")

        self.result_frame.pack_forget()
        self.buttons_frame.pack_forget()

    def set_progress(self, value: int) -> None:
        """Define o valor do progresso (0-100)."""
        normalized = max(0, min(100, value)) / 100
        self.progress_bar.set(normalized)
        self.percentage_label.configure(text=f"{value}%")

    def set_status(self, message: str) -> None:
        """Define a mensagem de status principal."""
        self.status_label.configure(text=message)

    def add_log(self, message: str) -> None:
        """Adiciona uma mensagem ao log."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def clear_log(self) -> None:
        """Limpa o log de mensagens."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", "end")
        self.log_textbox.configure(state="disabled")

    def set_visible(self, visible: bool) -> None:
        """Mostra ou esconde o painel."""
        self._visible = visible
        if visible:
            self.pack(fill="x", pady=(0, 15))
        else:
            self.pack_forget()

    def reset(self) -> None:
        """Reseta o painel para o estado inicial de conversão."""
        self.set_progress(0)
        self.set_status("Preparando...")
        self.status_icon.configure(text="⏳")
        self.percentage_label.configure(text_color=("dodgerblue", "dodgerblue"))
        self.progress_bar.configure(progress_color=("dodgerblue", "dodgerblue"))
        self.clear_log()
        self._output_path = None

        self.log_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.result_frame.pack_forget()
        self.buttons_frame.pack_forget()

    def show_success(
        self,
        message: str = "Conversão concluída!",
        details: str = "",
        output_path: Optional[Path] = None,
    ) -> None:
        """Exibe estado de sucesso com opções."""
        self._output_path = output_path

        self.set_progress(100)
        self.status_icon.configure(text="✅")
        self.status_label.configure(text=message)
        self.percentage_label.configure(text_color=("green", "lightgreen"))
        self.progress_bar.configure(progress_color=("green", "lightgreen"))

        self.log_frame.pack_forget()

        self.result_frame.pack(fill="x", padx=15, pady=(5, 10))
        self.result_icon.configure(text="🎉")
        self.result_label.configure(
            text="Arquivo convertido com sucesso!",
            text_color=("green", "lightgreen"),
        )
        self.result_details.configure(text=details)

        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        if output_path:
            self.open_file_button.pack(side="left", padx=(0, 10))
            self.open_folder_button.pack(side="left")
        self.close_button.pack(side="right")

    def show_error(self, message: str = "Erro na conversão", details: str = "") -> None:
        """Exibe estado de erro."""
        self.status_icon.configure(text="❌")
        self.status_label.configure(text=message)
        self.percentage_label.configure(text_color=("red", "salmon"))
        self.progress_bar.configure(progress_color=("red", "salmon"))

        self.result_frame.pack(fill="x", padx=15, pady=(5, 10))
        self.result_icon.configure(text="😞")
        self.result_label.configure(
            text="Ocorreu um erro durante a conversão",
            text_color=("red", "salmon"),
        )
        self.result_details.configure(text=details)

        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.open_file_button.pack_forget()
        self.open_folder_button.pack_forget()
        self.close_button.pack(side="right")

    def _open_file(self) -> None:
        """Abre o arquivo convertido."""
        if self._output_path and self._output_path.exists():
            if sys.platform == "win32":
                os.startfile(self._output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(self._output_path)])
            else:
                subprocess.run(["xdg-open", str(self._output_path)])

    def _open_folder(self) -> None:
        """Abre a pasta contendo o arquivo."""
        if self._output_path and self._output_path.exists():
            folder = self._output_path.parent
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(folder)])
            else:
                subprocess.run(["xdg-open", str(folder)])

    def _close_panel(self) -> None:
        """Fecha/esconde o painel."""
        self.set_visible(False)
