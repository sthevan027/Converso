"""
VIREX - Conversor de Documentos
Interface desktop moderna com CustomTkinter.
Layout SaaS premium dark com funcionalidade completa de conversão.
"""

from __future__ import annotations

import os
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Callable, Optional

import customtkinter as ctk  # pyright: ignore[reportMissingImports]


# ═══════════════════════════════════════════════════════════════════════════════
# TEMA
# ═══════════════════════════════════════════════════════════════════════════════

class Theme:
    BG_MAIN = "#080F1A"
    BG_SIDEBAR = "#0C1322"
    BG_CARD = "#111827"
    BG_CARD_ELEVATED = "#151D2E"
    BG_INPUT = "#0D1520"
    BG_HOVER = "#1A2435"
    BORDER = "#1E293B"
    BORDER_LIGHT = "#334155"
    BORDER_FOCUS = "#3B82F6"

    PRIMARY = "#3B82F6"
    PRIMARY_HOVER = "#2563EB"
    PRIMARY_DARK = "#1E3A5F"
    PRIMARY_GLOW = "#1D4ED8"
    PRIMARY_SUBTLE = "#172554"

    ACCENT = "#8B5CF6"
    ACCENT_HOVER = "#7C3AED"

    SUCCESS = "#10B981"
    SUCCESS_DARK = "#064E3B"
    ERROR = "#EF4444"
    ERROR_DARK = "#7F1D1D"
    WARNING = "#F59E0B"
    WARNING_DARK = "#78350F"

    TEXT_PRIMARY = "#F8FAFC"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED = "#64748B"
    TEXT_DISABLED = "#475569"

    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = (FONT_FAMILY, 28, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 14)
    FONT_HEADING = (FONT_FAMILY, 13, "bold")
    FONT_BODY = (FONT_FAMILY, 12)
    FONT_SMALL = (FONT_FAMILY, 11)
    FONT_TINY = (FONT_FAMILY, 10)
    FONT_LOGO = (FONT_FAMILY, 20, "bold")
    FONT_LOGO_SUB = (FONT_FAMILY, 10)
    FONT_MENU_ICON = (FONT_FAMILY, 16)
    FONT_BTN_PRIMARY = (FONT_FAMILY, 14, "bold")
    FONT_VERSION = (FONT_FAMILY, 9)

    RADIUS_SM = 6
    RADIUS_MD = 10
    RADIUS_LG = 14
    RADIUS_XL = 16


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR BUTTON
# ═══════════════════════════════════════════════════════════════════════════════

class SidebarButton(ctk.CTkFrame):
    def __init__(
        self, master: ctk.CTkFrame, text: str, icon: str = "",
        active: bool = False, command: Callable | None = None, **kw,
    ) -> None:
        super().__init__(master, fg_color="transparent", height=44, **kw)
        self.pack_propagate(False)
        self._text, self._icon, self._command, self._active = text, icon, command, active
        self._build()
        self._apply_style()
        for w in (self, self._content, self._label):
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)
        if hasattr(self, "_icon_label"):
            self._icon_label.bind("<Button-1>", self._on_click)
            self._icon_label.bind("<Enter>", self._on_enter)
            self._icon_label.bind("<Leave>", self._on_leave)

    def _build(self) -> None:
        self._indicator = ctk.CTkFrame(self, width=3, height=28, corner_radius=2, fg_color="transparent")
        self._indicator.pack(side="left", pady=8)
        self._content = ctk.CTkFrame(self, fg_color="transparent", corner_radius=Theme.RADIUS_SM)
        self._content.pack(side="left", fill="both", expand=True, padx=(6, 14), pady=4)
        if self._icon:
            self._icon_label = ctk.CTkLabel(
                self._content, text=self._icon, font=Theme.FONT_MENU_ICON,
                text_color=Theme.TEXT_MUTED,
            )
            self._icon_label.pack(side="left", padx=(14, 10))
        self._label = ctk.CTkLabel(
            self._content, text=self._text, font=Theme.FONT_BODY,
            text_color=Theme.TEXT_MUTED, anchor="w",
        )
        self._label.pack(side="left", fill="x", expand=True, padx=(0, 14))

    def _apply_style(self) -> None:
        if self._active:
            self._indicator.configure(fg_color=Theme.PRIMARY)
            self._content.configure(fg_color=Theme.PRIMARY_SUBTLE)
            self._label.configure(text_color=Theme.TEXT_PRIMARY)
            if hasattr(self, "_icon_label"):
                self._icon_label.configure(text_color=Theme.PRIMARY)
        else:
            self._indicator.configure(fg_color="transparent")
            self._content.configure(fg_color="transparent")
            self._label.configure(text_color=Theme.TEXT_MUTED)
            if hasattr(self, "_icon_label"):
                self._icon_label.configure(text_color=Theme.TEXT_MUTED)

    def _on_click(self, _e=None) -> None:
        if self._command:
            self._command()

    def _on_enter(self, _e=None) -> None:
        if not self._active:
            self._content.configure(fg_color=Theme.BG_HOVER)
            self._label.configure(text_color=Theme.TEXT_SECONDARY)
            if hasattr(self, "_icon_label"):
                self._icon_label.configure(text_color=Theme.TEXT_SECONDARY)

    def _on_leave(self, _e=None) -> None:
        if not self._active:
            self._content.configure(fg_color="transparent")
            self._label.configure(text_color=Theme.TEXT_MUTED)
            if hasattr(self, "_icon_label"):
                self._icon_label.configure(text_color=Theme.TEXT_MUTED)

    def set_active(self, active: bool) -> None:
        self._active = active
        self._apply_style()


# ═══════════════════════════════════════════════════════════════════════════════
# FORMAT BUTTON
# ═══════════════════════════════════════════════════════════════════════════════

class FormatButton(ctk.CTkButton):
    def __init__(self, master: ctk.CTkFrame, text: str, active: bool = False,
                 command: Callable | None = None, enabled: bool = True, **kw) -> None:
        self._active = active
        self._enabled = enabled
        self._user_command = command
        self._fmt_text = text
        super().__init__(master, text=text, width=76, height=36, corner_radius=Theme.RADIUS_SM,
                         font=Theme.FONT_SMALL, border_width=1, border_color=Theme.BORDER,
                         command=self._on_click, **kw)
        self._apply_style()

    def _apply_style(self) -> None:
        if not self._enabled:
            self.configure(
                fg_color="transparent", hover_color=Theme.BG_HOVER,
                text_color=Theme.TEXT_DISABLED, border_color=Theme.BORDER,
            )
            return
        if self._active:
            self.configure(
                fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_HOVER,
                text_color=Theme.TEXT_PRIMARY, border_color=Theme.PRIMARY,
            )
        else:
            self.configure(
                fg_color="transparent", hover_color=Theme.BG_HOVER,
                text_color=Theme.TEXT_SECONDARY, border_color=Theme.BORDER_LIGHT,
            )

    def _on_click(self) -> None:
        if self._enabled and self._user_command:
            self._user_command()

    def set_active(self, active: bool) -> None:
        self._active = active
        self._apply_style()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        self._apply_style()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

class Sidebar(ctk.CTkFrame):
    WIDTH = 220

    def __init__(self, master: ctk.CTk, on_menu: Callable[[int], None] | None = None, **kw) -> None:
        super().__init__(master, width=self.WIDTH, fg_color=Theme.BG_SIDEBAR, corner_radius=0, **kw)
        self.pack_propagate(False)
        self._buttons: list[SidebarButton] = []
        self._on_menu = on_menu
        self._build_logo()
        self._build_divider()
        self._build_menu()
        self._build_footer()

    def _build_logo(self) -> None:
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=24, pady=(28, 0))

        icon_bg = ctk.CTkFrame(frame, width=38, height=38, corner_radius=10, fg_color=Theme.PRIMARY)
        icon_bg.pack(side="left", padx=(0, 12))
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(
            icon_bg, text="V", font=(Theme.FONT_FAMILY, 18, "bold"),
            text_color="#FFF",
        ).place(relx=.5, rely=.5, anchor="center")

        ctk.CTkLabel(
            frame, text="VIREX", font=Theme.FONT_LOGO,
            text_color=Theme.TEXT_PRIMARY, anchor="w",
        ).pack(side="left")

    def _build_divider(self) -> None:
        ctk.CTkFrame(self, height=1, fg_color=Theme.BORDER).pack(fill="x", padx=24, pady=(24, 20))

    def _build_menu(self) -> None:
        menu = ctk.CTkFrame(self, fg_color="transparent")
        menu.pack(fill="x")
        items = [("⇄", "Conversões"), ("⏱", "Histórico"), ("⚙", "Configurações")]
        for i, (icon, text) in enumerate(items):
            btn = SidebarButton(menu, text=text, icon=icon, active=(i == 0),
                                command=lambda idx=i: self._set_active(idx))
            btn.pack(fill="x", pady=1)
            self._buttons.append(btn)

    def _set_active(self, index: int) -> None:
        for i, btn in enumerate(self._buttons):
            btn.set_active(i == index)
        if self._on_menu:
            self._on_menu(index)

    def _build_footer(self) -> None:
        ctk.CTkFrame(self, fg_color="transparent").pack(fill="both", expand=True)

        try:
            from gui import __version__ as ver
        except ImportError:
            ver = "1.0.0"
        ctk.CTkLabel(
            self, text=f"v{ver}", font=Theme.FONT_TINY,
            text_color=Theme.TEXT_DISABLED, anchor="w",
        ).pack(anchor="w", padx=28, pady=(0, 20))


