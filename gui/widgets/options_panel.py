"""
Painel de opções avançadas de conversão.
"""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog
from typing import Optional  # pyright: ignore[reportMissingImports]

import customtkinter as ctk  # pyright: ignore[reportMissingImports]


class SectionFrame(ctk.CTkFrame):
    """Frame para agrupar opções em uma seção com título."""

    def __init__(
        self,
        master: ctk.CTkFrame,
        title: str,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color=("gray92", "gray17"), corner_radius=8, **kwargs)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60"),
        )
        self.title_label.pack(anchor="w", padx=12, pady=(8, 5))

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="x", padx=12, pady=(0, 10))


class OptionsPanel(ctk.CTkFrame):
    """
    Painel expansível com opções avançadas de conversão.
    
    Permite ao usuário configurar parâmetros como qualidade,
    tratamento de cabeçalhos/rodapés, páginas específicas, etc.
    """

    def __init__(self, master: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self._expanded = False
        self._output_dir: Optional[Path] = None
        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self) -> None:
        """Cria os widgets do painel."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.toggle_button = ctk.CTkButton(
            self.header_frame,
            text="⚙️ Opções Avançadas ▶",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            text_color=("gray30", "gray70"),
            anchor="w",
            command=self._toggle_expansion,
        )

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")

        self._create_output_section()
        self._create_quality_section()
        self._create_pages_section()
        self._create_header_footer_section()
        self._create_text_options_section()
        self._create_image_options_section()

    def _create_output_section(self) -> None:
        """Cria a seção de diretório e nome de saída."""
        self.output_section = SectionFrame(self.content_frame, "📁 Saída")

        self.filename_row = ctk.CTkFrame(self.output_section.content, fg_color="transparent")

        self.filename_input_frame = ctk.CTkFrame(
            self.filename_row,
            fg_color=("gray88", "gray20"),
            corner_radius=6,
        )

        self.filename_entry = ctk.CTkEntry(
            self.filename_input_frame,
            placeholder_text="mesmo nome do original",
            width=220,
            height=32,
            border_width=0,
            fg_color="transparent",
        )

        self.filename_ext_label = ctk.CTkLabel(
            self.filename_input_frame,
            text=".docx",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("dodgerblue", "dodgerblue"),
            width=50,
        )

        self.output_dir_row = ctk.CTkFrame(self.output_section.content, fg_color="transparent")

        self.output_dir_input_frame = ctk.CTkFrame(
            self.output_dir_row,
            fg_color=("gray88", "gray20"),
            corner_radius=6,
        )

        self.output_label = ctk.CTkLabel(
            self.output_dir_input_frame,
            text="📁 Mesmo diretório do arquivo",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
            anchor="w",
            height=32,
        )

        self.output_button = ctk.CTkButton(
            self.output_dir_row,
            text="Alterar",
            width=70,
            height=32,
            font=ctk.CTkFont(size=12),
            command=self._select_output_dir,
        )

        self.output_reset_button = ctk.CTkButton(
            self.output_dir_row,
            text="↺",
            width=32,
            height=32,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            text_color=("gray40", "gray60"),
            command=self._reset_output_dir,
        )

    def _create_quality_section(self) -> None:
        """Cria a seção de qualidade."""
        self.quality_section = SectionFrame(self.content_frame, "⚡ Qualidade")

        self.quality_var = ctk.StringVar(value="Equilibrado")
        self.quality_menu = ctk.CTkSegmentedButton(
            self.quality_section.content,
            values=["Rápido", "Equilibrado", "Alta Qualidade"],
            variable=self.quality_var,
        )

        self.quality_desc = ctk.CTkLabel(
            self.quality_section.content,
            text="Equilibrado: boa qualidade com velocidade razoável",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        )

        self.quality_var.trace_add("write", self._update_quality_description)

    def _create_pages_section(self) -> None:
        """Cria a seção de seleção de páginas."""
        self.pages_section = SectionFrame(self.content_frame, "📄 Páginas")

        self.pages_frame = ctk.CTkFrame(self.pages_section.content, fg_color="transparent")

        self.start_page_label = ctk.CTkLabel(
            self.pages_frame,
            text="De:",
            font=ctk.CTkFont(size=12),
        )
        self.start_page_entry = ctk.CTkEntry(
            self.pages_frame,
            width=70,
            placeholder_text="1",
        )

        self.end_page_label = ctk.CTkLabel(
            self.pages_frame,
            text="Até:",
            font=ctk.CTkFont(size=12),
        )
        self.end_page_entry = ctk.CTkEntry(
            self.pages_frame,
            width=70,
            placeholder_text="Última",
        )

        self.pages_hint = ctk.CTkLabel(
            self.pages_section.content,
            text="Deixe vazio para converter todas as páginas",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray50"),
        )

    def _create_header_footer_section(self) -> None:
        """Cria a seção de cabeçalho e rodapé."""
        self.hf_section = SectionFrame(self.content_frame, "📋 Cabeçalho e Rodapé")

        self.hf_frame = ctk.CTkFrame(self.hf_section.content, fg_color="transparent")

        self.header_label = ctk.CTkLabel(
            self.hf_frame,
            text="Cabeçalho:",
            font=ctk.CTkFont(size=12),
        )
        self.header_var = ctk.StringVar(value="Converter")
        self.header_menu = ctk.CTkComboBox(
            self.hf_frame,
            values=["Manter", "Remover", "Converter"],
            variable=self.header_var,
            width=110,
            state="readonly",
        )

        self.footer_label = ctk.CTkLabel(
            self.hf_frame,
            text="Rodapé:",
            font=ctk.CTkFont(size=12),
        )
        self.footer_var = ctk.StringVar(value="Converter")
        self.footer_menu = ctk.CTkComboBox(
            self.hf_frame,
            values=["Manter", "Remover", "Converter"],
            variable=self.footer_var,
            width=110,
            state="readonly",
        )

    def _create_text_options_section(self) -> None:
        """Cria a seção de opções de texto."""
        self.text_section = SectionFrame(self.content_frame, "📝 Texto")

        self.preserve_formatting_var = ctk.BooleanVar(value=True)
        self.preserve_formatting_cb = ctk.CTkCheckBox(
            self.text_section.content,
            text="Preservar formatação (negrito, itálico)",
            variable=self.preserve_formatting_var,
            font=ctk.CTkFont(size=12),
        )

        self.preserve_layout_var = ctk.BooleanVar(value=True)
        self.preserve_layout_cb = ctk.CTkCheckBox(
            self.text_section.content,
            text="Preservar layout de colunas",
            variable=self.preserve_layout_var,
            font=ctk.CTkFont(size=12),
        )

        self.merge_paragraphs_var = ctk.BooleanVar(value=True)
        self.merge_paragraphs_cb = ctk.CTkCheckBox(
            self.text_section.content,
            text="Mesclar parágrafos fragmentados",
            variable=self.merge_paragraphs_var,
            font=ctk.CTkFont(size=12),
        )

        self.remove_hyphenation_var = ctk.BooleanVar(value=True)
        self.remove_hyphenation_cb = ctk.CTkCheckBox(
            self.text_section.content,
            text="Remover hifenização de fim de linha",
            variable=self.remove_hyphenation_var,
            font=ctk.CTkFont(size=12),
        )

    def _create_image_options_section(self) -> None:
        """Cria a seção de opções de imagem."""
        self.image_section = SectionFrame(self.content_frame, "🖼️ Imagens")

        self.extract_images_var = ctk.BooleanVar(value=True)
        self.extract_images_cb = ctk.CTkCheckBox(
            self.image_section.content,
            text="Extrair imagens do documento",
            variable=self.extract_images_var,
            font=ctk.CTkFont(size=12),
            command=self._toggle_image_options,
        )

        self.image_quality_frame = ctk.CTkFrame(self.image_section.content, fg_color="transparent")

        self.image_quality_label = ctk.CTkLabel(
            self.image_quality_frame,
            text="Qualidade JPEG:",
            font=ctk.CTkFont(size=12),
        )

        self.image_quality_var = ctk.IntVar(value=95)
        self.image_quality_slider = ctk.CTkSlider(
            self.image_quality_frame,
            from_=50,
            to=100,
            number_of_steps=10,
            variable=self.image_quality_var,
            width=120,
        )

        self.image_quality_value = ctk.CTkLabel(
            self.image_quality_frame,
            text="95%",
            font=ctk.CTkFont(size=12),
            width=40,
        )

        self.image_quality_var.trace_add("write", self._update_image_quality_label)

        self.max_width_frame = ctk.CTkFrame(self.image_section.content, fg_color="transparent")

        self.max_width_label = ctk.CTkLabel(
            self.max_width_frame,
            text="Largura máxima:",
            font=ctk.CTkFont(size=12),
        )

        self.max_width_entry = ctk.CTkEntry(
            self.max_width_frame,
            width=70,
            placeholder_text="800",
        )
        self.max_width_entry.insert(0, "800")

        self.max_width_unit = ctk.CTkLabel(
            self.max_width_frame,
            text="px",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )

    def _setup_layout(self) -> None:
        """Configura o layout do painel."""
        self.header_frame.pack(fill="x")
        self.toggle_button.pack(fill="x", padx=5, pady=5)

        self.output_section.pack(fill="x", pady=(5, 8))

        self.filename_row.pack(fill="x", pady=(0, 8))
        self.filename_input_frame.pack(fill="x")
        self.filename_entry.pack(side="left", padx=(8, 0), pady=4)
        self.filename_ext_label.pack(side="right", padx=(0, 8))

        self.output_dir_row.pack(fill="x")
        self.output_dir_input_frame.pack(side="left", fill="x", expand=True)
        self.output_label.pack(fill="x", padx=10, pady=4)
        self.output_button.pack(side="left", padx=(8, 0))
        self.output_reset_button.pack(side="left", padx=(4, 0))

        self.quality_section.pack(fill="x", pady=(0, 8))
        self.quality_menu.pack(fill="x", pady=(0, 5))
        self.quality_desc.pack(anchor="w")

        self.pages_section.pack(fill="x", pady=(0, 8))
        self.pages_frame.pack(fill="x", pady=(0, 5))
        self.start_page_label.pack(side="left", padx=(0, 5))
        self.start_page_entry.pack(side="left", padx=(0, 15))
        self.end_page_label.pack(side="left", padx=(0, 5))
        self.end_page_entry.pack(side="left")
        self.pages_hint.pack(anchor="w")

        self.hf_section.pack(fill="x", pady=(0, 8))
        self.hf_frame.pack(fill="x")
        self.header_label.pack(side="left", padx=(0, 5))
        self.header_menu.pack(side="left", padx=(0, 20))
        self.footer_label.pack(side="left", padx=(0, 5))
        self.footer_menu.pack(side="left")

        self.text_section.pack(fill="x", pady=(0, 8))
        self.preserve_formatting_cb.pack(anchor="w", pady=2)
        self.preserve_layout_cb.pack(anchor="w", pady=2)
        self.merge_paragraphs_cb.pack(anchor="w", pady=2)
        self.remove_hyphenation_cb.pack(anchor="w", pady=2)

        self.image_section.pack(fill="x", pady=(0, 5))
        self.extract_images_cb.pack(anchor="w", pady=(0, 8))
        self.image_quality_frame.pack(fill="x", pady=2)
        self.image_quality_label.pack(side="left", padx=(0, 10))
        self.image_quality_slider.pack(side="left")
        self.image_quality_value.pack(side="left", padx=(5, 0))
        self.max_width_frame.pack(fill="x", pady=2)
        self.max_width_label.pack(side="left", padx=(0, 10))
        self.max_width_entry.pack(side="left")
        self.max_width_unit.pack(side="left", padx=(5, 0))

        self.content_frame.pack_forget()

    def _toggle_expansion(self) -> None:
        """Alterna entre expandido e colapsado."""
        self._expanded = not self._expanded
        if self._expanded:
            self.toggle_button.configure(text="⚙️ Opções Avançadas ▼")
            self.content_frame.pack(fill="x", padx=5, pady=(0, 10))
        else:
            self.toggle_button.configure(text="⚙️ Opções Avançadas ▶")
            self.content_frame.pack_forget()

    def _select_output_dir(self) -> None:
        """Abre diálogo para selecionar diretório de saída."""
        dir_path = filedialog.askdirectory(title="Selecionar pasta de saída")
        if dir_path:
            self._output_dir = Path(dir_path)
            display_path = str(self._output_dir)
            if len(display_path) > 40:
                display_path = "..." + display_path[-37:]
            self.output_label.configure(
                text=f"📂 {display_path}",
                text_color=("gray20", "gray80"),
            )

    def _reset_output_dir(self) -> None:
        """Reseta o diretório de saída para o padrão."""
        self._output_dir = None
        self.output_label.configure(
            text="📁 Mesmo diretório do arquivo",
            text_color=("gray40", "gray60"),
        )

    def _update_quality_description(self, *args) -> None:
        """Atualiza a descrição baseada na qualidade selecionada."""
        descriptions = {
            "Rápido": "Rápido: processamento veloz, menor precisão",
            "Equilibrado": "Equilibrado: boa qualidade com velocidade razoável",
            "Alta Qualidade": "Alta Qualidade: máxima precisão, mais lento",
        }
        self.quality_desc.configure(text=descriptions.get(self.quality_var.get(), ""))

    def _update_image_quality_label(self, *args) -> None:
        """Atualiza o label de qualidade de imagem."""
        self.image_quality_value.configure(text=f"{self.image_quality_var.get()}%")

    def _toggle_image_options(self) -> None:
        """Habilita/desabilita opções de imagem."""
        enabled = self.extract_images_var.get()
        state = "normal" if enabled else "disabled"
        self.image_quality_slider.configure(state=state)
        self.max_width_entry.configure(state=state)

    def set_input_file(self, filename: str) -> None:
        """Define o nome sugerido baseado no arquivo de entrada."""
        name_without_ext = Path(filename).stem
        self.filename_entry.delete(0, "end")
        self.filename_entry.insert(0, name_without_ext)

    def set_output_extension(self, ext: str) -> None:
        """Atualiza a extensão do arquivo de saída."""
        if not ext.startswith("."):
            ext = f".{ext}"
        self.filename_ext_label.configure(text=ext.lower())

    def get_output_filename(self) -> Optional[str]:
        """Retorna o nome do arquivo de saída (sem extensão)."""
        name = self.filename_entry.get().strip()
        return name if name else None

    def get_options(self) -> dict:
        """Retorna as opções configuradas."""
        start_page = self.start_page_entry.get()
        end_page = self.end_page_entry.get()
        max_width = self.max_width_entry.get()

        return {
            "output_dir": str(self._output_dir) if self._output_dir else None,
            "output_filename": self.get_output_filename(),
            "quality": self.quality_var.get(),
            "header_mode": self.header_var.get(),
            "footer_mode": self.footer_var.get(),
            "start_page": int(start_page) if start_page.isdigit() else None,
            "end_page": int(end_page) if end_page.isdigit() else None,
            "preserve_formatting": self.preserve_formatting_var.get(),
            "preserve_layout": self.preserve_layout_var.get(),
            "merge_paragraphs": self.merge_paragraphs_var.get(),
            "remove_hyphenation": self.remove_hyphenation_var.get(),
            "extract_images": self.extract_images_var.get(),
            "image_quality": self.image_quality_var.get(),
            "max_image_width": int(max_width) if max_width.isdigit() else 800,
        }

    def reset(self) -> None:
        """Reseta todas as opções para os valores padrão."""
        self._output_dir = None
        self.output_label.configure(
            text="📁 Mesmo diretório do arquivo",
            text_color=("gray40", "gray60"),
        )
        self.filename_entry.delete(0, "end")
        self.filename_ext_label.configure(text=".docx")
        self.quality_var.set("Equilibrado")
        self.header_var.set("Converter")
        self.footer_var.set("Converter")
        self.start_page_entry.delete(0, "end")
        self.end_page_entry.delete(0, "end")
        self.preserve_formatting_var.set(True)
        self.preserve_layout_var.set(True)
        self.merge_paragraphs_var.set(True)
        self.remove_hyphenation_var.set(True)
        self.extract_images_var.set(True)
        self.image_quality_var.set(95)
        self.max_width_entry.delete(0, "end")
        self.max_width_entry.insert(0, "800")
        self._toggle_image_options()
