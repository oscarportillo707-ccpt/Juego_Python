import pygame
import os


# Ubicación de la carpeta del proyecto
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# Carpeta donde estarán las imágenes
CARPETA_IMAGENES = os.path.join(
    BASE_DIR,
    "imagenes"
)


def cargar_imagen(nombre, tamaño=None):

    # Crear la ruta completa
    ruta = os.path.join(
        CARPETA_IMAGENES,
        nombre
    )

    # Cargar imagen
    imagen = pygame.image.load(ruta).convert_alpha()

    # Cambiar tamaño si se especifica
    if tamaño is not None:
        imagen = pygame.transform.scale(
            imagen,
            tamaño
        )

    return imagen