# ═══════════════════════════════════════════════════════════════════════════════
# DROP ZONE
# ═══════════════════════════════════════════════════════════════════════════════

class DropZone(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, command: Callable | None = None, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_LG, **kw)
        self._command = command
        self._file_selected = False
        self._build()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", self._draw_border)

    def _build(self) -> None:
        self._canvas = tk.Canvas(self, bg=Theme.BG_CARD, highlightthickness=0, bd=0)
        self._canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._inner = ctk.CTkFrame(self, fg_color="transparent")
        self._inner.place(relx=0.5, rely=0.5, anchor="center")

        icon_bg = ctk.CTkFrame(
            self._inner, width=56, height=56, corner_radius=28,
            fg_color=Theme.PRIMARY_SUBTLE,
        )
        icon_bg.pack(pady=(0, 14))
        icon_bg.pack_propagate(False)
        self._upload_icon = ctk.CTkLabel(
            icon_bg, text="↑", font=(Theme.FONT_FAMILY, 22, "bold"),
            text_color=Theme.PRIMARY,
        )
        self._upload_icon.place(relx=0.5, rely=0.5, anchor="center")

        self._title_lbl = ctk.CTkLabel(
            self._inner, text="Arraste ou clique para selecionar",
            font=Theme.FONT_BODY, text_color=Theme.TEXT_SECONDARY,
        )
        self._title_lbl.pack(pady=(0, 6))

        self._sub_lbl = ctk.CTkLabel(
            self._inner, text="PDF, DOCX, TXT, MD",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._sub_lbl.pack()

        for child in self._inner.winfo_children():
            child.bind("<Button-1>", self._on_click)

    def _draw_border(self, _e=None) -> None:
        c = self._canvas
        c.delete("border")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return
        pad, r = 8, 14
        x0, y0, x1, y1 = pad, pad, w - pad, h - pad
        pts = [
            x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r,
            x1, y1 - r, x1, y1, x1 - r, y1, x0 + r, y1,
            x0, y1, x0, y1 - r, x0, y0 + r, x0, y0, x0 + r, y0,
        ]
        color = Theme.SUCCESS if self._file_selected else Theme.BORDER_LIGHT
        c.create_line(*pts, fill=color, dash=(10, 6), width=2, smooth=True, tags="border")

    def set_file_selected(self, selected: bool, filename: str = "") -> None:
        self._file_selected = selected
        if selected and filename:
            display = filename if len(filename) <= 40 else filename[:37] + "..."
            self._upload_icon.configure(text="✓", text_color=Theme.SUCCESS)
            self._title_lbl.configure(text=display, text_color=Theme.SUCCESS)
            self._sub_lbl.configure(text="Clique para alterar", text_color=Theme.TEXT_MUTED)
        else:
            self._upload_icon.configure(text="↑", text_color=Theme.PRIMARY)
            self._title_lbl.configure(text="Arraste ou clique para selecionar", text_color=Theme.TEXT_SECONDARY)
            self._sub_lbl.configure(text="PDF, DOCX, TXT, MD", text_color=Theme.TEXT_MUTED)
        self._draw_border()

    def reset(self) -> None:
        self._file_selected = False
        self.set_file_selected(False)

    def _on_click(self, _e=None) -> None:
        if self._command:
            self._command()


# ═══════════════════════════════════════════════════════════════════════════════
# FILE INFO BAR
# ═══════════════════════════════════════════════════════════════════════════════

class FileInfoBar(ctk.CTkFrame):
    FILE_ICONS = {".pdf": "📕", ".docx": "📘", ".txt": "📝", ".md": "📋"}

    def __init__(self, master: ctk.CTkFrame, on_clear: Callable | None = None, **kw) -> None:
        super().__init__(
            master, fg_color=Theme.BG_CARD_ELEVATED, corner_radius=Theme.RADIUS_MD,
            border_width=1, border_color=Theme.BORDER, **kw,
        )
        self._on_clear = on_clear
        self._build()
        self.pack_forget()

    def _build(self) -> None:
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=10)

        self._icon_lbl = ctk.CTkLabel(inner, text="📄", font=(Theme.FONT_FAMILY, 20))
        self._icon_lbl.pack(side="left", padx=(0, 12))

        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        self._name_lbl = ctk.CTkLabel(
            info, text="", font=Theme.FONT_HEADING,
            text_color=Theme.TEXT_PRIMARY, anchor="w",
        )
        self._name_lbl.pack(anchor="w")
        self._detail_lbl = ctk.CTkLabel(
            info, text="", font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED, anchor="w",
        )
        self._detail_lbl.pack(anchor="w", pady=(2, 0))

        ctk.CTkButton(
            inner, text="✕", width=32, height=32, corner_radius=Theme.RADIUS_SM,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, font=Theme.FONT_BODY,
            command=self._clear,
        ).pack(side="right")

    def set_file(self, path: Path, file_type: str = "") -> None:
        ext = path.suffix.lower()
        self._icon_lbl.configure(text=self.FILE_ICONS.get(ext, "📄"))
        self._name_lbl.configure(text=path.name)
        size = path.stat().st_size
        if size < 1024:
            sz = f"{size} B"
        elif size < 1024 * 1024:
            sz = f"{size / 1024:.1f} KB"
        else:
            sz = f"{size / (1024 * 1024):.1f} MB"
        parent = str(path.parent)
        if len(parent) > 50:
            parent = "..." + parent[-47:]
        self._detail_lbl.configure(text=f"{file_type}  ·  {sz}  ·  {parent}")
        self.pack(fill="x", pady=(0, 16))

    def clear(self) -> None:
        self.pack_forget()

    def _clear(self) -> None:
        if self._on_clear:
            self._on_clear()


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS PANEL
# ═══════════════════════════════════════════════════════════════════════════════

