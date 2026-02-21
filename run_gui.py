#!/usr/bin/env python
"""
Script de entrada para executar a interface gráfica do Converso.

Uso:
    python run_gui.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gui.app import run

if __name__ == "__main__":
    sys.exit(run())
