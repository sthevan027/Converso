"""
Janela principal do Converso.

Este módulo contém a implementação da interface principal,
incluindo área de seleção de arquivo, opções de configuração
e controles de conversão.
"""

from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog
from typing import Optional

import customtkinter as ctk  # pyright: ignore[reportMissingImports]

from gui.widgets.drop_zone import DropZone
from gui.widgets.file_info import FileInfo
from gui.widgets.header import Header
from gui.widgets.options_panel import OptionsPanel
from gui.widgets.progress_panel import ProgressPanel


class MainWindow(ctk.CTkScrollableFrame):
    """Frame principal com scroll contendo toda a interface do conversor."""

    SUPPORTED_EXTENSIONS = [
        ("Todos os suportados", "*.pdf *.docx *.txt *.md"),
        ("Arquivos PDF", "*.pdf"),
        ("Documentos Word", "*.docx"),
        ("Arquivos de Texto", "*.txt"),
        ("Arquivos Markdown", "*.md"),
    ]

    OUTPUT_FORMATS = {
        ".pdf": ["DOCX", "HTML", "MD"],
        ".docx": ["PDF"],
        ".txt": ["PDF"],
        ".md": ["PDF"],
    }

    FILE_TYPE_NAMES = {
        ".pdf": "Documento PDF",
        ".docx": "Documento Word",
        ".txt": "Arquivo de Texto",
        ".md": "Arquivo Markdown",
    }

    IMPLEMENTED_FORMATS = ["docx", "pdf"]

    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(
            master,
            fg_color="transparent",
            scrollbar_button_color=("gray70", "gray30"),
            scrollbar_button_hover_color=("gray60", "gray40"),
        )

        self.selected_file: Optional[Path] = None
        self.is_converting = False

        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self) -> None:
        """Cria todos os widgets da interface."""
        self.header = Header(
            self,
            title="Converso",
            subtitle="Conversor de Documentos PDF, DOCX, TXT e MD",
        )

        self.separator = ctk.CTkFrame(self, height=2, fg_color=("gray80", "gray25"))

        self.drop_zone = DropZone(
            self,
            on_file_dropped=self._on_file_selected,
            on_click=self._open_file_dialog,
        )

        self.file_info = FileInfo(
            self,
            on_clear=self._clear_selection,
        )

        self.format_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.format_label = ctk.CTkLabel(
            self.format_frame,
            text="Converter para:",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.format_dropdown = ctk.CTkComboBox(
            self.format_frame,
            values=["DOCX"],
            state="disabled",
            width=150,
            command=self._on_format_changed,
        )
        self.format_dropdown.set("DOCX")

        self.format_status_label = ctk.CTkLabel(
            self.format_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("orange", "orange"),
        )

        self.options_panel = OptionsPanel(self)

        self.progress_panel = ProgressPanel(self)

        self.convert_button = ctk.CTkButton(
            self,
            text="Converter",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            state="disabled",
            command=self._start_conversion,
        )

    def _setup_layout(self) -> None:
        """Configura o layout dos widgets."""
        self.header.pack(fill="x", pady=(0, 15))

        self.separator.pack(fill="x", pady=(0, 15))

        self.drop_zone.pack(fill="x", pady=(0, 15))

        self.format_frame.pack(fill="x", pady=(0, 10))
        self.format_label.pack(side="left", pady=8)
        self.format_dropdown.pack(side="left", padx=15, pady=8)
        self.format_status_label.pack(side="left", pady=8)

        self.options_panel.pack(fill="x", pady=(0, 15))

        self.progress_panel.pack(fill="x", pady=(0, 15))

        self.convert_button.pack(fill="x", pady=(10, 0))

    def _on_file_selected(self, file_path: str | Path) -> None:
        """Callback quando um arquivo é selecionado ou arrastado."""
        path = Path(file_path) if isinstance(file_path, str) else file_path

        if not path.exists():
            self._show_error(f"Arquivo não encontrado: {path}")
            return

        ext = path.suffix.lower()
        if ext not in self.OUTPUT_FORMATS:
            self._show_error(f"Formato não suportado: {ext}")
            return

        self.selected_file = path
        self._update_ui_for_file(path)

    def _update_ui_for_file(self, path: Path) -> None:
        """Atualiza a interface após seleção de arquivo."""
        ext = path.suffix.lower()
        file_type = self.FILE_TYPE_NAMES.get(ext, "Arquivo")
        self.file_info.set_file(path, file_type)

        formats = self.OUTPUT_FORMATS.get(ext, [])
        self.format_dropdown.configure(values=formats, state="readonly")
        if formats:
            self.format_dropdown.set(formats[0])
            self._on_format_changed(formats[0])

        self.options_panel.set_input_file(path.name)
        self.drop_zone.set_file_selected(True, path.name)

    def _on_format_changed(self, selected_format: str) -> None:
        """Callback quando o formato de saída é alterado."""
        format_lower = selected_format.lower()
        is_implemented = format_lower in self.IMPLEMENTED_FORMATS

        self.options_panel.set_output_extension(format_lower)

        if is_implemented:
            self.format_status_label.configure(text="")
            self.convert_button.configure(state="normal")
        else:
            self.format_status_label.configure(text="⚠️ Em breve")
            self.convert_button.configure(state="disabled")

    def _clear_selection(self) -> None:
        """Limpa a seleção de arquivo atual."""
        self.selected_file = None
        self.file_info.clear()
        self.drop_zone.reset()
        self.format_dropdown.configure(state="disabled")
        self.format_dropdown.set("DOCX")
        self.format_status_label.configure(text="")
        self.convert_button.configure(state="disabled")
        self.progress_panel.reset()
        self.progress_panel.set_visible(False)

    def _open_file_dialog(self) -> None:
        """Abre o diálogo de seleção de arquivo."""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo para conversão",
            filetypes=self.SUPPORTED_EXTENSIONS,
        )
        if file_path:
            self._on_file_selected(file_path)

    def _start_conversion(self) -> None:
        """Inicia o processo de conversão."""
        if not self.selected_file or self.is_converting:
            return

        self.is_converting = True
        self._update_ui_converting(True)

        options = self.options_panel.get_options()
        target_format = self.format_dropdown.get().lower()

        thread = threading.Thread(
            target=self._run_conversion,
            args=(self.selected_file, target_format, options),
            daemon=True,
        )
        thread.start()

    def _run_conversion(
        self, input_file: Path, target_format: str, options: dict
    ) -> None:
        """Executa a conversão em uma thread separada."""
        try:
            from conversores.base import (
                ConversionOptions,
                HeaderFooterMode,
                TranscriptionQuality,
            )
            from conversores.docx_converter import DocxConverter
            from conversores.pdf_converter import PdfConverter
            from utils.file_utils import build_output_path

            self.after(0, lambda: self.progress_panel.set_status("Preparando conversão..."))
            self.after(0, lambda: self.progress_panel.set_progress(5))
            self.after(0, lambda: self.progress_panel.add_log(f"📄 Arquivo: {input_file.name}"))
            self.after(0, lambda: self.progress_panel.add_log(f"🎯 Formato de saída: {target_format.upper()}"))

            header_mode_map = {
                "Manter": HeaderFooterMode.KEEP,
                "Remover": HeaderFooterMode.REMOVE,
                "Converter": HeaderFooterMode.CONVERT_TO_HEADER,
            }
            quality_map = {
                "Rápido": TranscriptionQuality.FAST,
                "Equilibrado": TranscriptionQuality.BALANCED,
                "Alta Qualidade": TranscriptionQuality.HIGH,
            }

            self.after(0, lambda: self.progress_panel.set_progress(10))
            self.after(0, lambda: self.progress_panel.add_log("⚙️ Configurando opções..."))

            conversion_options = ConversionOptions(
                start_page=options.get("start_page"),
                end_page=options.get("end_page"),
                verbose=True,
                header_mode=header_mode_map.get(
                    options.get("header_mode", "Converter"),
                    HeaderFooterMode.CONVERT_TO_HEADER,
                ),
                footer_mode=header_mode_map.get(
                    options.get("footer_mode", "Converter"),
                    HeaderFooterMode.CONVERT_TO_HEADER,
                ),
                transcription_quality=quality_map.get(
                    options.get("quality", "Equilibrado"),
                    TranscriptionQuality.BALANCED,
                ),
                preserve_formatting=options.get("preserve_formatting", True),
                preserve_layout=options.get("preserve_layout", True),
                merge_paragraphs=options.get("merge_paragraphs", True),
                remove_hyphenation=options.get("remove_hyphenation", True),
                extract_images=options.get("extract_images", True),
                image_quality=options.get("image_quality", 95),
                max_image_width=options.get("max_image_width", 800),
            )

            converters = {
                "docx": DocxConverter,
                "pdf": PdfConverter,
            }

            converter_cls = converters.get(target_format)
            if not converter_cls:
                raise ValueError(f"Formato de saída não suportado: {target_format}")

            self.after(0, lambda: self.progress_panel.set_status("Processando documento..."))
            self.after(0, lambda: self.progress_panel.set_progress(20))
            self.after(0, lambda: self.progress_panel.add_log("📖 Lendo documento de entrada..."))

            output_dir = options.get("output_dir")
            output_filename = options.get("output_filename")

            if output_filename:
                base_dir = Path(output_dir) if output_dir else input_file.parent
                output_path = base_dir / f"{output_filename}.{target_format}"
            else:
                output_path = build_output_path(str(input_file), output_dir, target_format)

            self.after(0, lambda: self.progress_panel.set_status("Convertendo..."))
            self.after(0, lambda: self.progress_panel.set_progress(40))
            self.after(0, lambda: self.progress_panel.add_log("🔄 Convertendo conteúdo..."))

            converter = converter_cls(options=conversion_options)
            result = converter.convert(str(input_file), str(output_path))

            self.after(0, lambda: self.progress_panel.set_progress(90))
            self.after(0, lambda: self.progress_panel.add_log("💾 Salvando arquivo..."))

            pages = result.pages_converted
            images = result.images_extracted or 0
            details = f"{pages} página(s) convertida(s)"
            if images > 0:
                details += f" • {images} imagem(ns) extraída(s)"

            self.after(0, lambda: self.progress_panel.add_log(f"✅ Concluído: {output_path.name}"))
            self.after(
                0,
                lambda: self.progress_panel.show_success(
                    message="Conversão concluída!",
                    details=details,
                    output_path=Path(output_path),
                ),
            )
            self.after(0, lambda: self._conversion_finished(True, str(output_path)))

        except Exception as exc:
            error_msg = str(exc)
            self.after(0, lambda: self.progress_panel.add_log(f"❌ Erro: {error_msg}"))
            self.after(
                0,
                lambda: self.progress_panel.show_error(
                    message="Erro na conversão",
                    details=error_msg[:100] + "..." if len(error_msg) > 100 else error_msg,
                ),
            )
            self.after(0, lambda: self._conversion_finished(False))

    def _conversion_finished(self, success: bool, output_path: str = "") -> None:
        """Callback quando a conversão termina."""
        self.is_converting = False
        self._update_ui_converting(False)

    def _update_ui_converting(self, converting: bool) -> None:
        """Atualiza a interface durante a conversão."""
        if converting:
            self.convert_button.configure(state="disabled", text="Convertendo...")
            self.format_dropdown.configure(state="disabled")
            self.drop_zone.set_enabled(False)
            self.progress_panel.reset()
            self.progress_panel.set_visible(True)
        else:
            self.convert_button.configure(text="Converter")
            self.format_dropdown.configure(state="readonly")
            self.drop_zone.set_enabled(True)
            self._on_format_changed(self.format_dropdown.get())

    def _show_error(self, message: str) -> None:
        """Exibe uma mensagem de erro."""
        self.progress_panel.set_status(f"❌ {message}")
        self.progress_panel.set_visible(True)