class ProgressPanel(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, **kw) -> None:
        super().__init__(
            master, fg_color=Theme.BG_CARD_ELEVATED, corner_radius=Theme.RADIUS_LG,
            border_width=1, border_color=Theme.BORDER, **kw,
        )
        self._output_path: Optional[Path] = None
        self._build()
        self.pack_forget()

    def _build(self) -> None:
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(18, 10))
        self._status_icon = ctk.CTkLabel(hdr, text="⏳", font=(Theme.FONT_FAMILY, 18))
        self._status_icon.pack(side="left", padx=(0, 10))
        self._status_lbl = ctk.CTkLabel(
            hdr, text="Preparando...", font=Theme.FONT_HEADING,
            text_color=Theme.TEXT_PRIMARY, anchor="w",
        )
        self._status_lbl.pack(side="left", fill="x", expand=True)
        self._pct_lbl = ctk.CTkLabel(
            hdr, text="0%", font=Theme.FONT_HEADING,
            text_color=Theme.PRIMARY,
        )
        self._pct_lbl.pack(side="right")

        bar_frame = ctk.CTkFrame(self, fg_color=Theme.BG_INPUT, height=8, corner_radius=4)
        bar_frame.pack(fill="x", padx=18, pady=(0, 10))
        self._bar = ctk.CTkProgressBar(
            self, height=8, corner_radius=4,
            progress_color=Theme.PRIMARY, fg_color=Theme.BG_INPUT,
        )
        self._bar.set(0)
        self._bar.pack(fill="x", padx=18, pady=(0, 10))
        bar_frame.pack_forget()

        self._log_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._log_frame.pack(fill="x", padx=18, pady=(0, 10))
        ctk.CTkLabel(
            self._log_frame, text="Log", font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED, anchor="w",
        ).pack(anchor="w", pady=(0, 6))
        self._log_box = ctk.CTkTextbox(
            self._log_frame, height=100, font=("Consolas", 10),
            fg_color=Theme.BG_INPUT, text_color=Theme.TEXT_SECONDARY,
            corner_radius=Theme.RADIUS_SM, state="disabled",
        )
        self._log_box.pack(fill="x")

        self._result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._result_icon = ctk.CTkLabel(self._result_frame, text="", font=(Theme.FONT_FAMILY, 32))
        self._result_icon.pack(anchor="center")
        self._result_lbl = ctk.CTkLabel(self._result_frame, text="", font=Theme.FONT_BODY)
        self._result_lbl.pack(anchor="center", pady=(6, 0))
        self._result_detail = ctk.CTkLabel(
            self._result_frame, text="", font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED,
        )
        self._result_detail.pack(anchor="center")

        self._btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._open_file_btn = ctk.CTkButton(
            self._btn_frame, text="📄 Abrir Arquivo", font=Theme.FONT_BODY, height=36,
            corner_radius=Theme.RADIUS_SM, fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER, command=self._open_file,
        )
        self._open_folder_btn = ctk.CTkButton(
            self._btn_frame, text="📂 Abrir Pasta", font=Theme.FONT_BODY, height=36,
            corner_radius=Theme.RADIUS_SM, fg_color="transparent", border_width=1,
            border_color=Theme.BORDER_LIGHT, hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_SECONDARY, command=self._open_folder,
        )
        self._close_btn = ctk.CTkButton(
            self._btn_frame, text="✕", width=36, height=36,
            corner_radius=Theme.RADIUS_SM, fg_color="transparent",
            hover_color=Theme.BG_HOVER, text_color=Theme.TEXT_MUTED,
            command=lambda: self.set_visible(False),
        )

    def set_visible(self, v: bool) -> None:
        if v:
            self.pack(fill="x", pady=(0, 16))
        else:
            self.pack_forget()

    def reset(self) -> None:
        self.set_progress(0)
        self._status_icon.configure(text="⏳")
        self._status_lbl.configure(text="Preparando...")
        self._pct_lbl.configure(text_color=Theme.PRIMARY)
        self._bar.configure(progress_color=Theme.PRIMARY)
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")
        self._output_path = None
        self._log_frame.pack(fill="x", padx=18, pady=(0, 10))
        self._result_frame.pack_forget()
        self._btn_frame.pack_forget()

    def set_progress(self, val: int) -> None:
        self._bar.set(max(0, min(100, val)) / 100)
        self._pct_lbl.configure(text=f"{val}%")

    def set_status(self, msg: str) -> None:
        self._status_lbl.configure(text=msg)

    def add_log(self, msg: str) -> None:
        self._log_box.configure(state="normal")
        self._log_box.insert("end", f"{msg}\n")
        self._log_box.see("end")
        self._log_box.configure(state="disabled")

    def show_success(self, message: str = "Conversão concluída!", details: str = "",
                     output_path: Optional[Path] = None) -> None:
        self._output_path = output_path
        self.set_progress(100)
        self._status_icon.configure(text="✅")
        self._status_lbl.configure(text=message)
        self._pct_lbl.configure(text_color=Theme.SUCCESS)
        self._bar.configure(progress_color=Theme.SUCCESS)
        self._log_frame.pack_forget()
        self._result_frame.pack(fill="x", padx=18, pady=(4, 10))
        self._result_icon.configure(text="🎉")
        self._result_lbl.configure(text="Arquivo convertido com sucesso!", text_color=Theme.SUCCESS)
        self._result_detail.configure(text=details)
        self._btn_frame.pack(fill="x", padx=18, pady=(0, 18))
        if output_path:
            self._open_file_btn.pack(side="left", padx=(0, 8))
            self._open_folder_btn.pack(side="left")
        self._close_btn.pack(side="right")

    def show_error(self, message: str = "Erro na conversão", details: str = "") -> None:
        self._status_icon.configure(text="❌")
        self._status_lbl.configure(text=message)
        self._pct_lbl.configure(text_color=Theme.ERROR)
        self._bar.configure(progress_color=Theme.ERROR)
        self._result_frame.pack(fill="x", padx=18, pady=(4, 10))
        self._result_icon.configure(text="😞")
        self._result_lbl.configure(text="Ocorreu um erro durante a conversão", text_color=Theme.ERROR)
        self._result_detail.configure(text=details)
        self._btn_frame.pack(fill="x", padx=18, pady=(0, 18))
        self._open_file_btn.pack_forget()
        self._open_folder_btn.pack_forget()
        self._close_btn.pack(side="right")

    def _open_file(self) -> None:
        if self._output_path and self._output_path.exists():
            if sys.platform == "win32":
                os.startfile(self._output_path)  # noqa: S606
            elif sys.platform == "darwin":
                subprocess.run(["open", str(self._output_path)])
            else:
                subprocess.run(["xdg-open", str(self._output_path)])

    def _open_folder(self) -> None:
        if self._output_path and self._output_path.exists():
            folder = self._output_path.parent
            if sys.platform == "win32":
                os.startfile(folder)  # noqa: S606
            elif sys.platform == "darwin":
                subprocess.run(["open", str(folder)])
            else:
                subprocess.run(["xdg-open", str(folder)])


# ═══════════════════════════════════════════════════════════════════════════════
# OPTIONS PANEL
# ═══════════════════════════════════════════════════════════════════════════════

class OptionsSection(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, title: str, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_INPUT, corner_radius=Theme.RADIUS_SM, **kw)
        ctk.CTkLabel(
            self, text=title, font=(Theme.FONT_FAMILY, 11, "bold"),
            text_color=Theme.TEXT_MUTED,
        ).pack(anchor="w", padx=14, pady=(10, 6))
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="x", padx=14, pady=(0, 12))


