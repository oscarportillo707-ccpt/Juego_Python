import math
import pygame


# ==========================================================
# MODOS DE JUEGO
# ==========================================================
#
# Cada modo tiene su propia dificultad, colores, récord
# y trofeos. Los modos Medio y Avanzado se desbloquean
# ganando el trofeo de ORO en el modo anterior.

ORDEN_MODOS = ["basico", "medio", "avanzado"]

MODOS = {

    "basico": {
        "nombre": "BÁSICO",
        "subtitulo": "Órbita tranquila",
        "estrellas": 1,

        # Colores de las pantallas
        "color": (70, 150, 255),
        "fondo": (15, 30, 65),
        "lineas": (28, 48, 95),

        # Dificultad
        "velocidad_inicial": 3,
        "aumento_velocidad": 0.08,
        "vidas": 3,
        "vidas_maximas": 5,
        "obstaculos_iniciales": 3,
        "obstaculos_maximos": 8,
        "probabilidad_zigzag": 0,

        # Objetos especiales
        "duracion_escudo": 5,
        "duracion_iman": 6,
        "pesos_potenciadores": [35, 18, 17, 17, 13],

        # El jefe aparece desde estos puntos y luego cada 100
        "tiene_jefe": True,
        "puntos_primer_jefe": 300,

        "color_nave": "azul",
        "texto_diamante": "NIVEL MASTER",

        # (modo, trofeo) necesario para desbloquearlo
        "requisito": None,
    },

    "medio": {
        "nombre": "MEDIO",
        "subtitulo": "Cinturón de asteroides",
        "estrellas": 2,

        "color": (175, 95, 255),
        "fondo": (35, 15, 60),
        "lineas": (58, 32, 92),

        "velocidad_inicial": 4,
        "aumento_velocidad": 0.09,
        "vidas": 3,
        "vidas_maximas": 4,
        "obstaculos_iniciales": 4,
        "obstaculos_maximos": 9,
        "probabilidad_zigzag": 0.3,

        "duracion_escudo": 4.5,
        "duracion_iman": 5,
        "pesos_potenciadores": [35, 10, 22, 22, 13],

        "tiene_jefe": True,
        "puntos_primer_jefe": 300,

        "color_nave": "morada",
        "texto_diamante": "NIVEL MASTER",

        "requisito": ("basico", "oro"),
    },

    "avanzado": {
        "nombre": "AVANZADO",
        "subtitulo": "Agujero negro",
        "estrellas": 3,

        "color": (255, 75, 60),
        "fondo": (50, 10, 16),
        "lineas": (82, 26, 32),

        "velocidad_inicial": 4.5,
        "aumento_velocidad": 0.1,
        "vidas": 2,
        "vidas_maximas": 3,
        "obstaculos_iniciales": 4,
        "obstaculos_maximos": 10,
        "probabilidad_zigzag": 0.45,

        "duracion_escudo": 3.5,
        "duracion_iman": 4,
        "pesos_potenciadores": [45, 10, 20, 25, 15],

        "tiene_jefe": True,
        "puntos_primer_jefe": 100,

        "color_nave": "roja",
        "texto_diamante": "NIVEL LEYENDA",

        "requisito": ("medio", "oro"),
    },
}


# ==========================================================
# COLORES DE LA NAVE
# ==========================================================
#
# (clave, nombre, tinte, requisito)
#
# tinte = (tono, saturación, brillo extra)
#   tono: 0 a 1 (0 = rojo, 0.33 = verde, 0.66 = azul...)
#   saturación: None deja la original
#   None = la nave original (azul)
#
# requisito = (modo, trofeo) que hay que ganar, o None

COLORES_NAVE = [
    ("modo", "DEL MODO", None, None),
    ("azul", "AZUL", None, None),
    ("morada", "MORADA", (0.78, None, 0), ("basico", "oro")),
    ("roja", "ROJA", (0.0, None, 0), ("medio", "oro")),
    ("verde", "VERDE", (0.36, None, 0), ("basico", "plata")),
    ("naranja", "NARANJA", (0.07, None, 0.05), ("basico", "diamante")),
    ("dorada", "DORADA", (0.13, 0.8, 0.15), ("medio", "diamante")),
    ("cristal", "CRISTAL", (0.52, 0.25, 0.3), ("avanzado", "diamante")),
]


def datos_color(clave):

    for datos in COLORES_NAVE:

        if datos[0] == clave:
            return datos

    return COLORES_NAVE[0]


def tinte_nave(clave_color, modo):

    # "modo" usa el color propio del modo
    if clave_color == "modo":
        clave_color = MODOS[modo]["color_nave"]

    return datos_color(clave_color)[2]


# ==========================================================
# DESBLOQUEOS
# ==========================================================

def tiene_trofeo(progreso, modo, trofeo):

    return trofeo in progreso["modos"][modo]["trofeos"]


