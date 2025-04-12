# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['file_namer.py'],
             pathex=['c:\\Users\\adurs\\OneDrive\\Documents\\repos\\TFCSS'],
             binaries=[],
             datas=[],
             hiddenimports=['babel.numbers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'notebook', 'pandas', 'scipy', 'numpy', 'PIL', 
                      'sklearn', 'tensorflow', 'torch', 'jedi', 'sphinx', 'docutils',
                      'IPython', 'ipython', 'pytest', 'sqlite3', 'sqlalchemy', 'django',
                      'flask', 'PySide2', 'PyQt5', 'jupyter', 'jsonschema'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

# Clean collect
a.datas = [x for x in a.datas if not x[0].startswith("tk\\demos")]
a.datas = [x for x in a.datas if not x[0].startswith("tcl\\demos")]
a.datas = [x for x in a.datas if not x[0].startswith("tcl\\encoding")]
a.datas = [x for x in a.datas if not x[0].startswith("tcl\\tzdata")]
a.datas = [x for x in a.datas if not x[0].endswith(".pdb")]

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Canva File Namer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,  # Strip symbols to reduce size
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          uac_admin=False,
          uac_uiaccess=False,
          icon=None,
          # Added options for faster startup
          disable_windowed_traceback=True)