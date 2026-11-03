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

        # Moverse por los menús
        "mover": crear_sonido([
            (990, 0.04)
        ], 0.15),

        # Elegir una opción
        "elegir": crear_sonido([
            (660, 0.05), (990, 0.08)
        ], 0.2),

        # Intentar entrar a un modo bloqueado
        "bloqueado": crear_sonido([
            (180, 0.08), (0, 0.03), (150, 0.12)
        ], 0.3),

        # Nuevo modo desbloqueado
        "desbloqueo": crear_sonido([
            (392, 0.1), (523, 0.1), (659, 0.1), (784, 0.1),
            (0, 0.05), (1047, 0.12), (1319, 0.35)
        ], 0.3),

        # Sirena del jefe
        "alerta": crear_sonido([
            (620, 0.22), (820, 0.22), (620, 0.22), (820, 0.22),
            (620, 0.22), (820, 0.22)
        ], 0.22),

        # Disparo del jefe
        "disparo": crear_sonido([
            (900, 0.03), (500, 0.05)
        ], 0.12),

        # Rayo del jefe
        "laser": crear_sonido([
            (220, 0.08), (240, 0.08), (220, 0.08), (240, 0.08), (220, 0.15)
        ], 0.22),

        # Disparo de la nave
        "disparo_nave": crear_sonido([
            (1400, 0.02), (1000, 0.03)
        ], 0.07),

        # Meteorito destruido por una bala
        "meteorito_roto": crear_sonido([
            (300, 0.04), (180, 0.08)
        ], 0.25),

        # Bala que pega en el jefe
        "impacto_jefe": crear_sonido([
            (500, 0.02), (350, 0.03)
        ], 0.12),

        # El jefe se va (explosión)
        "explosion": crear_sonido([
            (160, 0.08), (120, 0.1), (90, 0.12), (60, 0.25)
        ], 0.4),
    }
