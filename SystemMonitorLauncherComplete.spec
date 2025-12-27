# -*- mode: python ; coding: utf-8 -*-

# 获取当前虚拟环境的Python路径
import sys
import os
venv_python = sys.executable
venv_site_packages = os.path.join(os.path.dirname(venv_python), 'Lib', 'site-packages')

a = Analysis(
    ['backend_launcher.py'],
    pathex=[venv_site_packages],
    binaries=[],
    datas=[
        # 包含后端目录
        ('backend', 'backend'),
        # 包含虚拟环境的Python解释器
        (venv_python, '.'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'websockets',
        'python-multipart',
        'jinja2',
        'requests',
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# 添加虚拟环境中的所有包到binaries
for item in a.binaries:
    if 'site-packages' in item[0]:
        a.binaries.remove(item)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SystemMonitorLauncher',
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