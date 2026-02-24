# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec para o Converso (GUI).
# Gerar o .exe: pyinstaller converso.spec

import sys

block_cipher = None

# Incluir ícone da janela se existir (opcional)
# Coloque um icon.ico na raiz do projeto ou em gui/assets/
icon_path = None
for candidate in ['gui/assets/icon.ico', 'icon.ico']:
    try:
        if __file__:
            from pathlib import Path
            p = Path(__file__).parent / candidate
            if p.exists():
                icon_path = str(p)
                break
    except Exception:
        pass

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Se você tiver gui/assets/icon.ico, descomente a linha abaixo:
        # ('gui/assets', 'gui/assets'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'pymupdf',
        'docx',
        'pdf2docx',
        'html2text',
        'rapidocr_onnxruntime',
        'pytesseract',
        'gui.update_checker',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Converso',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,   # False = não abrir janela do console (apenas GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
