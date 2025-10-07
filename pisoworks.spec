# -*- mode: python ; coding: utf-8 -*-
# pisoworks.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os

# Include all modules under your package
hidden_imports = (
    collect_submodules('pisoworks') +
    collect_submodules('qt_material_icons') +
    collect_submodules('qt_material_icons.resources')
)

datas = (
    collect_data_files('pisoworks.assets') +
    collect_data_files('pisoworks.styles') + 
     [('VERSION', '.')]
)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas = datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PiSoWorks',
    icon='pisoworks/assets/app_icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
