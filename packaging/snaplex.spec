# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path


project_root = Path(SPECPATH).parent
package_variant = os.environ.get("SNAPLEX_PACKAGE_VARIANT", "base").strip().lower() or "base"

hidden_imports = [
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "snaplex.providers.deepl",
    "snaplex.providers.fake",
    "snaplex.providers.libretranslate",
    "snaplex.providers.openai",
    "snaplex.services.capture_service",
    "snaplex.services.ocr_service",
    "snaplex.storage.config",
    "snaplex.storage.history",
    "snaplex.ui.app_shell",
]

excluded_modules = []
if package_variant in {"capture", "full"}:
    hidden_imports.extend(["mss", "mss.tools"])
else:
    excluded_modules.extend(["mss", "mss.tools"])

if package_variant in {"ocr", "full"}:
    hidden_imports.append("paddleocr")
else:
    excluded_modules.extend(["paddle", "paddleocr"])

block_cipher = None

a = Analysis(
    [str(project_root / "snaplex" / "__main__.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SnapLex",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="SnapLex",
)
