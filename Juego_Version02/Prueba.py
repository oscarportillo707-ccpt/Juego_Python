import math
import random
import sys

import pygame


# ==========================================================
# PANTALLA DE INICIO (independiente del juego)
# Solo para visualizar cómo se ve. No necesita ningún otro
# módulo ni imágenes: todo se dibuja con código.
# ==========================================================

pygame.init()

ANCHO = 600
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pantalla de inicio")

reloj = pygame.time.Clock()
FPS = 60


# ==========================================================
# COLORES
# ==========================================================

MORADO = (35, 20, 55)
MORADO_LINEAS = (55, 38, 80)
MORADO_MARCO = (95, 75, 135)
MORADO_APAGADO = (140, 120, 170)
NARANJA = (255, 150, 30)
NARANJA_SOMBRA = (150, 70, 0)
CREMA = (255, 235, 190)


# ==========================================================
# FUENTES
# ==========================================================

fuente_titulo = pygame.font.Font(None, 170)
fuente = pygame.font.Font(None, 48)
fuente_pequena = pygame.font.Font(None, 28)


# ==========================================================
# FUNCIONES DE DIBUJO
# ==========================================================

def dibujar_corazon(x, y, tam, color):

    # Un corazón se forma con dos círculos y un triángulo
    r = tam // 4

    pygame.draw.circle(pantalla, color, (x + r, y + r), r)
    pygame.draw.circle(pantalla, color, (x + 3 * r, y + r), r)

    pygame.draw.polygon(
        pantalla,
        color,
        [
            (x, y + int(r * 1.3)),
            (x + 4 * r, y + int(r * 1.3)),
            (x + 2 * r, y + 4 * r)
        ]
    )


def dibujar_meteorito(x, y, radio):

    centro = (int(x), int(y))

    pygame.draw.circle(pantalla, (110, 90, 75), centro, radio)
    pygame.draw.circle(pantalla, (60, 45, 38), centro, radio, 3)

    # Cráteres
    pygame.draw.circle(
        pantalla,
        (75, 58, 48),
        (int(x + radio * 0.3), int(y - radio * 0.3)),
        int(radio * 0.28)
    )

    pygame.draw.circle(
        pantalla,
        (75, 58, 48),
        (int(x - radio * 0.35), int(y + radio * 0.3)),
        int(radio * 0.35)
    )


def dibujar_nave(x, y, tiempo):

    # x, y = esquina superior izquierda de una nave de 60x70
    cx = x + 30

    # Llama del motor (parpadea)
    llama = 10 + math.sin(tiempo * 0.3) * 6

    pygame.draw.polygon(pantalla, (255, 170, 40), [
        (cx - 7, y + 54), (cx, y + 54 + llama + 8), (cx + 7, y + 54)
    ])

    # Alas
    pygame.draw.polygon(pantalla, (20, 90, 200), [
        (x + 1, y + 58), (cx - 11, y + 26), (cx - 11, y + 52)
    ])

    pygame.draw.polygon(pantalla, (20, 90, 200), [
        (x + 59, y + 58), (cx + 11, y + 26), (cx + 11, y + 52)
    ])

    # Cuerpo
    pygame.draw.polygon(pantalla, (30, 130, 255), [
        (cx, y + 1), (cx + 15, y + 28), (cx + 11, y + 56),
        (cx - 11, y + 56), (cx - 15, y + 28)
    ])

    # Cabina
    pygame.draw.ellipse(
        pantalla,
        (170, 230, 255),
        (cx - 6, y + 17, 12, 20)
    )


# ==========================================================
# METEORITOS DE ADORNO
# ==========================================================

meteoritos = []

for i in range(4):

    meteoritos.append({
        "x": random.randint(40, ANCHO - 40),
        "y": random.randint(-300, ALTO),
        "radio": random.randint(18, 26),
        "vel": random.uniform(1.5, 3)
    })


# ==========================================================
# BUCLE PRINCIPAL
# ==========================================================

# Opción seleccionada: 0 = SÍ, 1 = NO
opcion = 0

tiempo = 0

resultado = None

ejecutando = True

