"""
Armazenamento persistente do histórico de conversões em JSON local.

- Onde: arquivo em disco em ~/.conversor/history.json (ex.: C:\\Users\\<user>\\.conversor\\history.json).
- Memória: longo prazo (persistente). Os dados permanecem após fechar o app e reiniciar o PC.
- O que é salvo: para cada conversão, caminho do arquivo de entrada, formato de saída,
  caminho completo do arquivo salvo (output_file), data/hora, status (sucesso/erro), páginas e imagens.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


_HISTORY_DIR = Path.home() / ".conversor"
_HISTORY_FILE = _HISTORY_DIR / "history.json"
_MAX_ENTRIES = 200


def _ensure_dir() -> None:
    _HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def load_history() -> list[dict]:
    try:
        if _HISTORY_FILE.exists():
            return json.loads(_HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        pass
    return []


def save_history(entries: list[dict]) -> None:
    _ensure_dir()
    trimmed = entries[:_MAX_ENTRIES]
    _HISTORY_FILE.write_text(json.dumps(trimmed, ensure_ascii=False, indent=2), encoding="utf-8")


def add_entry(
    input_file: str,
    output_format: str,
    output_file: str,
    status: str,
    pages: int = 0,
    images: int = 0,
    error: Optional[str] = None,
) -> dict:
    entry = {
        "id": str(uuid.uuid4()),
        "input_file": input_file,
        "input_name": Path(input_file).name,
        "output_format": output_format,
        "output_file": output_file,
        "output_name": Path(output_file).name,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "pages": pages,
        "images": images,
        "error": error,
    }
    entries = load_history()
    entries.insert(0, entry)
    save_history(entries)
    return entry


def clear_history() -> None:
    save_history([])
