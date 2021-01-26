# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:/Users/HP/Desktop/DATA/Hadef-employee-manager/index.py'],
             pathex=['C:\\Users\\HP\\Desktop\\DATA\\Hadef-employee-manager'],
             binaries=[],
             datas=[('C:/Users/HP/Desktop/DATA/Hadef-employee-manager/src', 'src/'), ('C:/Users/HP/Desktop/DATA/Hadef-employee-manager/ui', 'ui/'), ('C:/Users/HP/Desktop/DATA/Hadef-employee-manager/i.json', '.')],
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
          name='index',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
