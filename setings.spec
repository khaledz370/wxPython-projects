# myscript.spec

import os
from pathlib import Path
import sys

data_files = [(str(Path(os.getcwd()) / "path/to/data/file.extension"), ".")]

a = Analysis(['myscript.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=None)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='myscript',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          upx_include=[])

coll = COLLECT(exe,
               zipfig=True,
               upx=True,
               name='myscript')