while ejecutando:

    tiempo += 1

    # ======================================================
    # EVENTOS
    # ======================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            # Cambiar de opción
            if evento.key in (
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_a,
                pygame.K_d,
                pygame.K_w,
                pygame.K_s
            ):
                opcion = 1 - opcion

            # Confirmar
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                resultado = "SI" if opcion == 0 else "NO"
                ejecutando = False

            # Salir
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # ======================================================
    # FONDO
    # ======================================================

    pantalla.fill(MORADO)

    # Cuadrícula
    for x in range(0, ANCHO, 50):
        pygame.draw.line(pantalla, MORADO_LINEAS, (x, 0), (x, ALTO))

    for y in range(0, ALTO, 50):
        pygame.draw.line(pantalla, MORADO_LINEAS, (0, y), (ANCHO, y))

    # Meteoritos cayendo
    for m in meteoritos:

        m["y"] += m["vel"]

        if m["y"] > ALTO + 40:
            m["y"] = random.randint(-200, -50)
            m["x"] = random.randint(40, ANCHO - 40)

        dibujar_meteorito(m["x"], m["y"], m["radio"])

    # Nave de adorno
    dibujar_nave(ANCHO // 2 - 30, ALTO - 150, tiempo)

    # Marco redondeado
    marco = pygame.Rect(30, 30, ANCHO - 60, ALTO - 60)

    pygame.draw.rect(
        pantalla,
        MORADO_MARCO,
        marco,
        4,
        border_radius=30
    )

    # ======================================================
    # PARTE SUPERIOR
    # ======================================================

    texto_nombre = fuente_pequena.render(
        "JUEGO DE MONEDAS",
        True,
        CREMA
    )

    pantalla.blit(texto_nombre, (60, 60))

    # Corazones (las 3 vidas del juego)
    for i in range(3):

        dibujar_corazon(
            ANCHO - 60 - 32 - i * 42,
            58,
            32,
            NARANJA
        )

    # ======================================================
    # TÍTULO
    # ======================================================

    sombra = fuente_titulo.render("START", True, NARANJA_SOMBRA)
    titulo = fuente_titulo.render("START", True, NARANJA)

    rect_titulo = titulo.get_rect(center=(ANCHO // 2, 230))

    pantalla.blit(sombra, rect_titulo.move(5, 5))
    pantalla.blit(titulo, rect_titulo)

    texto_sub = fuente_pequena.render(
        "ESQUIVA LOS METEORITOS Y RECOGE MONEDAS",
        True,
        CREMA
    )

    pantalla.blit(
        texto_sub,
        texto_sub.get_rect(center=(ANCHO // 2, 320))
    )

    # ======================================================
    # PREGUNTA Y OPCIONES
    # ======================================================

    texto_listo = fuente.render("¿ESTÁS LISTO?", True, CREMA)

    pantalla.blit(
        texto_listo,
        texto_listo.get_rect(center=(ANCHO // 2, 410))
    )

    opciones = ["SÍ", "NO"]

    posiciones = [ANCHO // 2 - 100, ANCHO // 2 + 100]

    for i in range(2):

        if i == opcion:
            color = CREMA
        else:
            color = MORADO_APAGADO

        texto = fuente.render(opciones[i], True, color)

        rect = texto.get_rect(center=(posiciones[i], 480))

        pantalla.blit(texto, rect)

        # Triángulo que señala la opción elegida
        if i == opcion:

            pygame.draw.polygon(
                pantalla,
                NARANJA,
                [
                    (rect.right + 28, rect.centery - 10),
                    (rect.right + 10, rect.centery),
                    (rect.right + 28, rect.centery + 10)
                ]
            )

    texto_ayuda = fuente_pequena.render(
        "Flechas para elegir   -   ENTER para confirmar",
        True,
        MORADO_APAGADO
    )

    pantalla.blit(
        texto_ayuda,
        texto_ayuda.get_rect(center=(ANCHO // 2, ALTO - 60))
    )

    # ======================================================
    # ACTUALIZAR PANTALLA
    # ======================================================

    pygame.display.flip()

    reloj.tick(FPS)


# ==========================================================
# CERRAR
# ==========================================================

if resultado == "SI":
    print("Elegiste SÍ: aquí empezaría el juego.")

elif resultado == "NO":
    print("Elegiste NO: aquí se cerraría el juego.")

pygame.quit()

sys.exit()