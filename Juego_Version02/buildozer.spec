# ==========================================================
# CONFIGURACIÓN PARA CREAR EL APK (ANDROID) CON BUILDOZER
# ==========================================================
#
# Buildozer solo funciona en Linux (WSL, Ubuntu o Google Colab).
#
# Para empaquetar, desde esta carpeta:
#
#     buildozer android debug
#
# El .apk queda en la carpeta "bin".
#
# (Expedicion33.spec es otra cosa: es para el .exe de Windows)

[app]

# Nombre que se ve debajo del icono en el celular
title = Expedicion 33

# Identificador único de la app (sin espacios ni tildes)
package.name = expedicion33
package.domain = org.oscarportillo

# Carpeta del código (esta misma) y el archivo principal es main.py
source.dir = .

# Tipos de archivo que van dentro del APK
source.include_exts = py,png,mp3,wav,ogg,json

# Carpetas que NO van dentro del APK
source.exclude_dirs = build,dist,bin,__pycache__,.vs,.buildozer

# Archivos que NO van dentro del APK:
# - el .spec y el .ico son solo para el .exe de Windows
# - progreso.json es tu récord personal: el APK empieza de cero
source.exclude_patterns = *.spec,icono.ico,progreso.json,buildozer.spec

version = 1.0

# Librerías que necesita el juego
#
# Python va fijo en 3.10: la receta de pygame para Android
# (pygame 2.1.0) no compila con Python 3.11 o más nuevo
# (error: 'longintrepr.h' file not found).
# python3 y hostpython3 deben ser la misma versión.
requirements = python3==3.10.14,hostpython3==3.10.14,pygame

# Icono de la app
icon.filename = %(source.dir)s/icono.png

# La ventana del juego es vertical (600 x 700)
orientation = portrait

# Pantalla completa (sin barra de notificaciones)
fullscreen = 1


# ----------------------------------------------------------
# ANDROID
# ----------------------------------------------------------

# Versión de Android para la que se compila (Google Play pide 35)
android.api = 35

# Android mínimo donde se puede instalar (Android 7.0)
android.minapi = 21
# Android 5.0+; el lienzo se escala con pygame.SCALED en celulares y tablets.

# Procesadores: celulares modernos (64 bits) y viejos (32 bits)
android.archs = arm64-v8a, armeabi-v7a, x86_64, x86
# ARM cubre dispositivos reales; x86 cubre tablets/emuladores antiguos.

# Aceptar licencias del SDK sin preguntar
android.accept_sdk_license = True

# Python-for-android usa SDL2 para pygame
p4a.bootstrap = sdl2


[buildozer]

# 2 = muestra todo lo que hace (útil si algo falla)
log_level = 2

warn_on_root = 1
