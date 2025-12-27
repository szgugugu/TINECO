# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['system_monitor.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'psutil', 'requests', 'threading', 'subprocess', 'queue', 'hashlib', 'platform', 'socket', 'time', 'os', 'uuid', 'atexit', 'json'],
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
    name='TINECO SystemMonitor Client',
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
    icon='c:\\Users\\zhifeng.gu.TINECO\\Documents\\trae_projects\\download_web\\system-monitor\\icon.ico',
)
