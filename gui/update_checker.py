"""
Verificação de atualização do Converso.
Busca a versão mais recente em uma URL configurável e compara com a versão atual.
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Optional

# URL que retorna a versão mais recente (texto "1.0.0" ou JSON {"version": "1.0.0", "url": "..."}).
# Altere para o seu repositório, por exemplo:
#   https://raw.githubusercontent.com/SEU_USUARIO/Converso-1/main/version.json
UPDATE_CHECK_URL: Optional[str] = None  # Desative deixando None; ou use uma URL real.


def _parse_version(s: str) -> tuple[int, ...]:
    """Converte string de versão (ex: '1.0.2') em tupla (1, 0, 2) para comparação."""
    s = s.strip()
    parts = re.sub(r"[^0-9.]", "", s).split(".") or ["0"]
    return tuple(int(p) if p.isdigit() else 0 for p in parts)


def check_update(current_version: str, url: Optional[str] = None) -> dict:
    """
    Verifica se há atualização disponível.
    Retorna dict com: has_update (bool), current (str), latest (str|None), download_url (str|None), error (str|None).
    """
    url = url or UPDATE_CHECK_URL
    result = {
        "has_update": False,
        "current": current_version,
        "latest": None,
        "download_url": None,
        "error": None,
    }
    if not url or not url.strip():
        result["error"] = "Verificação de atualização não configurada."
        return result
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Converso/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        result["error"] = str(e)
        return result
    latest_str = None
    download_url = None
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            latest_str = data.get("version") or data.get("latest")
            download_url = data.get("url") or data.get("download_url") or data.get("release_url")
        elif isinstance(data, str):
            latest_str = data
    except json.JSONDecodeError:
        latest_str = raw.split("\n")[0].strip() if raw else None
    if not latest_str:
        result["error"] = "Resposta da atualização inválida."
        return result
    result["latest"] = latest_str
    result["download_url"] = download_url
    try:
        cur = _parse_version(current_version)
        lat = _parse_version(latest_str)
        result["has_update"] = lat > cur
    except (ValueError, TypeError):
        result["has_update"] = latest_str != current_version
    return result
