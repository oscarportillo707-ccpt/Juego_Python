import os
import json
import math
import pygame


# ==========================================================
# ARCHIVO DONDE SE GUARDA EL PROGRESO
# ==========================================================

ARCHIVO_PROGRESO = os.path.join(
    os.path.dirname(__file__),
    "progreso.json"
)


# ==========================================================
# TROFEOS
# ==========================================================

# (clave, nombre, puntos necesarios, color principal, color sombra)
TROFEOS = [
    ("bronce", "BRONCE", 125, (205, 127, 50), (120, 70, 25)),
    ("plata", "PLATA", 225, (200, 205, 215), (110, 115, 130)),
    ("oro", "ORO", 350, (255, 205, 40), (160, 110, 0)),
    ("diamante", "DIAMANTE", 450, (120, 225, 255), (35, 105, 170)),
]

COLOR_BLOQUEADO = (55, 62, 85)
COLOR_BLOQUEADO_SOMBRA = (35, 40, 60)


# ==========================================================
# CARGAR Y GUARDAR
# ==========================================================

def cargar_progreso():

    # Si el archivo no existe o está dañado, empezamos de cero
    progreso = {
        "record": 0,
        "trofeos": []
    }

    try:

        with open(ARCHIVO_PROGRESO, "r", encoding="utf-8") as archivo:

            datos = json.load(archivo)

        progreso["record"] = int(datos.get("record", 0))
        progreso["trofeos"] = list(datos.get("trofeos", []))

    except (OSError, ValueError):
        pass

    return progreso


def guardar_progreso(progreso):

    try:

        with open(ARCHIVO_PROGRESO, "w", encoding="utf-8") as archivo:

            json.dump(progreso, archivo, indent=4)

    except OSError:
        pass


# ==========================================================
# DIBUJAR UN TROFEO
# ==========================================================

def dibujar_trofeo(pantalla, cx, cy, escala, color, sombra, brillo=True):

    # cx, cy = centro del trofeo
    # escala = 1 equivale a un trofeo de unos 60x80 píxeles

    def p(x, y):
        return (int(cx + x * escala), int(cy + y * escala))

    grosor = max(2, int(5 * escala))

    # Asas
    pygame.draw.circle(pantalla, sombra, p(-24, -18), int(12 * escala), grosor)
    pygame.draw.circle(pantalla, sombra, p(24, -18), int(12 * escala), grosor)

    # Copa
    pygame.draw.polygon(pantalla, color, [
        p(-26, -38), p(26, -38), p(22, -14),
        p(12, 2), p(-12, 2), p(-22, -14)
    ])

    # Borde de la copa
    pygame.draw.rect(
        pantalla,
        sombra,
        (*p(-28, -42), int(56 * escala), max(3, int(6 * escala))),
        border_radius=max(1, int(3 * escala))
    )

    # Tallo
    pygame.draw.polygon(pantalla, sombra, [
        p(-5, 2), p(5, 2), p(7, 20), p(-7, 20)
    ])

    # Base
    pygame.draw.rect(
        pantalla,
        color,
        (*p(-18, 20), int(36 * escala), int(9 * escala)),
        border_radius=max(1, int(2 * escala))
    )

    pygame.draw.rect(
        pantalla,
        sombra,
        (*p(-24, 29), int(48 * escala), int(10 * escala)),
        border_radius=max(1, int(3 * escala))
    )

    # Reflejo
    if brillo:

        pygame.draw.polygon(pantalla, (255, 255, 255), [
            p(-17, -34), p(-11, -34), p(-14, -12), p(-18, -16)
        ])

        # Estrella en la copa
        estrella = [
            p(0, -31), p(3, -24), p(10, -24), p(4, -19),
            p(6, -12), p(0, -16), p(-6, -12), p(-4, -19),
            p(-10, -24), p(-3, -24)
        ]

        pygame.draw.polygon(pantalla, sombra, estrella)