class OptionsPanel(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, **kw) -> None:
        super().__init__(master, fg_color="transparent", **kw)
        self._expanded = False
        self._output_dir: Optional[Path] = None
        self._build()

    def _build(self) -> None:
        self._toggle_btn = ctk.CTkButton(
            self, text="Opções avançadas  ▸", font=Theme.FONT_SMALL,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, anchor="w", height=36,
            command=self._toggle,
        )
        self._toggle_btn.pack(fill="x")

        self._content = ctk.CTkFrame(self, fg_color="transparent")

        sec = OptionsSection(self._content, "📁 Saída")
        sec.pack(fill="x", pady=(8, 6))
        row1 = ctk.CTkFrame(sec.content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        inp_frame = ctk.CTkFrame(row1, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_SM)
        inp_frame.pack(fill="x")
        self._filename_entry = ctk.CTkEntry(
            inp_frame, placeholder_text="mesmo nome do original", width=200,
            height=32, border_width=0, fg_color="transparent",
            text_color=Theme.TEXT_PRIMARY, placeholder_text_color=Theme.TEXT_DISABLED,
        )
        self._filename_entry.pack(side="left", padx=(10, 0), pady=4)
        self._ext_lbl = ctk.CTkLabel(
            inp_frame, text=".docx", font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.PRIMARY, width=50,
        )
        self._ext_lbl.pack(side="right", padx=(0, 10))

        row2 = ctk.CTkFrame(sec.content, fg_color="transparent")
        row2.pack(fill="x")
        dir_frame = ctk.CTkFrame(row2, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_SM)
        dir_frame.pack(side="left", fill="x", expand=True)
        self._dir_lbl = ctk.CTkLabel(
            dir_frame, text="📁 Mesmo diretório do arquivo", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED, anchor="w", height=32,
        )
        self._dir_lbl.pack(fill="x", padx=10, pady=4)
        ctk.CTkButton(
            row2, text="Alterar", width=68, height=32, font=Theme.FONT_SMALL,
            corner_radius=Theme.RADIUS_SM, fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER, command=self._select_output_dir,
        ).pack(side="left", padx=(8, 0))
        ctk.CTkButton(
            row2, text="↺", width=32, height=32, corner_radius=Theme.RADIUS_SM,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            text_color=Theme.TEXT_MUTED, command=self._reset_output_dir,
        ).pack(side="left", padx=(4, 0))

        sec2 = OptionsSection(self._content, "⚡ Qualidade")
        sec2.pack(fill="x", pady=(0, 6))
        self._quality_var = ctk.StringVar(value="Equilibrado")
        ctk.CTkSegmentedButton(
            sec2.content, values=["Rápido", "Equilibrado", "Alta Qualidade"],
            variable=self._quality_var,
        ).pack(fill="x", pady=(0, 6))
        self._quality_desc = ctk.CTkLabel(
            sec2.content, text="Equilibrado: boa qualidade com velocidade razoável",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._quality_desc.pack(anchor="w")
        self._quality_var.trace_add("write", self._update_quality_desc)

        sec3 = OptionsSection(self._content, "📄 Páginas")
        sec3.pack(fill="x", pady=(0, 6))
        pf = ctk.CTkFrame(sec3.content, fg_color="transparent")
        pf.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(pf, text="De:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self._start_page = ctk.CTkEntry(
            pf, width=68, placeholder_text="1", height=30,
            fg_color=Theme.BG_CARD, border_width=0, text_color=Theme.TEXT_PRIMARY,
        )
        self._start_page.pack(side="left", padx=(0, 14))
        ctk.CTkLabel(pf, text="Até:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self._end_page = ctk.CTkEntry(
            pf, width=68, placeholder_text="Última", height=30,
            fg_color=Theme.BG_CARD, border_width=0, text_color=Theme.TEXT_PRIMARY,
        )
        self._end_page.pack(side="left")
        ctk.CTkLabel(
            sec3.content, text="Deixe vazio para converter todas",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_DISABLED,
        ).pack(anchor="w")

        sec4 = OptionsSection(self._content, "📋 Cabeçalho e Rodapé")
        sec4.pack(fill="x", pady=(0, 6))
        hf = ctk.CTkFrame(sec4.content, fg_color="transparent")
        hf.pack(fill="x")
        ctk.CTkLabel(hf, text="Cabeçalho:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self._header_var = ctk.StringVar(value="Converter")
        ctk.CTkComboBox(
            hf, values=["Manter", "Remover", "Converter"], variable=self._header_var,
            width=108, state="readonly", fg_color=Theme.BG_CARD,
            border_color=Theme.BORDER, button_color=Theme.PRIMARY,
        ).pack(side="left", padx=(0, 18))
        ctk.CTkLabel(hf, text="Rodapé:", font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY).pack(side="left", padx=(0, 6))
        self._footer_var = ctk.StringVar(value="Converter")
        ctk.CTkComboBox(
            hf, values=["Manter", "Remover", "Converter"], variable=self._footer_var,
            width=108, state="readonly", fg_color=Theme.BG_CARD,
            border_color=Theme.BORDER, button_color=Theme.PRIMARY,
        ).pack(side="left")

        sec5 = OptionsSection(self._content, "📝 Texto")
        sec5.pack(fill="x", pady=(0, 6))
        self._preserve_fmt = ctk.BooleanVar(value=True)
        self._preserve_layout = ctk.BooleanVar(value=True)
        self._merge_para = ctk.BooleanVar(value=True)
        self._rm_hyphen = ctk.BooleanVar(value=True)
        for var, txt in [
            (self._preserve_fmt, "Preservar formatação (negrito, itálico)"),
            (self._preserve_layout, "Preservar layout de colunas"),
            (self._merge_para, "Mesclar parágrafos fragmentados"),
            (self._rm_hyphen, "Remover hifenização de fim de linha"),
        ]:
            ctk.CTkCheckBox(
                sec5.content, text=txt, variable=var, font=Theme.FONT_SMALL,
                text_color=Theme.TEXT_SECONDARY, fg_color=Theme.PRIMARY,
                hover_color=Theme.PRIMARY_HOVER, border_color=Theme.BORDER_LIGHT,
                corner_radius=4,
            ).pack(anchor="w", pady=3)

        sec6 = OptionsSection(self._content, "🖼️ Imagens")
        sec6.pack(fill="x", pady=(0, 4))
        self._extract_img = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            sec6.content, text="Extrair imagens do documento", variable=self._extract_img,
            font=Theme.FONT_SMALL, text_color=Theme.TEXT_SECONDARY, fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER, border_color=Theme.BORDER_LIGHT,
            corner_radius=4, command=self._toggle_img_opts,
        ).pack(anchor="w", pady=(0, 8))
        self._img_q_frame = ctk.CTkFrame(sec6.content, fg_color="transparent")
        self._img_q_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(
            self._img_q_frame, text="Qualidade JPEG:", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY,
        ).pack(side="left", padx=(0, 10))
        self._img_quality = ctk.IntVar(value=95)
        ctk.CTkSlider(
            self._img_q_frame, from_=50, to=100, number_of_steps=10,
            variable=self._img_quality, width=120,
        ).pack(side="left")
        self._img_q_lbl = ctk.CTkLabel(
            self._img_q_frame, text="95%", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY, width=38,
        )
        self._img_q_lbl.pack(side="left", padx=(6, 0))
        self._img_quality.trace_add("write", lambda *_: self._img_q_lbl.configure(text=f"{self._img_quality.get()}%"))

        mw = ctk.CTkFrame(sec6.content, fg_color="transparent")
        mw.pack(fill="x", pady=3)
        ctk.CTkLabel(
            mw, text="Largura máxima:", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_SECONDARY,
        ).pack(side="left", padx=(0, 10))
        self._max_width = ctk.CTkEntry(
            mw, width=68, placeholder_text="800", height=30,
            fg_color=Theme.BG_CARD, border_width=0, text_color=Theme.TEXT_PRIMARY,
        )
        self._max_width.insert(0, "800")
        self._max_width.pack(side="left")
        ctk.CTkLabel(mw, text="px", font=Theme.FONT_TINY, text_color=Theme.TEXT_DISABLED).pack(side="left", padx=(6, 0))

    def _toggle(self) -> None:
        self._expanded = not self._expanded
        if self._expanded:
            self._toggle_btn.configure(text="Opções avançadas  ▾")
            self._content.pack(fill="x", pady=(6, 0))
        else:
            self._toggle_btn.configure(text="Opções avançadas  ▸")
            self._content.pack_forget()

    def _toggle_img_opts(self) -> None:
        state = "normal" if self._extract_img.get() else "disabled"
        for w in self._img_q_frame.winfo_children():
            try:
                w.configure(state=state)
            except Exception:
                pass

    def _select_output_dir(self) -> None:
        d = filedialog.askdirectory(title="Selecionar pasta de saída")
        if d:
            self._output_dir = Path(d)
            disp = str(self._output_dir)
            if len(disp) > 40:
                disp = "..." + disp[-37:]
            self._dir_lbl.configure(text=f"📂 {disp}", text_color=Theme.TEXT_SECONDARY)

    def _reset_output_dir(self) -> None:
        self._output_dir = None
        self._dir_lbl.configure(text="📁 Mesmo diretório do arquivo", text_color=Theme.TEXT_MUTED)

    def _update_quality_desc(self, *_) -> None:
        descs = {
            "Rápido": "Rápido: processamento veloz, menor precisão",
            "Equilibrado": "Equilibrado: boa qualidade com velocidade razoável",
            "Alta Qualidade": "Alta Qualidade: máxima precisão, mais lento",
        }
        self._quality_desc.configure(text=descs.get(self._quality_var.get(), ""))

    def set_input_file(self, filename: str) -> None:
        self._filename_entry.delete(0, "end")
        self._filename_entry.insert(0, Path(filename).stem)

    def set_output_extension(self, ext: str) -> None:
        if not ext.startswith("."):
            ext = f".{ext}"
        self._ext_lbl.configure(text=ext.lower())

    def get_options(self) -> dict:
        sp, ep = self._start_page.get(), self._end_page.get()
        mw = self._max_width.get()
        return {
            "output_dir": str(self._output_dir) if self._output_dir else None,
            "output_filename": self._filename_entry.get().strip() or None,
            "quality": self._quality_var.get(),
            "header_mode": self._header_var.get(),
            "footer_mode": self._footer_var.get(),
            "start_page": int(sp) if sp.isdigit() else None,
            "end_page": int(ep) if ep.isdigit() else None,
            "preserve_formatting": self._preserve_fmt.get(),
            "preserve_layout": self._preserve_layout.get(),
            "merge_paragraphs": self._merge_para.get(),
            "remove_hyphenation": self._rm_hyphen.get(),
            "extract_images": self._extract_img.get(),
            "image_quality": self._img_quality.get(),
            "max_image_width": int(mw) if mw.isdigit() else 800,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CARD
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_FORMATS = {".pdf": ["DOCX"], ".docx": ["PDF"], ".txt": ["PDF"], ".md": ["PDF"]}
FILE_TYPE_NAMES = {".pdf": "PDF", ".docx": "Word", ".txt": "Texto", ".md": "Markdown"}
IMPLEMENTED_FORMATS = {"docx", "pdf"}


class MainCard(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, on_converted: Callable | None = None, **kw) -> None:
        super().__init__(
            master, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_XL,
            border_width=1, border_color=Theme.BORDER, **kw,
        )
        self._on_converted = on_converted
        self.selected_file: Optional[Path] = None
        self.is_converting = False
        self._format_buttons: list[FormatButton] = []
        self._available_formats: list[str] = []
        self._build()

    def _build(self) -> None:
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.BORDER_LIGHT,
        )
        self._scroll.pack(fill="both", expand=True, padx=24, pady=24)
        content = self._scroll

        ctk.CTkLabel(
            content, text="Formato de saída", font=Theme.FONT_TINY,
            text_color=Theme.TEXT_MUTED, anchor="w",
        ).pack(anchor="w", pady=(0, 8))

        self._fmt_row = ctk.CTkFrame(content, fg_color="transparent")
        self._fmt_row.pack(anchor="w", pady=(0, 4))
        self._fmt_warning = ctk.CTkLabel(
            content, text="", font=Theme.FONT_TINY,
            text_color=Theme.WARNING, anchor="w",
        )
        self._fmt_warning.pack(anchor="w", pady=(0, 14))
        self._init_format_buttons()

        self._file_info = FileInfoBar(content, on_clear=self._clear_selection)

        self._drop_zone = DropZone(content, command=self._open_file_dialog, height=180)
        self._drop_zone.pack(fill="x", pady=(0, 14))

        self._opts_panel = OptionsPanel(content)
        self._opts_panel.pack(fill="x", pady=(0, 14))
        try:
            from gui.settings_store import load_settings
            st = load_settings()
            self._opts_panel._quality_var.set(st.get("default_quality", "Equilibrado"))
            self._opts_panel._extract_img.set(st.get("extract_images", True))
            self._opts_panel._update_quality_desc()
        except Exception:
            pass

        self._progress = ProgressPanel(content)

        self._footer = ctk.CTkFrame(content, fg_color="transparent")
        self._footer.pack(fill="x", pady=(6, 0))

        self._status_row = ctk.CTkFrame(self._footer, fg_color="transparent")
        self._status_row.pack(side="left")
        self._status_dot = ctk.CTkFrame(
            self._status_row, width=8, height=8,
            corner_radius=4, fg_color=Theme.TEXT_DISABLED,
        )
        self._status_dot.pack(side="left", padx=(0, 8))
        self._status_text = ctk.CTkLabel(
            self._status_row, text="Selecione um arquivo",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED,
        )
        self._status_text.pack(side="left")

        self._convert_btn = ctk.CTkButton(
            self._footer, text="Converter", width=160, height=44,
            corner_radius=Theme.RADIUS_SM, font=Theme.FONT_BTN_PRIMARY,
            fg_color=Theme.BORDER, hover_color=Theme.BORDER,
            text_color=Theme.TEXT_DISABLED, state="disabled",
            command=self._start_conversion,
        )
        self._convert_btn.pack(side="right")

    def _init_format_buttons(self) -> None:
        all_fmts = ["PDF", "DOCX", "HTML", "MD"]
        for i, fmt in enumerate(all_fmts):
            btn = FormatButton(self._fmt_row, text=fmt, active=False, enabled=False,
                               command=lambda idx=i: self._select_format(idx))
            btn.pack(side="left", padx=(0, 10))
            self._format_buttons.append(btn)

    def _select_format(self, index: int) -> None:
        for i, btn in enumerate(self._format_buttons):
            btn.set_active(i == index)
        fmt = self._format_buttons[index]._fmt_text.lower()
        self._opts_panel.set_output_extension(fmt)
        if fmt in IMPLEMENTED_FORMATS:
            self._fmt_warning.configure(text="")
            self._set_convert_enabled(True)
        else:
            self._fmt_warning.configure(text=f"⚠️ Conversão para {fmt.upper()} será implementada em breve")
            self._set_convert_enabled(False)

    def _set_convert_enabled(self, enabled: bool) -> None:
        if enabled and self.selected_file and not self.is_converting:
            self._convert_btn.configure(
                state="normal", fg_color=Theme.PRIMARY,
                hover_color=Theme.PRIMARY_HOVER, text_color="#FFF",
            )
            self._status_dot.configure(fg_color=Theme.SUCCESS)
            self._status_text.configure(text="Pronto para converter", text_color=Theme.SUCCESS)
        else:
            self._convert_btn.configure(
                state="disabled", fg_color=Theme.BORDER,
                hover_color=Theme.BORDER, text_color=Theme.TEXT_DISABLED,
            )
            if not self.selected_file:
                self._status_dot.configure(fg_color=Theme.TEXT_MUTED)
                self._status_text.configure(text="Selecione um arquivo", text_color=Theme.TEXT_MUTED)

    def _open_file_dialog(self) -> None:
        fp = filedialog.askopenfilename(
            title="Selecionar arquivo para conversão",
            filetypes=[
                ("Todos suportados", "*.pdf *.docx *.txt *.md"),
                ("PDF", "*.pdf"), ("DOCX", "*.docx"),
                ("Texto", "*.txt"), ("Markdown", "*.md"),
            ],
        )
        if fp:
            self._on_file_selected(Path(fp))

    def _on_file_selected(self, path: Path) -> None:
        if not path.exists():
            return
        ext = path.suffix.lower()
        if ext not in OUTPUT_FORMATS:
            self._status_text.configure(text=f"Formato {ext} não suportado", text_color=Theme.ERROR)
            self._status_dot.configure(fg_color=Theme.ERROR)
            return

        self.selected_file = path
        file_type = FILE_TYPE_NAMES.get(ext, "Arquivo")
        self._file_info.set_file(path, file_type)
        self._drop_zone.set_file_selected(True, path.name)
        self._opts_panel.set_input_file(path.name)

        available = OUTPUT_FORMATS.get(ext, [])
        self._available_formats = available
        all_fmts = ["PDF", "DOCX", "HTML", "MD"]
        for i, fmt in enumerate(all_fmts):
            enabled = fmt in available
            self._format_buttons[i].set_enabled(enabled)
            self._format_buttons[i].set_active(False)

        if available:
            first_idx = all_fmts.index(available[0])
            self._select_format(first_idx)

    def apply_default_settings(self) -> None:
        """Aplica os padrões das Configurações ao painel de opções (ex.: ao abrir a página)."""
        try:
            from gui.settings_store import load_settings
            st = load_settings()
            self._opts_panel._quality_var.set(st.get("default_quality", "Equilibrado"))
            self._opts_panel._extract_img.set(st.get("extract_images", True))
            self._opts_panel._update_quality_desc()
            self._opts_panel._toggle_img_opts()
        except Exception:
            pass

    def _clear_selection(self) -> None:
        self.selected_file = None
        self._file_info.clear()
        self._drop_zone.reset()
        for btn in self._format_buttons:
            btn.set_enabled(False)
            btn.set_active(False)
        self._fmt_warning.configure(text="")
        self._set_convert_enabled(False)
        self._status_text.configure(text="Selecione um arquivo", text_color=Theme.TEXT_MUTED)
        self._status_dot.configure(fg_color=Theme.TEXT_MUTED)
        self._progress.set_visible(False)

    def _start_conversion(self) -> None:
        if not self.selected_file or self.is_converting:
            return
        self.is_converting = True
        self._update_ui_converting(True)

        options = self._opts_panel.get_options()
        active_fmt = ""
        for btn in self._format_buttons:
            if btn._active:
                active_fmt = btn._fmt_text.lower()
                break

        thread = threading.Thread(
            target=self._run_conversion,
            args=(self.selected_file, active_fmt, options),
            daemon=True,
        )
        thread.start()

    def _run_conversion(self, input_file: Path, target_format: str, options: dict) -> None:
        try:
            from conversores.base import ConversionOptions, HeaderFooterMode, TranscriptionQuality
            from conversores.docx_converter import DocxConverter
            from conversores.pdf_converter import PdfConverter
            from utils.file_utils import build_output_path

            self.after(0, lambda: self._progress.set_status("Preparando conversão..."))
            self.after(0, lambda: self._progress.set_progress(5))
            self.after(0, lambda: self._progress.add_log(f"📄 Arquivo: {input_file.name}"))
            self.after(0, lambda: self._progress.add_log(f"🎯 Formato de saída: {target_format.upper()}"))

            hf_map = {
                "Manter": HeaderFooterMode.KEEP,
                "Remover": HeaderFooterMode.REMOVE,
                "Converter": HeaderFooterMode.CONVERT_TO_HEADER,
            }
            q_map = {
                "Rápido": TranscriptionQuality.FAST,
                "Equilibrado": TranscriptionQuality.BALANCED,
                "Alta Qualidade": TranscriptionQuality.HIGH,
            }

            self.after(0, lambda: self._progress.set_progress(10))
            self.after(0, lambda: self._progress.add_log("⚙️ Configurando opções..."))

            conv_opts = ConversionOptions(
                start_page=options.get("start_page"),
                end_page=options.get("end_page"),
                verbose=True,
                header_mode=hf_map.get(options.get("header_mode", "Converter"), HeaderFooterMode.CONVERT_TO_HEADER),
                footer_mode=hf_map.get(options.get("footer_mode", "Converter"), HeaderFooterMode.CONVERT_TO_HEADER),
                transcription_quality=q_map.get(options.get("quality", "Equilibrado"), TranscriptionQuality.BALANCED),
                preserve_formatting=options.get("preserve_formatting", True),
                preserve_layout=options.get("preserve_layout", True),
                merge_paragraphs=options.get("merge_paragraphs", True),
                remove_hyphenation=options.get("remove_hyphenation", True),
                extract_images=options.get("extract_images", True),
                image_quality=options.get("image_quality", 95),
                max_image_width=options.get("max_image_width", 800),
            )

            converters = {"docx": DocxConverter, "pdf": PdfConverter}
            converter_cls = converters.get(target_format)
            if not converter_cls:
                raise ValueError(f"Formato de saída não suportado: {target_format}")

            self.after(0, lambda: self._progress.set_status("Processando documento..."))
            self.after(0, lambda: self._progress.set_progress(20))
            self.after(0, lambda: self._progress.add_log("📖 Lendo documento de entrada..."))

            output_dir = options.get("output_dir")
            if not output_dir:
                try:
                    from gui.settings_store import load_settings
                    st = load_settings()
                    default_dir = st.get("default_output_dir")
                    if default_dir:
                        output_dir = default_dir
                except Exception:
                    pass
            output_filename = options.get("output_filename")
            if output_filename:
                base_dir = Path(output_dir) if output_dir else input_file.parent
                output_path = base_dir / f"{output_filename}.{target_format}"
            else:
                output_path = build_output_path(str(input_file), output_dir, target_format)

            self.after(0, lambda: self._progress.set_status("Convertendo..."))
            self.after(0, lambda: self._progress.set_progress(40))
            self.after(0, lambda: self._progress.add_log("🔄 Convertendo conteúdo..."))

            converter = converter_cls(options=conv_opts)
            result = converter.convert(str(input_file), str(output_path))

            self.after(0, lambda: self._progress.set_progress(90))
            self.after(0, lambda: self._progress.add_log("💾 Salvando arquivo..."))

            pages = result.pages_converted
            images = result.images_extracted or 0
            details = f"{pages} página(s) convertida(s)"
            if images > 0:
                details += f" · {images} imagem(ns) extraída(s)"

            self.after(0, lambda: self._progress.add_log(f"✅ Concluído: {Path(output_path).name}"))
            self.after(0, lambda: self._progress.show_success(
                message="Conversão concluída!", details=details, output_path=Path(output_path)))
            self.after(0, lambda: self._conversion_finished(True))

            try:
                from gui.history_store import add_entry
                add_entry(
                    input_file=str(input_file),
                    output_format=target_format,
                    output_file=str(output_path),
                    status="success",
                    pages=pages,
                    images=images,
                )
            except Exception:
                pass

        except Exception as exc:
            err = str(exc)
            self.after(0, lambda: self._progress.add_log(f"❌ Erro: {err}"))
            self.after(0, lambda: self._progress.show_error(
                message="Erro na conversão",
                details=err[:120] + "..." if len(err) > 120 else err,
            ))
            self.after(0, lambda: self._conversion_finished(False))

            try:
                from gui.history_store import add_entry
                add_entry(
                    input_file=str(input_file),
                    output_format=target_format,
                    output_file="",
                    status="error",
                    error=err[:200],
                )
            except Exception:
                pass

    def _conversion_finished(self, _success: bool) -> None:
        self.is_converting = False
        self._update_ui_converting(False)

    def _update_ui_converting(self, converting: bool) -> None:
        if converting:
            self._convert_btn.configure(
                state="disabled", text="Convertendo...",
                fg_color=Theme.PRIMARY_DARK, text_color=Theme.TEXT_MUTED,
            )
            self._progress.reset()
            self._progress.set_visible(True)
        else:
            self._convert_btn.configure(text="Converter")
            if self.selected_file:
                self._set_convert_enabled(True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE BASE
# ═══════════════════════════════════════════════════════════════════════════════

class PageBase(ctk.CTkFrame):
    """Frame base para todas as páginas com título."""

    def __init__(self, master: ctk.CTkFrame, title: str, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_MAIN, corner_radius=0, **kw)
        self._wrapper = ctk.CTkFrame(self, fg_color="transparent")
        self._wrapper.pack(fill="both", expand=True, padx=32, pady=28)
        ctk.CTkLabel(
            self._wrapper, text=title,
            font=Theme.FONT_TITLE, text_color=Theme.TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w", pady=(0, 24))
        self.body = ctk.CTkFrame(self._wrapper, fg_color="transparent")
        self.body.pack(fill="both", expand=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSION PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class ConversionPage(PageBase):
    def __init__(self, master: ctk.CTkFrame, on_converted: Callable | None = None, **kw) -> None:
        super().__init__(master, title="Conversor de Documentos", **kw)
        self._on_converted = on_converted
        self.main_card = MainCard(self.body, on_converted=on_converted)
        self.main_card.pack(fill="both", expand=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HISTORY PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class _HistoryRow(ctk.CTkFrame):
    STATUS_ICONS = {"success": "✓", "error": "✕"}
    STATUS_COLORS = {"success": Theme.SUCCESS, "error": Theme.ERROR}
    FMT_ICONS = {".pdf": "📕", ".docx": "📘", ".txt": "📝", ".md": "📋"}

    def __init__(self, master: ctk.CTkFrame, entry: dict, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_SM, **kw)
        self._entry = entry
        self._build()

    def _build(self) -> None:
        e = self._entry
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=10)

        ext = Path(e.get("input_file", "")).suffix.lower()
        icon = self.FMT_ICONS.get(ext, "📄")
        ctk.CTkLabel(inner, text=icon, font=(Theme.FONT_FAMILY, 18)).pack(side="left", padx=(0, 12))

        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        name_row = ctk.CTkFrame(info, fg_color="transparent")
        name_row.pack(fill="x")
        ctk.CTkLabel(
            name_row, text=e.get("input_name", "?"),
            font=Theme.FONT_BODY, text_color=Theme.TEXT_PRIMARY, anchor="w",
        ).pack(side="left")
        ctk.CTkLabel(
            name_row, text=f"→  .{e.get('output_format', '?')}",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED, anchor="w",
        ).pack(side="left", padx=(8, 0))

        details = []
        pages = e.get("pages", 0)
        if pages:
            details.append(f"{pages} pág.")
        images = e.get("images", 0)
        if images:
            details.append(f"{images} img.")
        ts = e.get("timestamp", "")
        if ts:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(ts)
                details.append(dt.strftime("%d/%m/%Y  %H:%M"))
            except ValueError:
                details.append(ts)
        ctk.CTkLabel(
            info, text="  ·  ".join(details) if details else "",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_MUTED, anchor="w",
        ).pack(anchor="w", pady=(2, 0))

        # Onde foi salvo (pasta ou caminho do arquivo)
        output_file = e.get("output_file", "")
        if output_file and e.get("status") == "success":
            out_path = Path(output_file)
            save_dir = str(out_path.parent)
            if len(save_dir) > 55:
                save_dir = "..." + save_dir[-52:]
            path_lbl = ctk.CTkLabel(
                info, text=f"Salvo em: {save_dir}",
                font=Theme.FONT_TINY, text_color=Theme.TEXT_DISABLED, anchor="w",
            )
            path_lbl.pack(anchor="w", pady=(2, 0))

        status = e.get("status", "success")
        color = self.STATUS_COLORS.get(status, Theme.TEXT_MUTED)
        icon_txt = self.STATUS_ICONS.get(status, "?")
        badge = ctk.CTkFrame(inner, fg_color=color, width=26, height=26, corner_radius=13)
        badge.pack(side="right")
        badge.pack_propagate(False)
        ctk.CTkLabel(
            badge, text=icon_txt, font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color="#FFF",
        ).place(relx=.5, rely=.5, anchor="center")


class HistoryPage(PageBase):
    def __init__(self, master: ctk.CTkFrame, **kw) -> None:
        super().__init__(master, title="Histórico", **kw)
        self._build_content()

    def _build_content(self) -> None:
        toolbar = ctk.CTkFrame(self.body, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 16))

        self._count_lbl = ctk.CTkLabel(
            toolbar, text="", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED, anchor="w",
        )
        self._count_lbl.pack(side="left")

        self._clear_btn = ctk.CTkButton(
            toolbar, text="Limpar histórico", width=130, height=32,
            font=Theme.FONT_SMALL, corner_radius=Theme.RADIUS_SM,
            fg_color="transparent", hover_color=Theme.BG_HOVER,
            border_width=1, border_color=Theme.BORDER,
            text_color=Theme.TEXT_MUTED, command=self._clear_history,
        )
        self._clear_btn.pack(side="right")

        self._scroll = ctk.CTkScrollableFrame(
            self.body, fg_color="transparent",
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.BORDER_LIGHT,
        )
        self._scroll.pack(fill="both", expand=True)

        self._empty_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        empty_inner = ctk.CTkFrame(self._empty_frame, fg_color="transparent")
        empty_inner.place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(
            empty_inner, text="⏱", font=(Theme.FONT_FAMILY, 40),
            text_color=Theme.TEXT_DISABLED,
        ).pack()
        ctk.CTkLabel(
            empty_inner, text="Nenhuma conversão realizada",
            font=Theme.FONT_BODY, text_color=Theme.TEXT_MUTED,
        ).pack(pady=(12, 4))
        ctk.CTkLabel(
            empty_inner, text="Suas conversões aparecerão aqui",
            font=Theme.FONT_TINY, text_color=Theme.TEXT_DISABLED,
        ).pack()

    def refresh(self) -> None:
        from gui.history_store import load_history
        entries = load_history()

        for w in self._scroll.winfo_children():
            w.destroy()

        if entries:
            self._count_lbl.configure(text=f"{len(entries)} conversão(ões)")
            self._clear_btn.pack(side="right")
            self._empty_frame.pack_forget()
            self._scroll.pack(fill="both", expand=True)
            for entry in entries:
                row = _HistoryRow(self._scroll, entry)
                row.pack(fill="x", pady=(0, 6))
        else:
            self._count_lbl.configure(text="")
            self._clear_btn.pack_forget()
            self._scroll.pack_forget()
            self._empty_frame.pack(fill="both", expand=True)

    def _clear_history(self) -> None:
        from gui.history_store import clear_history
        clear_history()
        self.refresh()


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

class _SettingsSection(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, title: str, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_CARD, corner_radius=Theme.RADIUS_MD,
                         border_width=1, border_color=Theme.BORDER, **kw)
        ctk.CTkLabel(
            self, text=title, font=Theme.FONT_HEADING,
            text_color=Theme.TEXT_PRIMARY,
        ).pack(anchor="w", padx=18, pady=(16, 10))
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="x", padx=18, pady=(0, 16))


class _SettingRow(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, label: str, description: str = "", **kw) -> None:
        super().__init__(master, fg_color="transparent", **kw)
        left = ctk.CTkFrame(self, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            left, text=label, font=Theme.FONT_BODY,
            text_color=Theme.TEXT_PRIMARY, anchor="w",
        ).pack(anchor="w")
        if description:
            ctk.CTkLabel(
                left, text=description, font=Theme.FONT_TINY,
                text_color=Theme.TEXT_MUTED, anchor="w",
            ).pack(anchor="w", pady=(2, 0))
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.pack(side="right")


class SettingsPage(PageBase):
    def __init__(self, master: ctk.CTkFrame, **kw) -> None:
        super().__init__(master, title="Configurações", **kw)
        self._output_dir: Optional[Path] = None
        self._build_content()
        self._load_into_ui()

    def _build_content(self) -> None:
        scroll = ctk.CTkScrollableFrame(
            self.body, fg_color="transparent",
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.BORDER_LIGHT,
        )
        scroll.pack(fill="both", expand=True)

        sec1 = _SettingsSection(scroll, "Aparência")
        sec1.pack(fill="x", pady=(0, 12))

        row_theme = _SettingRow(sec1.content, "Tema", "Aparência visual da interface")
        row_theme.pack(fill="x", pady=(0, 8))
        self._theme_var = ctk.StringVar(value="Escuro")
        ctk.CTkSegmentedButton(
            row_theme.right, values=["Escuro", "Claro", "Sistema"],
            variable=self._theme_var, width=220,
            command=self._on_theme_change,
        ).pack()

        sec2 = _SettingsSection(scroll, "Conversão")
        sec2.pack(fill="x", pady=(0, 12))

        row_quality = _SettingRow(sec2.content, "Qualidade padrão", "Usado na tela de conversão ao abrir")
        row_quality.pack(fill="x", pady=(0, 8))
        self._def_quality = ctk.StringVar(value="Equilibrado")
        ctk.CTkSegmentedButton(
            row_quality.right, values=["Rápido", "Equilibrado", "Alta Qualidade"],
            variable=self._def_quality, width=280,
            command=self._save_settings,
        ).pack()

        row_dir = _SettingRow(sec2.content, "Pasta de saída padrão", "Usada quando não escolher pasta na conversão")
        row_dir.pack(fill="x", pady=(0, 8))
        dir_row = ctk.CTkFrame(row_dir.right, fg_color="transparent")
        dir_row.pack()
        self._dir_lbl = ctk.CTkLabel(
            dir_row, text="Mesmo do original", font=Theme.FONT_SMALL,
            text_color=Theme.TEXT_MUTED,
        )
        self._dir_lbl.pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            dir_row, text="Alterar", width=68, height=28, font=Theme.FONT_SMALL,
            corner_radius=Theme.RADIUS_SM, fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER, command=self._pick_dir,
        ).pack(side="left")

        row_img = _SettingRow(sec2.content, "Extrair imagens (padrão)", "Valor inicial na tela de conversão")
        row_img.pack(fill="x", pady=(0, 8))
        self._extract_img = ctk.BooleanVar(value=True)
        sw = ctk.CTkSwitch(
            row_img.right, text="", variable=self._extract_img,
            width=44, fg_color=Theme.BORDER_LIGHT, progress_color=Theme.PRIMARY,
            command=self._save_settings,
        )
        sw.pack()

        sec3 = _SettingsSection(scroll, "Dados")
        sec3.pack(fill="x", pady=(0, 12))

        row_clear = _SettingRow(sec3.content, "Limpar histórico", "Remove todos os registros de conversões")
        row_clear.pack(fill="x", pady=(0, 8))
        ctk.CTkButton(
            row_clear.right, text="Limpar", width=80, height=30,
            font=Theme.FONT_SMALL, corner_radius=Theme.RADIUS_SM,
            fg_color="transparent", hover_color=Theme.ERROR_DARK,
            border_width=1, border_color=Theme.BORDER,
            text_color=Theme.ERROR, command=self._clear_history,
        ).pack()

        sec4 = _SettingsSection(scroll, "Sobre")
        sec4.pack(fill="x", pady=(0, 12))

        try:
            from gui import __version__ as app_version
        except ImportError:
            app_version = "1.0.0"
        about_data = [
            ("Aplicação", "VIREX - Conversor de Documentos"),
            ("Versão", app_version),
            ("Framework", "CustomTkinter / Python"),
        ]
        for label, value in about_data:
            row = ctk.CTkFrame(sec4.content, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(
                row, text=label, font=Theme.FONT_SMALL,
                text_color=Theme.TEXT_MUTED, anchor="w", width=120,
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=value, font=Theme.FONT_SMALL,
                text_color=Theme.TEXT_SECONDARY, anchor="w",
            ).pack(side="left")

        row_url = _SettingRow(sec4.content, "URL de atualização", "Opcional: URL que retorna a versão (JSON ou texto)")
        row_url.pack(fill="x", pady=(8, 0))
        self._update_url_entry = ctk.CTkEntry(
            row_url.right, width=320, height=28, font=Theme.FONT_SMALL,
            placeholder_text="ex: https://raw.githubusercontent.com/.../version.json",
            fg_color=Theme.BG_INPUT, border_color=Theme.BORDER,
        )
        self._update_url_entry.pack()
        self._update_url_entry.bind("<FocusOut>", self._save_settings)

        row_update = _SettingRow(sec4.content, "Atualização", "Verificar se há nova versão disponível")
        row_update.pack(fill="x", pady=(12, 0))
        self._update_btn = ctk.CTkButton(
            row_update.right, text="Verificar atualizações", width=160, height=30,
            font=Theme.FONT_SMALL, corner_radius=Theme.RADIUS_SM,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_HOVER,
            command=self._check_updates,
        )
        self._update_btn.pack()

    def _load_into_ui(self) -> None:
        try:
            from gui.settings_store import load_settings
            st = load_settings()
            theme_map = {"dark": "Escuro", "light": "Claro", "system": "Sistema"}
            self._theme_var.set(theme_map.get(st.get("theme", "dark"), "Escuro"))
            self._def_quality.set(st.get("default_quality", "Equilibrado"))
            self._extract_img.set(st.get("extract_images", True))
            dd = st.get("default_output_dir")
            if dd:
                self._output_dir = Path(dd)
                disp = str(self._output_dir)
                if len(disp) > 30:
                    disp = "..." + disp[-27:]
                self._dir_lbl.configure(text=disp, text_color=Theme.TEXT_SECONDARY)
            else:
                self._output_dir = None
                self._dir_lbl.configure(text="Mesmo do original", text_color=Theme.TEXT_MUTED)
            url = st.get("update_check_url") or ""
            if hasattr(self, "_update_url_entry"):
                self._update_url_entry.delete(0, "end")
                self._update_url_entry.insert(0, url)
        except Exception:
            pass

    def _save_settings(self, _value: str = "") -> None:
        try:
            from gui.settings_store import load_settings, save_settings
            st = load_settings()
            theme_map = {"Escuro": "dark", "Claro": "light", "Sistema": "system"}
            st["theme"] = theme_map.get(self._theme_var.get(), "dark")
            st["default_quality"] = self._def_quality.get()
            st["extract_images"] = self._extract_img.get()
            st["default_output_dir"] = str(self._output_dir) if self._output_dir else None
            if hasattr(self, "_update_url_entry"):
                u = (self._update_url_entry.get() or "").strip()
                st["update_check_url"] = u if u else None
            save_settings(st)
        except Exception:
            pass

    def _on_theme_change(self, value: str) -> None:
        mode_map = {"Escuro": "dark", "Claro": "light", "Sistema": "system"}
        ctk.set_appearance_mode(mode_map.get(value, "dark"))
        self._save_settings()

    def _pick_dir(self) -> None:
        d = filedialog.askdirectory(title="Pasta de saída padrão")
        if d:
            self._output_dir = Path(d)
            disp = str(self._output_dir)
            if len(disp) > 30:
                disp = "..." + disp[-27:]
            self._dir_lbl.configure(text=disp, text_color=Theme.TEXT_SECONDARY)
            self._save_settings()

    def _clear_history(self) -> None:
        from gui.history_store import clear_history
        clear_history()

    def _check_updates(self) -> None:
        """Verifica atualização em background e mostra resultado em diálogo."""
        try:
            from gui import __version__ as current_version
        except ImportError:
            current_version = "1.0.0"
        self._update_btn.configure(state="disabled", text="Verificando...")

        def do_check() -> None:
            from gui.update_checker import check_update
            from gui.settings_store import load_settings
            url = (load_settings().get("update_check_url") or "").strip() or None
            result = check_update(current_version, url=url)
            self.after(0, lambda: self._show_update_result(result))

        threading.Thread(target=do_check, daemon=True).start()

    def _show_update_result(self, result: dict) -> None:
        self._update_btn.configure(state="normal", text="Verificar atualizações")
        err = result.get("error")
        if err:
            messagebox.showinfo("Verificar atualizações", f"Não foi possível verificar.\n\n{err}", parent=self.winfo_toplevel())
            return
        if result.get("has_update"):
            latest = result.get("latest", "")
            url = result.get("download_url")
            msg = f"Nova versão disponível: {latest}\n\nSua versão: {result.get('current', '')}"
            if url:
                msg += "\n\nDeseja abrir o link para download?"
            if url and messagebox.askyesno("Atualização disponível", msg, parent=self.winfo_toplevel()):
                import webbrowser
                webbrowser.open(url)
        else:
            messagebox.showinfo(
                "Verificar atualizações",
                f"Você está atualizado.\n\nVersão atual: {result.get('current', '')}",
                parent=self.winfo_toplevel(),
            )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT (page container)
# ═══════════════════════════════════════════════════════════════════════════════

class MainContent(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, **kw) -> None:
        super().__init__(master, fg_color=Theme.BG_MAIN, corner_radius=0, **kw)
        self._pages: list[ctk.CTkFrame] = []
        self._current = 0
        self._build()

    def _build(self) -> None:
        self._conversion_page = ConversionPage(self, on_converted=self._on_converted)
        self._history_page = HistoryPage(self)
        self._settings_page = SettingsPage(self)

        self._pages = [
            self._conversion_page,
            self._history_page,
            self._settings_page,
        ]

        for page in (self._conversion_page, self._history_page, self._settings_page):
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._conversion_page.tkraise()

    def show_page(self, index: int) -> None:
        if 0 <= index < len(self._pages):
            self._current = index
            page = self._pages[index]
            page.tkraise()
            if isinstance(page, HistoryPage):
                page.refresh()
            elif isinstance(page, ConversionPage):
                page.main_card.apply_default_settings()

    def _on_converted(self) -> None:
        """Notifica que uma conversão ocorreu para atualizar histórico se visível."""
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class VirexApp(ctk.CTk):
    APP_NAME = "VIREX - Conversor de Documentos"
    WIDTH, HEIGHT = 1160, 780
    MIN_W, MIN_H = 960, 660

    def __init__(self) -> None:
        super().__init__()
        ctk.set_default_color_theme("blue")
        try:
            from gui.settings_store import load_settings
            st = load_settings()
            ctk.set_appearance_mode(st.get("theme", "dark"))
        except Exception:
            ctk.set_appearance_mode("dark")
        self._setup_window()
        self._create_layout()
        # Verificação de atualização ao abrir o aplicativo (em background, após a janela estar visível)
        self.after(800, self._startup_update_check)

    def _startup_update_check(self) -> None:
        """Executa verificação de atualização ao abrir o app; notifica só se houver nova versão."""
        try:
            from gui import __version__ as current_version
        except ImportError:
            current_version = "1.0.0"
        from gui.settings_store import load_settings
        url = (load_settings().get("update_check_url") or "").strip() or None
        if not url:
            return
        def do_check() -> None:
            from gui.update_checker import check_update
            result = check_update(current_version, url=url)
            self.after(0, lambda: self._on_startup_update_result(result))
        threading.Thread(target=do_check, daemon=True).start()

    def _on_startup_update_result(self, result: dict) -> None:
        """Mostra aviso só se houver atualização disponível."""
        if result.get("error") or not result.get("has_update"):
            return
        latest = result.get("latest", "")
        url = result.get("download_url")
        msg = f"Nova versão disponível: {latest}\n\nSua versão: {result.get('current', '')}"
        if url:
            msg += "\n\nDeseja abrir o link para download?"
        if url and messagebox.askyesno("Atualização disponível", msg, parent=self):
            import webbrowser
            webbrowser.open(url)
        elif not url:
            messagebox.showinfo("Atualização disponível", msg, parent=self)

    def _setup_window(self) -> None:
        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.MIN_W, self.MIN_H)
        self.configure(fg_color=Theme.BG_MAIN)
        self.update_idletasks()
        sx, sy = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{(sx - self.WIDTH) // 2}+{(sy - self.HEIGHT) // 2}")
        icon_path = Path(__file__).parent / "assets" / "icon.ico"
        if icon_path.exists():
            self.iconbitmap(str(icon_path))

    def _create_layout(self) -> None:
        self.main_content = MainContent(self)
        self.sidebar = Sidebar(self, on_menu=self._on_menu)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkFrame(self, width=1, fg_color=Theme.BORDER, corner_radius=0).pack(side="left", fill="y")
        self.main_content.pack(side="left", fill="both", expand=True)

    def _on_menu(self, index: int) -> None:
        self.main_content.show_page(index)


ConversoApp = VirexApp


def run() -> int:
    try:
        app = VirexApp()
        app.mainloop()
        return 0
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
