# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['D:\\projects\\CLGR-UI\\src\\control_panel.py',
                     'D:\\projects\\CLGR-UI\\src\\listbox_panel.py',
                     'D:\\projects\\CLGR-UI\\src\\main_window.py',
                     'D:\\projects\\CLGR-UI\\src\\search_process.py',
                     'D:\\projects\\CLGR-UI\\src\\subprocess_data_receive_thread.py',
                     'D:\\projects\\CLGR-UI\\src\\text_reader.py'],
             binaries=[],
             datas=[(".\\bin\\clgr.exe", ".\\bin\\clgr.exe"), (".\\temp", ".\\temp")],
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
          [],
          exclude_binaries=True,
          name='clgrui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='clgr-ui')
