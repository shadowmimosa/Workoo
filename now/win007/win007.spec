# -*- mode: python ; coding: utf-8 -*-

#import distutils
#if distutils.distutils_path.endswith('__init__.py'):
#    distutils.distutils_path = os.path.dirname(distutils.distutils_path)

block_cipher = pyi_crypto.PyiBlockCipher(key='Shadow@Win0070&04')

a = Analysis(
    ['main.py'],
    pathex=[
        'C:\\Users\\ShadowMimosa\\Documents\\Repos\\Workoo\\now\\win007'
    ],
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas, [],
          name='win007',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='icon.ico')
