# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for building Bungee Biker macOS app
Usage: pyinstaller build_macos.spec
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'pygame',
        'numpy',
        'src.engine.physics',
        'src.engine.renderer',
        'src.game.game',
        'src.game.level',
        'src.game.objects',
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
    [],
    exclude_binaries=True,
    name='BungeeBiker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BungeeBiker',
)

app = BUNDLE(
    coll,
    name='BungeeBiker.app',
    icon='assets/icon.icns',
    bundle_identifier='com.bungeebiker.game',
    info_plist={
        'CFBundleName': 'Bungee Biker',
        'CFBundleDisplayName': 'Bungee Biker',
        'CFBundleGetInfoString': 'A 1:1 clone of Elasto Mania',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHumanReadableCopyright': '2026 Bungee Biker',
        'NSHighResolutionCapable': True,
    },
)
