import math
import array
import pygame


# ==========================================================
# SONIDOS GENERADOS POR CÓDIGO
# ==========================================================
#
# Para no depender de más archivos .mp3, estos sonidos
# se crean con ondas simples.


def crear_sonido(notas, volumen=0.4):

    # notas = lista de (frecuencia, duración en segundos)
    # Una frecuencia de 0 es un silencio.

    frecuencia_mezcla, formato, canales = pygame.mixer.get_init()

    muestras = array.array("h")

    for frecuencia, duracion in notas:

        total = int(frecuencia_mezcla * duracion)

        for i in range(total):

            if frecuencia == 0:
                valor = 0

            else:

                # Onda cuadrada suave (estilo arcade)
                t = i / frecuencia_mezcla
                onda = math.sin(2 * math.pi * frecuencia * t)
                onda = 0.6 * onda + 0.4 * (1 if onda >= 0 else -1)

                # Desvanecer al final de cada nota
                envolvente = 1 - (i / total)

                valor = int(onda * envolvente * volumen * 32767)

            for c in range(canales):
                muestras.append(valor)

    return pygame.mixer.Sound(buffer=muestras.tobytes())


def cargar_sonidos_extra():

    return {
        # Notas descendentes y tristes
        "game_over": crear_sonido([
            (523, 0.18), (392, 0.18), (330, 0.18), (262, 0.45)
        ], 0.35),

        # Escala rápida hacia arriba
        "potenciador": crear_sonido([
            (660, 0.06), (880, 0.06), (1100, 0.1)
        ], 0.25),

        # Fanfarria corta
        "nivel": crear_sonido([
            (523, 0.1), (659, 0.1), (784, 0.18)
        ], 0.3),

        # Fanfarria larga para los trofeos
        "trofeo": crear_sonido([
            (523, 0.12), (659, 0.12), (784, 0.12),
            (1047, 0.2), (0, 0.05), (784, 0.1), (1047, 0.4)
        ], 0.35),

        # Golpe absorbido por el escudo
        "escudo": crear_sonido([
            (300, 0.05), (200, 0.1)
        ], 0.3),

        # Pausa
        "pausa": crear_sonido([
            (880, 0.05), (0, 0.03), (660, 0.08)
        ], 0.2),
    }
