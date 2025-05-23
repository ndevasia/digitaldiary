# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('window/templates', 'templates'), ('window/static', 'static'), ('../lib', 'lib'), ('../frontend', 'frontend'), ('../backend', 'backend'), ('../recordings', 'recordings'), ('../screenshots', 'screenshots'), ('../audio', 'audio'), ('C:\\Users\\ndevasia\\Miniconda3\\lib\\site-packages\\imageio_ffmpeg', 'imageio_ffmpeg')]
binaries = []
hiddenimports = ['boto3', 'flask_cors', 'pyautogui', 'cv2', 'numpy', 'moviepy', 'PIL', 'sounddevice', 'soundfile', 'PyQt5', 'imageio_ffmpeg', 'imageio', 'imageio_ffmpeg.binaries']
tmp_ret = collect_all('moviepy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('imageio')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('imageio_ffmpeg')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


block_cipher = None


a = Analysis(
    ['window\\app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
