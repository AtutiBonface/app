# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'xdm.py', 'settings.py', 'main_application.py', 'progress_manager.py', 'file_manager.py', 'network_manager.py','multi_file_window.py' ,'progress.py', 'app_utils.py','add_link.py', 'about.py', 'database.py', 'file_ui.py', 'file_actions.py'],
    pathex=['xe-logos', 'images'],
    binaries=[],
    datas=[
        ('xe-logos/*', 'xe-logos'),
        ('images/*', 'images')
    ],
    hiddenimports=[],
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
    name='blackjuice',
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
    icon=['xe-logos\\main.ico'],
    onefile=False
)
