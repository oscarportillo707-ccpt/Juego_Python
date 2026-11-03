import os
import math
import wave
import array
import random

from rutas import ruta_recurso, ruta_datos


# ==========================================================
# MÚSICA DE CADA MODO
# ==========================================================
#
# El modo Básico usa la música original (mp3).
# Los modos Medio y Avanzado usan canciones creadas por
# código. Ya vienen guardadas como .wav en la carpeta
# "sonidos". Si faltan, se generan una vez en la carpeta
# de datos (ver rutas.py) y luego cargan al instante.

FRECUENCIA = 22050

CARPETA_SONIDOS = ruta_recurso("sonidos")

ARCHIVOS = {
    "basico": "Ambientacion_Jueguito.mp3",
    "medio": "musica_medio_v1.wav",
    "avanzado": "musica_avanzado_v1.wav",
}


def frecuencia_nota(midi):

    # 69 = La (440 Hz)
    return 440 * 2 ** ((midi - 69) / 12)


# ==========================================================
# INSTRUMENTOS
# ==========================================================

def agregar_nota(buffer, inicio, duracion, midi, volumen, forma="seno", caida=4):

    frecuencia = frecuencia_nota(midi)

    primera = int(inicio * FRECUENCIA)
    total = int(duracion * FRECUENCIA)

    for i in range(total):

        posicion = primera + i

        if posicion >= len(buffer):
            break

        t = i / FRECUENCIA
        fase = (frecuencia * t) % 1

        if forma == "seno":
            onda = math.sin(2 * math.pi * fase)

        elif forma == "cuadrada":
            onda = 0.7 if fase < 0.5 else -0.7

        else:  # triángulo
            onda = 4 * abs(fase - 0.5) - 1

        # Ataque corto, caída suave y final sin "click"
        envolvente = min(1, t / 0.005) * math.exp(-t * caida)
        envolvente *= min(1, (total - i) / (FRECUENCIA * 0.01))

        buffer[posicion] += onda * envolvente * volumen


def agregar_bombo(buffer, inicio, volumen):

    primera = int(inicio * FRECUENCIA)
    total = int(0.15 * FRECUENCIA)

    fase = 0

    for i in range(total):

        posicion = primera + i

        if posicion >= len(buffer):
            break

        t = i / FRECUENCIA

        # El tono baja rápido (sonido de golpe)
        frecuencia = 45 + 90 * math.exp(-t * 30)

        fase += frecuencia / FRECUENCIA

        buffer[posicion] += math.sin(2 * math.pi * fase) * math.exp(-t * 18) * volumen


def agregar_ruido(buffer, inicio, duracion, volumen, caida):

    # Platillos y caja
    primera = int(inicio * FRECUENCIA)
    total = int(duracion * FRECUENCIA)

    anterior = 0

    for i in range(total):

        posicion = primera + i

        if posicion >= len(buffer):
            break

        t = i / FRECUENCIA

        ruido = random.uniform(-1, 1)

        # Quitar graves para que suene más brillante
        valor = ruido - anterior * 0.6
        anterior = ruido

        buffer[posicion] += valor * math.exp(-t * caida) * volumen


# ==========================================================
# CANCIONES
# ==========================================================

def cancion_medio():

    # Misteriosa, en La menor, 112 pulsos por minuto
    pulso = 60 / 112

    # (nota grave, tipo de acorde)
    acordes = [
        (45, "m"), (41, "M"), (48, "M"), (43, "M"),
        (45, "m"), (41, "M"), (50, "m"), (40, "M"),
    ]

    buffer = [0.0] * int(len(acordes) * 4 * pulso * FRECUENCIA)

    for compas, (raiz, tipo) in enumerate(acordes):

        inicio_compas = compas * 4 * pulso

        tercera = 3 if tipo == "m" else 4

        # Bajo (dos notas por compás)
        for tiempo in (0, 2):

            agregar_nota(buffer, inicio_compas + tiempo * pulso, pulso * 2, raiz, 0.35, "triangulo", 1.5)

        # Arpegio en corcheas
        arpegio = [0, tercera, 7, 12, 19, 12, 7, tercera]

        for i, intervalo in enumerate(arpegio):

            agregar_nota(
                buffer,
                inicio_compas + i * pulso / 2,
                pulso / 2,
                raiz + 24 + intervalo,
                0.16,
                "cuadrada",
                6
            )

        # Platillo suave a contratiempo
        for tiempo in range(4):

            agregar_ruido(buffer, inicio_compas + (tiempo + 0.5) * pulso, 0.05, 0.05, 60)

    return buffer


def cancion_avanzado():

    # Tensa y rápida, en Re menor, 150 pulsos por minuto
    pulso = 60 / 150

    acordes = [
        (38, "m"), (38, "m"), (46, "M"), (45, "M"),
        (38, "m"), (38, "m"), (43, "m"), (45, "M"),
    ]

    buffer = [0.0] * int(len(acordes) * 4 * pulso * FRECUENCIA)

    for compas, (raiz, tipo) in enumerate(acordes):

        inicio_compas = compas * 4 * pulso

        tercera = 3 if tipo == "m" else 4

        # Bajo que bombea en corcheas (nota y octava)
        for i in range(8):

            nota = raiz if i % 2 == 0 else raiz + 12

            agregar_nota(buffer, inicio_compas + i * pulso / 2, pulso / 2, nota, 0.3, "cuadrada", 7)

        # Melodía rápida en semicorcheas
        patron = [0, 12, tercera + 12, 7 + 12, 12, 7 + 12, tercera + 12, 7]

        for i in range(16):

            intervalo = patron[i % len(patron)]

            agregar_nota(
                buffer,
                inicio_compas + i * pulso / 4,
                pulso / 4,
                raiz + 36 + intervalo - 12,
                0.1,
                "cuadrada",
                10
            )

        # Batería
        for tiempo in range(4):

            momento = inicio_compas + tiempo * pulso

            agregar_bombo(buffer, momento, 0.7)

            # Caja en los tiempos 2 y 4
            if tiempo % 2 == 1:
                agregar_ruido(buffer, momento, 0.15, 0.3, 22)

            # Platillo a contratiempo
            agregar_ruido(buffer, momento + pulso / 2, 0.04, 0.12, 70)

    return buffer


# ==========================================================
# GUARDAR Y OBTENER LA MÚSICA
# ==========================================================

def guardar_wav(buffer, ruta):

    # Ajustar el volumen para que no se sature
    maximo = max(0.001, max(abs(valor) for valor in buffer))

    escala = 0.9 / maximo

    muestras = array.array(
        "h",
        (int(valor * escala * 32767) for valor in buffer)
    )

    with wave.open(ruta, "wb") as archivo:

        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(FRECUENCIA)
        archivo.writeframes(muestras.tobytes())


def ruta_musica(modo):

    # Devuelve el archivo de música del modo (lo crea si hace falta)
    ruta = os.path.join(CARPETA_SONIDOS, ARCHIVOS[modo])

    if os.path.exists(ruta):
        return ruta

    # Si no viene con el juego, se crea donde sí se puede escribir
    ruta = ruta_datos(ARCHIVOS[modo])

    if os.path.exists(ruta):
        return ruta

    if modo == "medio":
        guardar_wav(cancion_medio(), ruta)

    elif modo == "avanzado":
        guardar_wav(cancion_avanzado(), ruta)

    return ruta
