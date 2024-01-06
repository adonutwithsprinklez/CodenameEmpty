# -*- mode: python ; coding: utf-8 -*-
import os
import shutil

block_cipher = None


a = Analysis(['src/launchGame.py'],
             pathex=['CodeNameEmpty'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GameLauncher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          windowed=True )

path = 'dist/res/'
if os.path.exists(path):
    shutil.rmtree(path)           # Removes all the subdirectories!

shutil.copytree('src/res/', path)