def dibujar_trofeo_diamante(pantalla, cx, cy, escala):

    # Trofeo especial: copa de cristal con un diamante,
    # laureles y destellos que brillan.

    def p(x, y):
        return (int(cx + x * escala), int(cy + y * escala))

    tiempo = pygame.time.get_ticks() / 1000

    CLARO = (185, 245, 255)
    MEDIO = (110, 210, 250)
    OSCURO = (35, 105, 170)
    MARINO = (20, 45, 95)
    BLANCO = (255, 255, 255)
    LAUREL = (120, 230, 200)

    grosor = max(2, int(4 * escala))

    # Laureles a los lados
    for lado in (-1, 1):

        for i in range(5):

            x = lado * (30 + i * 2)
            y = 18 - i * 11

            hoja = pygame.Rect(0, 0, max(3, int(12 * escala)), max(2, int(6 * escala)))
            hoja.center = p(x, y)

            pygame.draw.ellipse(pantalla, LAUREL, hoja)

    # Asas
    pygame.draw.circle(pantalla, OSCURO, p(-25, -20), int(12 * escala), grosor)
    pygame.draw.circle(pantalla, OSCURO, p(25, -20), int(12 * escala), grosor)

    # Copa en dos tonos (efecto de cristal)
    pygame.draw.polygon(pantalla, MEDIO, [
        p(-27, -40), p(27, -40), p(23, -14),
        p(12, 4), p(-12, 4), p(-23, -14)
    ])

    pygame.draw.polygon(pantalla, CLARO, [
        p(-27, -40), p(0, -40), p(0, 4),
        p(-12, 4), p(-23, -14)
    ])

    # Borde de la copa
    pygame.draw.rect(
        pantalla,
        OSCURO,
        (*p(-30, -45), int(60 * escala), max(3, int(6 * escala))),
        border_radius=max(1, int(3 * escala))
    )

    # Diamante en el centro de la copa
    pygame.draw.polygon(pantalla, BLANCO, [
        p(-8, -30), p(8, -30), p(13, -24), p(0, -8), p(-13, -24)
    ])

    pygame.draw.polygon(pantalla, (150, 235, 255), [
        p(-13, -24), p(13, -24), p(0, -8)
    ])

    pygame.draw.polygon(pantalla, MEDIO, [
        p(0, -24), p(13, -24), p(0, -8)
    ])

    pygame.draw.polygon(pantalla, OSCURO, [
        p(-8, -30), p(8, -30), p(13, -24), p(0, -8), p(-13, -24)
    ], max(1, int(1.5 * escala)))

    pygame.draw.line(pantalla, OSCURO, p(-13, -24), p(13, -24), max(1, int(escala)))
    pygame.draw.line(pantalla, OSCURO, p(-4, -30), p(-6, -24), max(1, int(escala)))
    pygame.draw.line(pantalla, OSCURO, p(4, -30), p(6, -24), max(1, int(escala)))

    # Tallo
    pygame.draw.polygon(pantalla, OSCURO, [
        p(-5, 4), p(5, 4), p(8, 20), p(-8, 20)
    ])

    # Base de tres escalones
    pygame.draw.rect(
        pantalla, MEDIO,
        (*p(-17, 20), int(34 * escala), int(7 * escala)),
        border_radius=max(1, int(2 * escala))
    )

    pygame.draw.rect(
        pantalla, MARINO,
        (*p(-24, 27), int(48 * escala), int(12 * escala)),
        border_radius=max(1, int(3 * escala))
    )

    pygame.draw.rect(
        pantalla, MEDIO,
        (*p(-24, 27), int(48 * escala), int(12 * escala)),
        max(1, int(1.5 * escala)),
        border_radius=max(1, int(3 * escala))
    )

    # Gemas pequeñas en la base
    for x in (-12, 0, 12):

        pygame.draw.circle(pantalla, CLARO, p(x, 33), max(1, int(2.5 * escala)))

    # Reflejo
    pygame.draw.polygon(pantalla, BLANCO, [
        p(-20, -36), p(-15, -36), p(-17, -16), p(-21, -20)
    ])

    # Destellos que aparecen y desaparecen
    destellos = [(-34, -44, 0), (36, -36, 1.7), (-38, 6, 3.1), (34, 14, 4.4)]

    for x, y, fase in destellos:

        tam = (math.sin(tiempo * 4 + fase) + 1) / 2 * 7 * escala

        if tam < 1:
            continue

        sx, sy = p(x, y)

        pygame.draw.polygon(pantalla, BLANCO, [
            (sx, sy - tam), (sx + tam * 0.3, sy - tam * 0.3),
            (sx + tam, sy), (sx + tam * 0.3, sy + tam * 0.3),
            (sx, sy + tam), (sx - tam * 0.3, sy + tam * 0.3),
            (sx - tam, sy), (sx - tam * 0.3, sy - tam * 0.3)
        ])


def dibujar_trofeo_clave(pantalla, clave, cx, cy, escala):

    # Dibuja el trofeo que corresponde a la clave
    if clave == "diamante":

        dibujar_trofeo_diamante(pantalla, cx, cy, escala)
        return

    for datos in TROFEOS:

        if datos[0] == clave:

            dibujar_trofeo(pantalla, cx, cy, escala, datos[3], datos[4])


def dibujar_coleccion(pantalla, cx, cy, escala, trofeos_ganados, fuente, separacion=None):

    # Dibuja todos los trofeos en fila.
    # Los que no se han ganado aparecen apagados.

    # Mínimo 95 píxeles para que no se encimen los textos
    if separacion is None:
        separacion = max(95, int(95 * escala))

    # Para que la fila quede centrada
    mitad = (len(TROFEOS) - 1) / 2

    for i, (clave, nombre, puntos, color, sombra) in enumerate(TROFEOS):

        x = int(cx + (i - mitad) * separacion)

        if clave in trofeos_ganados:

            dibujar_trofeo_clave(pantalla, clave, x, cy, escala)
            color_texto = color

        else:

            dibujar_trofeo(
                pantalla, x, cy, escala,
                COLOR_BLOQUEADO, COLOR_BLOQUEADO_SOMBRA,
                brillo=False
            )
            color_texto = (120, 145, 190)

        # Sin fuente solo se dibujan los trofeos
        if fuente is None:
            continue

        texto = fuente.render(f"{puntos} pts", True, color_texto)

        pantalla.blit(
            texto,
            texto.get_rect(center=(x, cy + int(52 * escala)))
        )