def modo_desbloqueado(progreso, modo):

    requisito = MODOS[modo]["requisito"]

    if requisito is None:
        return True

    return tiene_trofeo(progreso, *requisito)


def color_desbloqueado(progreso, clave):

    requisito = datos_color(clave)[3]

    if requisito is None:
        return True

    return tiene_trofeo(progreso, *requisito)


def texto_requisito(requisito):

    modo, trofeo = requisito

    return f"{trofeo.upper()} en {MODOS[modo]['nombre']}"


# ==========================================================
# DIBUJOS
# ==========================================================

def dibujar_estrella(pantalla, cx, cy, radio, color, relleno=True):

    puntos = []

    for i in range(10):

        angulo = -math.pi / 2 + i * math.pi / 5

        if i % 2 == 0:
            r = radio
        else:
            r = radio * 0.45

        puntos.append((
            cx + math.cos(angulo) * r,
            cy + math.sin(angulo) * r
        ))

    if relleno:
        pygame.draw.polygon(pantalla, color, puntos)
    else:
        pygame.draw.polygon(pantalla, color, puntos, 2)


def dibujar_estrellas(pantalla, cx, cy, cantidad, color, color_vacia, radio=10):

    # Dibuja ★☆☆, ★★☆ o ★★★
    separacion = radio * 2 + 6

    for i in range(3):

        x = cx + (i - 1) * separacion

        if i < cantidad:
            dibujar_estrella(pantalla, x, cy, radio, color)
        else:
            dibujar_estrella(pantalla, x, cy, radio, color_vacia, relleno=False)


def dibujar_candado(pantalla, cx, cy, escala, color):

    grosor = max(2, int(5 * escala))

    # Arco
    pygame.draw.arc(
        pantalla,
        color,
        (cx - 14 * escala, cy - 30 * escala, 28 * escala, 34 * escala),
        0,
        math.pi,
        grosor
    )

    pygame.draw.line(pantalla, color, (cx - 14 * escala + grosor / 2, cy - 13 * escala), (cx - 14 * escala + grosor / 2, cy - 2 * escala), grosor)
    pygame.draw.line(pantalla, color, (cx + 14 * escala - grosor / 2, cy - 13 * escala), (cx + 14 * escala - grosor / 2, cy - 2 * escala), grosor)

    # Cuerpo
    cuerpo = pygame.Rect(0, 0, 40 * escala, 30 * escala)
    cuerpo.center = (cx, cy + 10 * escala)

    pygame.draw.rect(pantalla, color, cuerpo, border_radius=int(6 * escala))

    # Cerradura
    pygame.draw.circle(pantalla, (20, 25, 40), (int(cx), int(cy + 7 * escala)), max(2, int(4 * escala)))
    pygame.draw.line(pantalla, (20, 25, 40), (cx, cy + 7 * escala), (cx, cy + 17 * escala), max(2, int(3 * escala)))


def dibujar_icono_modo(pantalla, modo, cx, cy, tiempo):

    # Un dibujo pequeño que representa cada modo

    if modo == "basico":

        # Planeta azul con anillo
        pygame.draw.ellipse(pantalla, (150, 200, 255), (cx - 38, cy - 8, 76, 16), 3)
        pygame.draw.circle(pantalla, (60, 130, 240), (cx, cy), 22)
        pygame.draw.circle(pantalla, (110, 180, 255), (cx - 7, cy - 7), 8)

        # Parte del anillo que pasa por delante
        pygame.draw.arc(pantalla, (150, 200, 255), (cx - 38, cy - 8, 76, 16), math.pi, 2 * math.pi, 3)

    elif modo == "medio":

        # Nebulosa con asteroides girando
        for i, (radio, color) in enumerate([
            (30, (90, 40, 140)),
            (22, (140, 70, 200)),
            (13, (210, 150, 255)),
        ]):
            pygame.draw.circle(pantalla, color, (cx + i * 2, cy - i), radio)

        for i in range(3):

            angulo = tiempo * 1.5 + i * 2.1

            x = cx + math.cos(angulo) * 36
            y = cy + math.sin(angulo) * 14

            pygame.draw.circle(pantalla, (130, 105, 90), (int(x), int(y)), 6)

    elif modo == "avanzado":

        # Agujero negro con anillo rojo que gira
        for i in range(6):

            angulo = tiempo * 2 + i * math.pi / 3

            x = cx + math.cos(angulo) * 26
            y = cy + math.sin(angulo) * 26

            pygame.draw.circle(pantalla, (255, 120, 40), (int(x), int(y)), 4)

        pygame.draw.circle(pantalla, (255, 70, 40), (cx, cy), 27, 4)
        pygame.draw.circle(pantalla, (200, 40, 30), (cx, cy), 21, 3)
        pygame.draw.circle(pantalla, (5, 0, 5), (cx, cy), 18)
