"""
Persistência das configurações do aplicativo em JSON local (~/.conversor/settings.json).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_SETTINGS_DIR = Path.home() / ".conversor"
_SETTINGS_FILE = _SETTINGS_DIR / "settings.json"

DEFAULT_SETTINGS: dict[str, Any] = {
    "theme": "dark",
    "default_quality": "Equilibrado",
    "default_output_dir": None,
    "extract_images": True,
    "update_check_url": None,  # URL opcional para verificar atualização (ex.: raw GitHub version.json)
}


def _ensure_dir() -> None:
    _SETTINGS_DIR.mkdir(parents=True, exist_ok=True)


def load_settings() -> dict[str, Any]:
    try:
        if _SETTINGS_FILE.exists():
            data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
            out = DEFAULT_SETTINGS.copy()
            for k, v in data.items():
                if k in out:
                    out[k] = v
            return out
    except (json.JSONDecodeError, OSError, TypeError):
        pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict[str, Any]) -> None:
    _ensure_dir()
    to_save = {k: settings.get(k, v) for k, v in DEFAULT_SETTINGS.items()}
    to_save["default_output_dir"] = str(settings["default_output_dir"]) if settings.get("default_output_dir") else None
    to_save["update_check_url"] = (settings.get("update_check_url") or "").strip() or None
    _SETTINGS_FILE.write_text(json.dumps(to_save, ensure_ascii=False, indent=2), encoding="utf-8")
