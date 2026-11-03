import os
import sys


# ==========================================================
# RUTAS DE LOS ARCHIVOS DEL JUEGO
# ==========================================================
#
# El juego puede correr de dos formas:
#
# 1) Normal, con Python (python main.py)
# 2) Empaquetado como .exe (PyInstaller)
#
# En el .exe los archivos (imágenes, sonidos) se desempacan
# en una carpeta temporal, y esa carpeta se borra al cerrar.
# Por eso el progreso se guarda en otro lugar.

NOMBRE_JUEGO = "Expedicion33"


def esta_empaquetado():

    return getattr(sys, "frozen", False)


def ruta_recurso(*partes):

    # Imágenes y sonidos que vienen con el juego (solo lectura)
    if esta_empaquetado():
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, *partes)


def carpeta_datos():

    # Carpeta donde se guarda el progreso (se puede escribir)
    #
    # - Con Python: la misma carpeta del juego
    # - En el .exe: C:\Users\<usuario>\AppData\Roaming\Expedicion33
    if esta_empaquetado():

        base = os.environ.get("APPDATA") or os.path.expanduser("~")

        carpeta = os.path.join(base, NOMBRE_JUEGO)

    else:
        carpeta = os.path.dirname(os.path.abspath(__file__))

    os.makedirs(carpeta, exist_ok=True)

    return carpeta


def ruta_datos(*partes):

    return os.path.join(carpeta_datos(), *partes)
