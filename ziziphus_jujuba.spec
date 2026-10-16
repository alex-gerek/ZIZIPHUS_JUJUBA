# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

block_cipher = None

BASE_DIR = Path.cwd()

datas = [
    (str(BASE_DIR / 'data' / 'database' / 'ziziphus_jujuba.db'), 'data/database'),
    (str(BASE_DIR / 'data' / 'historical_events' / 'events_2013_2014.json'), 'data/historical_events'),
    (str(BASE_DIR / 'app' / 'templates'), 'app/templates'),
    (str(BASE_DIR / 'app' / 'static'), 'app/static'),
    (str(BASE_DIR / 'exports'), 'exports'),
]

hiddenimports = [
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespans',
    'uvicorn.lifespans.on',
    'uvicorn.lifespans.off',
    'fastapi',
    'fastapi.staticfiles',
    'fastapi.templating',
    'jinja2',
    'sqlite3',
    'pandas',
    'numpy',
    'scipy',
    'scipy.special',
    'scipy.special.cython_special',
    'sklearn',
    'sklearn.utils._typedefs',
    'sklearn.neighbors._typedefs',
    'networkx',
    'pydantic',
    'pydantic_core',
    'dateutil',
    'dateutil.parser',
]

a = Analysis(
    ['run_app.py'],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'tkinter', 'IPython', 'notebook', 'pytest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

icon_path = str(BASE_DIR / 'app' / 'static' / 'img' / 'ziziphus_icon.ico')
if not os.path.exists(icon_path):
    icon_path = None

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZiziphusJujuba',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='ZiziphusJujuba',
)
