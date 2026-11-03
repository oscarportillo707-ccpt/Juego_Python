# -*- mode: python ; coding: utf-8 -*-
#
# Configuración para crear Expedicion33.exe con PyInstaller.
#
# Para empaquetar, desde esta carpeta:
#
#     python -m PyInstaller Expedicion33.spec
#
# El .exe queda en la carpeta "dist".


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],

    # Archivos que van dentro del .exe: (archivo, carpeta destino)
    datas=[
        ('jugador.png', '.'),
        ('meteorito.png', '.'),
        ('icono.png', '.'),
        ('sonidos', 'sonidos'),
    ],

    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# Un solo archivo, sin ventana negra de consola
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Expedicion33',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

    # Icono del .exe (la nave azul en órbita)
    icon='icono.ico',
)
