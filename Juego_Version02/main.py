import pygame
import sys
import random
import math
import os

from jugador import Jugador
from moneda import Moneda
from obstaculo import Obstaculo
from potenciador import Potenciador

from ambiente import Ambiente

from progreso import (
    TROFEOS,
    cargar_progreso,
    guardar_progreso,
    dibujar_trofeo_clave,
    dibujar_coleccion
)

from sonidos_extra import cargar_sonidos_extra

from modos import (
    MODOS,
    ORDEN_MODOS,
    COLORES_NAVE,
    tinte_nave
)

from jefe import Jefe
from rutas import ruta_recurso
from musica import ruta_musica
from pantallas import pantalla_modos, pantalla_logros, total_trofeos
from controles_tactiles import ControlesTactiles
from adaptacion_pantalla import presentar


# ==========================================================
# INICIALIZAR PYGAME
# ==========================================================

## sonidos de la nave y de los meteoritos

pygame.init()

carpeta_sonidos = ruta_recurso("sonidos")
sonido_moneda = pygame.mixer.Sound(
    os.path.join(carpeta_sonidos, "Points.mp3")
)
sonido_meteorito = pygame.mixer.Sound(
    os.path.join(carpeta_sonidos, "Error.mp3")
)
pygame.mixer.music.load(
    os.path.join(carpeta_sonidos, "Ambientacion_Jueguito.mp3")
)

# Música más suave para que se escuchen los efectos
pygame.mixer.music.set_volume(0.4)

# Sonidos creados por código (game over, trofeos, niveles...)
sonidos = cargar_sonidos_extra()


# ==========================================================
# PROGRESO GUARDADO (RÉCORD Y TROFEOS)
# ==========================================================

progreso = cargar_progreso()


# ==========================================================
# CONFIGURACIÓN DE LA PANTALLA
# ==========================================================

ANCHO = 600
ALTO = 700

# Icono de la ventana (la nave en órbita)
pygame.display.set_icon(
    pygame.image.load(ruta_recurso("icono.png"))
)

ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pantalla = pygame.Surface((ANCHO, ALTO))

pygame.display.set_caption(
    "Expedición 33"
)


# Control de FPS
reloj = pygame.time.Clock()

FPS = 60

ambiente = Ambiente(
    ANCHO,
    ALTO
)


# ==========================================================
# COLORES
# ==========================================================

NEGRO = (15, 15, 25)
BLANCO = (255, 255, 255)
GRIS = (60, 60, 70)
VERDE = (60, 220, 100)
ROJO = (220, 60, 60)
AMARILLO = (255, 220, 0)


# ==========================================================
# FUENTES
# ==========================================================

fuente = pygame.font.Font(None, 36)

fuente_grande = pygame.font.Font(
    None,
    70
)

fuente_pequeña = pygame.font.Font(
    None,
    28
)


# ==========================================================
# CONFIGURACIÓN DEL JUEGO
# ==========================================================

SUELO = ALTO - 100


# ==========================================================
# COLORES DE LA PANTALLA DE INICIO
# ==========================================================
 
AZUL = (15, 30, 65)
AZUL_LINEAS = (28, 48, 95)
AZUL_APAGADO = (120, 145, 190)
NARANJA = (255, 150, 30)
NARANJA_SOMBRA = (150, 70, 0)
CREMA = (255, 235, 190)

# ==========================================================
# FUNCIONES DE DIBUJO
# ==========================================================
 
def dibujar_corazon(pantalla, x, y, tam, color):
 
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
 
 
def dibujar_meteorito(pantalla, x, y, radio):
 
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
 
 
def dibujar_nave(pantalla, x, y, tiempo):
 
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
# PANTALLA DE INICIO
# ==========================================================
 
def pantalla_inicio(pantalla, ancho, alto, reloj, fps):
 
    # Devuelve "jugar" si el jugador elige SÍ, "logros" si elige
    # LOGROS y False si elige NO, presiona ESC o cierra la ventana.

    # Fuentes
    fuente_titulo = pygame.font.Font(None, 170)
    fuente = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 28)

    # Opción seleccionada: 0 = SÍ, 1 = LOGROS, 2 = NO
    opcion = 0
    controles_menu = ControlesTactiles(ancho, alto)
    zonas = [
        pygame.Rect(30 + i * (ancho - 60) // 3, 435,
                    (ancho - 60) // 3, 90)
        for i in range(3)
    ]

    # Mejor récord de todos los modos y trofeos ganados
    mejor_record = max(
        progreso["modos"][modo]["record"] for modo in ORDEN_MODOS
    )

    trofeos_ganados, trofeos_totales = total_trofeos(progreso)
 
    # Meteoritos de adorno cayendo detrás del menú
    meteoritos = []
 
    for i in range(4):
 
        meteorito = Obstaculo(0,0)
        meteorito.reiniciar(ancho)
        meteoritos.append(meteorito)

    # Nave de adorno
    nave = Jugador(ancho // 2 - 30, alto - 150)


    while True:
 
        # ==================================================
        # EVENTOS
        # ==================================================
 
        for evento in pygame.event.get():
 
            if evento.type == pygame.QUIT:
                return False

            toque = controles_menu.evento(evento)
            if toque is not None and toque[0] == "back":
                if controles_menu.doble_atras():
                    return False
                continue

            if toque is not None and toque[0] == "down":
                _, posicion = toque
                for indice, zona in enumerate(zonas):
                    if zona.collidepoint(posicion):
                        opcion = indice
                        sonidos["elegir"].play()
                        if opcion == 0:
                            return "jugar"
                        if opcion == 1:
                            return "logros"
                        return False
 
            if evento.type == pygame.KEYDOWN:
 
                # Cambiar de opción
                if evento.key in (
                    pygame.K_LEFT,
                    pygame.K_UP,
                    pygame.K_a,
                    pygame.K_w
                ):
                    opcion = (opcion - 1) % 3
                    sonidos["mover"].play()

                if evento.key in (
                    pygame.K_RIGHT,
                    pygame.K_DOWN,
                    pygame.K_d,
                    pygame.K_s
                ):
                    opcion = (opcion + 1) % 3
                    sonidos["mover"].play()

                # Confirmar
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                    sonidos["elegir"].play()

                    if opcion == 0:
                        return "jugar"

                    if opcion == 1:
                        return "logros"

                    return False
 
                # Salir
                if evento.key == pygame.K_ESCAPE:
                    return False
 
        # ==================================================
        # FONDO
        # ==================================================
 
        pantalla.fill(AZUL)
 
        # Cuadrícula
        for x in range(0, ancho, 50):
            pygame.draw.line(pantalla, AZUL_LINEAS, (x, 0), (x, alto))
 
        for y in range(0, alto, 50):
            pygame.draw.line(pantalla, AZUL_LINEAS, (0, y), (ancho, y))
 
        # Meteoritos cayendo
        for m in meteoritos:
        
            m.actualizar(2)
 
            if m.esta_fuera(alto):
                m.reiniciar(ancho)

        m.dibujar(pantalla)
 
        # Nave de adorno
        nave.dibujar(pantalla)

        marco = pygame.Rect(30, 30, ancho - 60, alto - 60)
        pygame.draw.rect(pantalla, AZUL_APAGADO, marco, 4, border_radius=30)

        

 
        # ==================================================
        # PARTE SUPERIOR
        # ==================================================
 
        texto_nombre = fuente_pequena.render(
            "EXPEDICIÓN 33",
            True,
            CREMA
        )
 
        pantalla.blit(texto_nombre, (60, 60))

        texto_record = fuente_pequena.render(
            f"RÉCORD: {mejor_record}",
            True,
            NARANJA
        )

        pantalla.blit(texto_record, (60, 88))

        texto_trofeos = fuente_pequena.render(
            f"TROFEOS: {trofeos_ganados}/{trofeos_totales}",
            True,
            NARANJA
        )

        pantalla.blit(texto_trofeos, (60, 116))

        # Corazones (las 3 vidas del juego)
        for i in range(3):
 
            dibujar_corazon(
                pantalla,
                ancho - 60 - 32 - i * 42,
                58,
                32,
                NARANJA
            )
 
        # ==================================================
        # TÍTULO
        # ==================================================
 
        sombra = fuente_titulo.render("START", True, NARANJA_SOMBRA)
        titulo = fuente_titulo.render("START", True, NARANJA)
 
        rect_titulo = titulo.get_rect(center=(ancho // 2, 230))
 
        pantalla.blit(sombra, rect_titulo.move(5, 5))
        pantalla.blit(titulo, rect_titulo)
 
        texto_sub = fuente_pequena.render(
            "EXPEDICIÓN 33",
            True,
            CREMA
        )
 
        pantalla.blit(
            texto_sub,
            texto_sub.get_rect(center=(ancho // 2, 320))
        )
 
        # ==================================================
        # PREGUNTA Y OPCIONES
        # ==================================================
 
        texto_listo = fuente.render("¿ESTÁS LISTO?", True, CREMA)
 
        pantalla.blit(
            texto_listo,
            texto_listo.get_rect(center=(ancho // 2, 410))
        )
 
        opciones = ["SÍ", "LOGROS", "NO"]

        posiciones = [
            30 + (i * 2 + 1) * (ancho - 60) // 6
            for i in range(3)
        ]

        for i in range(3):
 
            if i == opcion:
                color = CREMA
            else:
                color = AZUL_APAGADO
 
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
            AZUL_APAGADO
        )
 
        pantalla.blit(
            texto_ayuda,
            texto_ayuda.get_rect(center=(ancho // 2, alto - 60))
        )

        # En Android las opciones son botones táctiles; se mantiene la
        # navegación por teclado para ordenador y dispositivos con teclado.
        for indice, zona in enumerate(zonas):
            pygame.draw.rect(pantalla, (255, 170, 50, 28), zona, 2, border_radius=12)
 
        # ==================================================
        # ACTUALIZAR PANTALLA
        # ==================================================
 
        presentar(pantalla)
 
        reloj.tick(fps)

# ==========================================================
# MENÚS: INICIO, LOGROS Y ELEGIR MODO
# ==========================================================

def flujo_menu(modo_inicial):

    # Muestra el menú hasta que el jugador elige un modo.
    # Devuelve el modo elegido o None si quiere salir.

    pygame.mixer.music.stop()

    while True:

        resultado = pantalla_inicio(pantalla, ANCHO, ALTO, reloj, FPS)

        if not resultado:
            return None

        if resultado == "logros":

            pantalla_logros(pantalla, reloj, FPS, progreso, sonidos)
            continue

        modo = pantalla_modos(
            pantalla, reloj, FPS, progreso, sonidos, modo_inicial
        )

        # ESC en la pantalla de modos vuelve al inicio
        if modo is not None:
            return modo


def iniciar_musica(modo):

    pygame.mixer.music.load(ruta_musica(modo))

    # Las canciones de los modos Medio y Avanzado suenan más fuerte
    if modo == "basico":
        pygame.mixer.music.set_volume(0.4)
    else:
        pygame.mixer.music.set_volume(0.3)

    pygame.mixer.music.play(loops=-1)


def aplicar_modo(modo):

    # Ajusta todo lo que depende del modo de juego
    global modo_actual, config

    modo_actual = modo
    config = MODOS[modo]

    Obstaculo.PROBABILIDAD_ZIGZAG = config["probabilidad_zigzag"]
    Obstaculo.ANCHO_PANTALLA = ANCHO

    Potenciador.PESOS = config["pesos_potenciadores"]

    ambiente.cambiar_tema(modo)


# ==========================================================
# MOSTRAR LA PANTALLA DE INICIO
# ==========================================================

modo_actual = "basico"
config = MODOS[modo_actual]

modo_elegido = flujo_menu("basico")

if modo_elegido is None:
    pygame.quit()
    sys.exit()

aplicar_modo(modo_elegido)


# ==========================================================
# REGLAS DE LA PARTIDA
# ==========================================================

# Cada cuántos puntos se sube de nivel
PUNTOS_POR_NIVEL = 25

# Cuántas monedas seguidas hacen subir el multiplicador
MONEDAS_POR_COMBO = 5
MULTIPLICADOR_MAXIMO = 5

# Cada cuántos segundos aparece un meteorito más
SEGUNDOS_POR_OBSTACULO = 20

# Duración de la invulnerabilidad después de un golpe
DURACION_INVULNERABLE = 1.5

# Jefe: aparece desde los puntos del modo y luego cada 100
PUNTOS_POR_JEFE = 100
PREMIO_JEFE = 25

# Arma: la nave dispara sola mientras dura
DURACION_ARMA = 10
CADENCIA_DISPARO = 0.15
VELOCIDAD_BALA = 12

# Lienzo donde se dibuja el juego (para poder sacudir la pantalla)
lienzo = pygame.Surface((ANCHO, ALTO))
controles_tactiles = ControlesTactiles(ANCHO, ALTO)

fuente_titulo = pygame.font.Font(None, 110)
fuente_trofeo = pygame.font.Font(None, 58)


# ==========================================================
# FUNCIONES DE AYUDA
# ==========================================================

def datos_modo():

    # Récord y trofeos del modo que se está jugando
    return progreso["modos"][modo_actual]


def lugar_libre(rect, otros):

    # True si el rectángulo no choca con ninguno de los otros
    # (se agranda un poco para dejar espacio entre objetos)
    zona = rect.inflate(30, 30)

    for otro in otros:

        if zona.colliderect(otro.rect):
            return False

    return True


def reubicar_moneda(moneda, obstaculos):

    # Busca un lugar donde la moneda no aparezca encima de un meteorito
    for intento in range(15):

        moneda.reiniciar(ANCHO)

        if lugar_libre(moneda.rect, obstaculos):
            return


def reubicar_obstaculo(obstaculo, monedas):

    # Busca un lugar donde el meteorito no tape una moneda
    for intento in range(15):

        obstaculo.reiniciar(ANCHO)

        if lugar_libre(obstaculo.rect, monedas):
            return


def calcular_multiplicador(combo):

    return min(
        MULTIPLICADOR_MAXIMO,
        1 + combo // MONEDAS_POR_COMBO
    )


def agregar_texto_flotante(texto, x, y, color):

    textos_flotantes.append({
        "texto": texto,
        "x": x,
        "y": y,
        "color": color,
        "vida": 45
    })


# ==========================================================
# FUNCIÓN PARA CREAR UNA PARTIDA NUEVA
# ==========================================================

def iniciar_juego():

    # --------------------------
    # Jugador (con el color elegido)
    # --------------------------

    jugador = Jugador(
        ANCHO // 2 - 30,
        SUELO - 70,
        tinte_nave(progreso["color_nave"], modo_actual)
    )


    # --------------------------
    # Obstáculos
    # --------------------------

    obstaculos = []

    for i in range(config["obstaculos_iniciales"]):

        x = random.randint(
            0,
            ANCHO - 45
        )

        y = random.randint(
            -900,
            -150
        )

        obstaculo = Obstaculo(
            x,
            y
        )

        obstaculos.append(obstaculo)


    # --------------------------
    # Monedas
    # --------------------------

    monedas = []

    for i in range(4):

        moneda = Moneda(0, 0)

        reubicar_moneda(moneda, obstaculos)

        monedas.append(moneda)


    # --------------------------
    # Objetos especiales
    # --------------------------

    potenciadores = []

    # Segundo en el que aparecerá el primero
    siguiente_potenciador = random.uniform(6, 10)


    # --------------------------
    # Puntuación, combo y nivel
    # --------------------------

    puntos = 0
    combo = 0
    nivel = 1


    # --------------------------
    # Vidas
    # --------------------------

    vidas = config["vidas"]


    # --------------------------
    # Trofeos ganados en esta partida
    # --------------------------

    trofeos_partida = []


    # --------------------------
    # Tiempo de inicio
    # --------------------------

    tiempo_inicio = pygame.time.get_ticks()


    return (
        jugador,
        monedas,
        obstaculos,
        potenciadores,
        puntos,
        vidas,
        combo,
        nivel,
        trofeos_partida,
        siguiente_potenciador,
        tiempo_inicio
    )


# ==========================================================
# INICIAR LA PARTIDA
# ==========================================================

(
    jugador,
    monedas,
    obstaculos,
    potenciadores,
    puntos,
    vidas,
    combo,
    nivel,
    trofeos_partida,
    siguiente_potenciador,
    tiempo_inicio
) = iniciar_juego()

iniciar_musica(modo_actual)


# Estado del juego:
# "jugando", "pausa", "trofeo" o "game_over"
estado = "jugando"

# Momento en que empezó la pausa (o el trofeo)
inicio_pausa = 0

# Trofeo que se está mostrando
trofeo_mostrado = None

# Textos que suben y desaparecen ("+1", "+5", "ESCUDO"...)
textos_flotantes = []

# Mensaje grande de nivel
mensaje_nivel = ""
mensaje_nivel_hasta = 0

# Sacudida de la pantalla
temblor = 0

# Jefe
jefe = None
proximo_jefe = config["puntos_primer_jefe"]

# Balas de la nave
balas = []
siguiente_bala = 0

# Datos del Game Over
nuevo_record = False
opcion_game_over = 0

tiempo_transcurrido = 0
velocidad_objetos = config["velocidad_inicial"]


# ==========================================================
# CAMBIOS DE ESTADO
# ==========================================================

def pausar(nuevo_estado):

    global estado, inicio_pausa

    estado = nuevo_estado
    inicio_pausa = pygame.time.get_ticks()


def continuar():

    # Al volver de la pausa se "corre" el tiempo de inicio
    # para que el tiempo de la partida no avance mientras
    # el juego estaba detenido.
    global estado, tiempo_inicio

    tiempo_inicio += pygame.time.get_ticks() - inicio_pausa

    estado = "jugando"


def terminar_partida():

    global estado, nuevo_record

    estado = "game_over"

    pygame.mixer.music.fadeout(800)
    sonidos["game_over"].play()

    # Guardar el récord del modo
    nuevo_record = puntos > datos_modo()["record"]

    if nuevo_record:

        datos_modo()["record"] = puntos
        guardar_progreso(progreso)


def reiniciar_partida():

    global jugador, monedas, obstaculos, potenciadores
    global puntos, vidas, combo, nivel, trofeos_partida
    global siguiente_potenciador, tiempo_inicio
    global estado, textos_flotantes, mensaje_nivel, temblor
    global opcion_game_over, jefe, proximo_jefe
    global tiempo_transcurrido, balas, siguiente_bala

    (
        jugador,
        monedas,
        obstaculos,
        potenciadores,
        puntos,
        vidas,
        combo,
        nivel,
        trofeos_partida,
        siguiente_potenciador,
        tiempo_inicio
    ) = iniciar_juego()

    estado = "jugando"
    textos_flotantes = []
    mensaje_nivel = ""
    temblor = 0
    opcion_game_over = 0
    jefe = None
    proximo_jefe = config["puntos_primer_jefe"]
    tiempo_transcurrido = 0
    balas = []
    siguiente_bala = 0

    iniciar_musica(modo_actual)


def volver_al_menu():

    # Devuelve False si el jugador decide salir del juego
    modo = flujo_menu(modo_actual)

    if modo is None:
        return False

    aplicar_modo(modo)
    reiniciar_partida()

    return True


def golpear_jugador(x, y):

    # El jugador pierde una vida
    global vidas, combo, temblor

    sonido_meteorito.play()

    vidas -= 1

    # Se pierde el combo
    combo = 0

    jugador.recibir_golpe(DURACION_INVULNERABLE)

    ambiente.efecto_golpe(x, y)

    # Sacudir la pantalla
    temblor = 18

    # Si no quedan vidas
    if vidas <= 0:
        terminar_partida()


def escudo_absorbe(x, y):

    sonidos["escudo"].play()

    ambiente.efecto_golpe(x, y)


def modo_que_desbloquea(trofeo):

    # Nombre del modo que se abre con este trofeo (o None)
    for clave in ORDEN_MODOS:

        if MODOS[clave]["requisito"] == (modo_actual, trofeo):
            return MODOS[clave]["nombre"]

    return None


def colores_que_desbloquea(trofeo):

    nombres = []

    for clave, nombre, tinte, requisito in COLORES_NAVE:

        if requisito == (modo_actual, trofeo):
            nombres.append(nombre)

    return nombres


# ==========================================================
# FUNCIONES DE DIBUJO DE LAS PANTALLAS
# ==========================================================

def dibujar_hud():

    # Puntos
    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_puntos,
        (20, 20)
    )


    # Vidas como corazones
    for i in range(config["vidas_maximas"]):

        if i < vidas:
            color = ROJO
        else:
            color = GRIS

        dibujar_corazon(
            pantalla,
            20 + i * 34,
            58,
            28,
            color
        )


    # Combo
    multiplicador = calcular_multiplicador(combo)

    if multiplicador > 1:

        # Palpita un poco
        tamaño = 32 + int(math.sin(pygame.time.get_ticks() * 0.01) * 3)

        fuente_combo = pygame.font.Font(None, tamaño)

        texto_combo = fuente_combo.render(
            f"COMBO x{multiplicador}",
            True,
            NARANJA
        )

        pantalla.blit(
            texto_combo,
            (20, 96)
        )


    # Mostrar velocidad
    texto_velocidad = fuente_pequeña.render(
        f"Velocidad: {velocidad_objetos:.1f}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_velocidad,
        (ANCHO - 160, 25)
    )


    # Mostrar tiempo
    texto_tiempo = fuente_pequeña.render(
        f"Tiempo: {tiempo_transcurrido:.0f}s",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_tiempo,
        (ANCHO - 160, 55)
    )


    # Mostrar nivel
    texto_nivel = fuente_pequeña.render(
        f"Nivel: {nivel}",
        True,
        AMARILLO
    )

    pantalla.blit(
        texto_nivel,
        (ANCHO - 160, 85)
    )


    # Mostrar récord del modo
    texto_record = fuente_pequeña.render(
        f"Récord: {max(puntos, datos_modo()['record'])}",
        True,
        CREMA
    )

    pantalla.blit(
        texto_record,
        (ANCHO - 160, 115)
    )


    # Trofeos ganados en esta partida (pequeños)
    for i, (clave, nombre, req, color, sombra) in enumerate(TROFEOS):

        if clave in trofeos_partida:

            dibujar_trofeo_clave(
                pantalla,
                clave,
                ANCHO - 145 + i * 30,
                160,
                0.35
            )


    # Modo de juego (abajo a la derecha)
    texto_modo = fuente_pequeña.render(
        f"MODO {config['nombre']}",
        True,
        config["color"]
    )

    pantalla.blit(
        texto_modo,
        texto_modo.get_rect(bottomright=(ANCHO - 20, ALTO - 15))
    )


    # Barras de tiempo del escudo y del imán
    y_barra = ALTO - 30

    efectos = [
        ("ESCUDO", jugador.escudo_hasta, config["duracion_escudo"], (80, 200, 255)),
        ("IMÁN", jugador.iman_hasta, config["duracion_iman"], (200, 90, 255)),
        ("DISPARO", jugador.arma_hasta, DURACION_ARMA, (255, 150, 40)),
    ]

    for nombre, hasta, duracion, color in efectos:

        restante = hasta - tiempo_transcurrido

        if restante > 0:

            texto = fuente_pequeña.render(nombre, True, color)
            pantalla.blit(texto, (20, y_barra - 4))

            pygame.draw.rect(pantalla, GRIS, (120, y_barra, 150, 12), border_radius=6)

            pygame.draw.rect(
                pantalla,
                color,
                (120, y_barra, int(150 * restante / duracion), 12),
                border_radius=6
            )

            y_barra -= 28


    # Barra de tiempo del jefe
    if jefe is not None:

        jefe.dibujar_barra(pantalla)


    # Mensaje de nuevo nivel
    if mensaje_nivel and tiempo_transcurrido < mensaje_nivel_hasta:

        restante = mensaje_nivel_hasta - tiempo_transcurrido

        alpha = int(min(1, restante) * 255)

        sombra = fuente_titulo.render(mensaje_nivel, True, NARANJA_SOMBRA)
        texto = fuente_titulo.render(mensaje_nivel, True, NARANJA)

        sombra.set_alpha(alpha)
        texto.set_alpha(alpha)

        rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 120))

        pantalla.blit(sombra, rect.move(4, 4))
        pantalla.blit(texto, rect)


    # Aviso del jefe
    if jefe is not None:

        jefe.dibujar_alerta(pantalla)


def dibujar_pausa():

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((5, 10, 30, 190))
    pantalla.blit(capa, (0, 0))

    sombra = fuente_titulo.render("PAUSA", True, NARANJA_SOMBRA)
    titulo = fuente_titulo.render("PAUSA", True, NARANJA)

    rect = titulo.get_rect(center=(ANCHO // 2, max(90, ALTO // 5)))

    pantalla.blit(sombra, rect.move(5, 5))
    pantalla.blit(titulo, rect)

    for rect, etiqueta in botones_pausa():
        pygame.draw.rect(pantalla, (255, 170, 50), rect, 2, border_radius=12)
        texto = fuente_pequeña.render(etiqueta, True, CREMA)
        pantalla.blit(texto, texto.get_rect(center=rect.center))


def botones_pausa():
    """Devuelve los mismos botones para dibujar y para detectar toques."""
    margen = max(30, ANCHO // 12)
    ancho = ANCHO - margen * 2
    alto_boton = max(52, min(76, ALTO // 10))
    separacion = max(12, alto_boton // 4)
    inicio = max(ALTO // 3, ALTO - (alto_boton * 3 + separacion * 2) - ALTO // 10)

    return [
        (pygame.Rect(margen, inicio + i * (alto_boton + separacion), ancho, alto_boton), etiqueta)
        for i, etiqueta in enumerate(("CONTINUAR", "MENÚ", "SALIR"))
    ]


def dibujar_trofeo_ganado():

    datos, es_nuevo, modo_abierto, colores_nuevos = trofeo_mostrado
    clave, nombre, req, color, sombra_trofeo = datos

    # Fuente para "NIVEL MASTER" / "NIVEL LEYENDA"
    fuente_master = pygame.font.Font(None, 48)

    segundos = (pygame.time.get_ticks() - inicio_pausa) / 1000

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((5, 10, 30, 210))
    pantalla.blit(capa, (0, 0))

    cx = ANCHO // 2
    cy = ALTO // 2 - 50

    # Rayos de luz que giran detrás del trofeo
    rayos = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    for i in range(12):

        angulo = segundos * 0.8 + i * math.pi / 6

        punta1 = (
            cx + math.cos(angulo - 0.12) * 400,
            cy + math.sin(angulo - 0.12) * 400
        )

        punta2 = (
            cx + math.cos(angulo + 0.12) * 400,
            cy + math.sin(angulo + 0.12) * 400
        )

        pygame.draw.polygon(rayos, (*color, 35), [(cx, cy), punta1, punta2])

    pantalla.blit(rayos, (0, 0))

    es_diamante = clave == "diamante"

    # El trofeo crece al aparecer y luego flota
    if es_diamante:
        escala_final = 2.3
    else:
        escala_final = 2.6

    escala = min(escala_final, 0.5 + segundos * 5)
    flotar = math.sin(segundos * 3) * 6

    dibujar_trofeo_clave(
        pantalla,
        clave,
        cx,
        int(cy + flotar),
        escala
    )

    # Textos
    if es_diamante:

        titulo = fuente_trofeo.render("¡TROFEO DIAMANTE!", True, color)

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(cx, cy - 195))
        )

        # "NIVEL MASTER" o "NIVEL LEYENDA" cambia de color como un brillo
        onda = (math.sin(segundos * 4) + 1) / 2

        color_master = (
            int(120 + onda * 135),
            int(225 + onda * 30),
            255
        )

        texto_diamante = config["texto_diamante"]

        sombra_master = fuente_master.render(texto_diamante, True, sombra_trofeo)
        texto_master = fuente_master.render(texto_diamante, True, color_master)

        rect_master = texto_master.get_rect(center=(cx, cy - 150))

        pantalla.blit(sombra_master, rect_master.move(3, 3))
        pantalla.blit(texto_master, rect_master)

    else:

        titulo = fuente_trofeo.render(f"¡TROFEO DE {nombre}!", True, color)

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(cx, cy - 160))
        )

    texto_puntos = fuente.render(
        f"Llegaste a {req} puntos en modo {config['nombre']}",
        True,
        CREMA
    )

    pantalla.blit(
        texto_puntos,
        texto_puntos.get_rect(center=(cx, cy + 145))
    )

    if es_nuevo:
        subtitulo = "¡NUEVO TROFEO GUARDADO!"
    else:
        subtitulo = "Ya tenías este trofeo"

    texto_sub = fuente_pequeña.render(subtitulo, True, AMARILLO)

    pantalla.blit(
        texto_sub,
        texto_sub.get_rect(center=(cx, cy + 180))
    )

    # Lo que se desbloquea con este trofeo
    y_extra = cy + 222

    if modo_abierto is not None:

        # Cartel que palpita
        tamaño = 40 + int(math.sin(segundos * 6) * 3)
        fuente_desbloqueo = pygame.font.Font(None, tamaño)

        texto = fuente_desbloqueo.render(
            f"¡MODO {modo_abierto} DESBLOQUEADO!",
            True,
            NARANJA
        )

        rect = texto.get_rect(center=(cx, y_extra))

        fondo = rect.inflate(30, 14)

        pygame.draw.rect(pantalla, (40, 20, 5), fondo, border_radius=12)
        pygame.draw.rect(pantalla, NARANJA, fondo, 3, border_radius=12)

        pantalla.blit(texto, rect)

        y_extra += 45

    for nombre_color in colores_nuevos:

        texto = fuente_pequeña.render(
            f"¡Nuevo color de nave: {nombre_color}!",
            True,
            (150, 230, 255)
        )

        pantalla.blit(texto, texto.get_rect(center=(cx, y_extra)))

        y_extra += 28

    if segundos > 1:

        texto_seguir = fuente_pequeña.render(
            "Presiona cualquier tecla para continuar",
            True,
            AZUL_APAGADO
        )

        pantalla.blit(
            texto_seguir,
            texto_seguir.get_rect(midbottom=(cx, ALTO - 24))
        )


def dibujar_game_over():

    # Fondo semitransparente del color del modo
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((*config["fondo"], 225))
    pantalla.blit(capa, (0, 0))

    marco = pygame.Rect(30, 30, ANCHO - 60, ALTO - 60)
    pygame.draw.rect(pantalla, AZUL_APAGADO, marco, 4, border_radius=30)

    # Título
    sombra = fuente_titulo.render("GAME OVER", True, NARANJA_SOMBRA)
    titulo = fuente_titulo.render("GAME OVER", True, NARANJA)

    rect_titulo = titulo.get_rect(center=(ANCHO // 2, 115))

    pantalla.blit(sombra, rect_titulo.move(5, 5))
    pantalla.blit(titulo, rect_titulo)

    texto_modo = fuente_pequeña.render(
        f"MODO {config['nombre']}",
        True,
        config["color"]
    )

    pantalla.blit(
        texto_modo,
        texto_modo.get_rect(center=(ANCHO // 2, 168))
    )

    # Puntuación final
    texto_final = fuente.render(
        f"Puntuación: {puntos}",
        True,
        CREMA
    )

    pantalla.blit(
        texto_final,
        texto_final.get_rect(center=(ANCHO // 2, 205))
    )

    texto_record = fuente_pequeña.render(
        f"Récord: {datos_modo()['record']}",
        True,
        AZUL_APAGADO
    )

    pantalla.blit(
        texto_record,
        texto_record.get_rect(center=(ANCHO // 2, 245))
    )

    # Nuevo récord (parpadea)
    if nuevo_record and (pygame.time.get_ticks() // 400) % 2 == 0:

        texto_nuevo = fuente.render("¡NUEVO RÉCORD!", True, AMARILLO)

        pantalla.blit(
            texto_nuevo,
            texto_nuevo.get_rect(center=(ANCHO // 2, 285))
        )

    # Colección de trofeos del modo
    texto_trofeos = fuente_pequeña.render("TROFEOS", True, CREMA)

    pantalla.blit(
        texto_trofeos,
        texto_trofeos.get_rect(center=(ANCHO // 2, 335))
    )

    dibujar_coleccion(
        pantalla,
        ANCHO // 2,
        400,
        0.8,
        datos_modo()["trofeos"],
        fuente_pequeña
    )

    # Pregunta y opciones
    texto_otra = fuente.render("¿JUGAR OTRA VEZ?", True, CREMA)

    pantalla.blit(
        texto_otra,
        texto_otra.get_rect(center=(ANCHO // 2, 505))
    )

    opciones = ["SÍ", "MENÚ", "NO"]

    posiciones = [ANCHO // 2 - 160, ANCHO // 2 - 10, ANCHO // 2 + 150]

    for i in range(3):

        if i == opcion_game_over:
            color = CREMA
        else:
            color = AZUL_APAGADO

        texto = fuente.render(opciones[i], True, color)

        rect = texto.get_rect(center=(posiciones[i], 565))

        pantalla.blit(texto, rect)

        # Triángulo que señala la opción elegida
        if i == opcion_game_over:

            pygame.draw.polygon(
                pantalla,
                NARANJA,
                [
                    (rect.right + 28, rect.centery - 10),
                    (rect.right + 10, rect.centery),
                    (rect.right + 28, rect.centery + 10)
                ]
            )

    texto_ayuda = fuente_pequeña.render(
        "ENTER para confirmar   -   R reinicia   -   ESC sale",
        True,
        AZUL_APAGADO
    )

    pantalla.blit(
        texto_ayuda,
        texto_ayuda.get_rect(center=(ANCHO // 2, ALTO - 65))
    )


# ==========================================================
# BUCLE PRINCIPAL
# ==========================================================

ejecutando = True


while ejecutando:

    # ======================================================
    # EVENTOS
    # ======================================================

    for evento in pygame.event.get():

        # Cerrar ventana
        if evento.type == pygame.QUIT:
            ejecutando = False

        toque = controles_tactiles.evento(evento)
        if toque is not None and toque[0] == "back":
            if controles_tactiles.doble_atras():
                ejecutando = False
                continue
            if estado == "jugando":
                pausar("pausa")
                pygame.mixer.music.pause()
                sonidos["pausa"].play()
            elif estado == "trofeo":
                continuar()
            continue

        if toque is not None and toque[0] == "swipe":
            gesto = toque[1]
            if estado == "jugando" and gesto in ("izquierda", "derecha"):
                jugador.rect.x += 90 if gesto == "derecha" else -90
                jugador.rect.left = max(0, jugador.rect.left)
                jugador.rect.right = min(ANCHO, jugador.rect.right)
            continue

        if toque is not None and toque[0] == "motion" and estado == "jugando":
            _, (_, desplazamiento_x, _) = toque
            jugador.rect.x += desplazamiento_x
            jugador.rect.left = max(0, jugador.rect.left)
            jugador.rect.right = min(ANCHO, jugador.rect.right)
            continue

        if toque is not None and toque[0] == "down":
            _, posicion = toque

            if estado == "pausa":
                botones = botones_pausa()
                if botones[0][0].collidepoint(posicion):
                    continuar()
                    pygame.mixer.music.unpause()
                    sonidos["pausa"].play()
                elif botones[1][0].collidepoint(posicion):
                    if not volver_al_menu():
                        ejecutando = False
                elif botones[2][0].collidepoint(posicion):
                    ejecutando = False

            elif estado == "trofeo":
                if pygame.time.get_ticks() - inicio_pausa > 1000:
                    continuar()

            elif estado == "game_over" and 510 <= posicion[1] <= 630:
                if posicion[0] < ANCHO // 3:
                    opcion_game_over = 0
                    reiniciar_partida()
                elif posicion[0] < 2 * ANCHO // 3:
                    opcion_game_over = 1
                    if not volver_al_menu():
                        ejecutando = False
                else:
                    opcion_game_over = 2
                    ejecutando = False


        # Teclas presionadas
        if evento.type == pygame.KEYDOWN:

            # ----------------------------------------------
            # Jugando: P o ESC pausan
            # ----------------------------------------------

            if estado == "jugando":

                if evento.key in (pygame.K_p, pygame.K_ESCAPE):

                    pausar("pausa")
                    pygame.mixer.music.pause()
                    sonidos["pausa"].play()


            # ----------------------------------------------
            # En pausa
            # ----------------------------------------------

            elif estado == "pausa":

                if evento.key in (pygame.K_p, pygame.K_ESCAPE):

                    continuar()
                    pygame.mixer.music.unpause()
                    sonidos["pausa"].play()

                elif evento.key == pygame.K_m:

                    if not volver_al_menu():
                        ejecutando = False

                elif evento.key == pygame.K_q:

                    ejecutando = False


            # ----------------------------------------------
            # Mostrando un trofeo
            # ----------------------------------------------

            elif estado == "trofeo":

                # Se espera un momento para no saltarlo sin querer
                if pygame.time.get_ticks() - inicio_pausa > 1000:

                    continuar()


            # ----------------------------------------------
            # Game Over
            # ----------------------------------------------

            elif estado == "game_over":

                # Cambiar de opción
                if evento.key in (
                    pygame.K_LEFT,
                    pygame.K_UP,
                    pygame.K_a,
                    pygame.K_w
                ):
                    opcion_game_over = (opcion_game_over - 1) % 3
                    sonidos["mover"].play()

                if evento.key in (
                    pygame.K_RIGHT,
                    pygame.K_DOWN,
                    pygame.K_d,
                    pygame.K_s
                ):
                    opcion_game_over = (opcion_game_over + 1) % 3
                    sonidos["mover"].play()

                # Confirmar
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                    if opcion_game_over == 0:
                        reiniciar_partida()

                    elif opcion_game_over == 1:

                        if not volver_al_menu():
                            ejecutando = False

                    else:
                        ejecutando = False

                # Presionar R para reiniciar
                elif evento.key == pygame.K_r:

                    reiniciar_partida()

                # ESC para salir
                elif evento.key == pygame.K_ESCAPE:

                    ejecutando = False


    # ======================================================
    # TECLAS
    # ======================================================

    teclas = pygame.key.get_pressed()


    # ======================================================
    # ACTUALIZAR JUEGO
    # ======================================================

    # El trofeo se cierra solo después de unos segundos
    if estado == "trofeo":

        # El de diamante se queda un poco más
        if trofeo_mostrado[0][0] == "diamante":
            duracion_trofeo = 5000
        else:
            duracion_trofeo = 3500

        if pygame.time.get_ticks() - inicio_pausa > duracion_trofeo:

            continuar()


    if estado == "jugando":

        # --------------------------------------------------
        # MOVIMIENTO DEL JUGADOR
        # --------------------------------------------------

        jugador.mover(
            teclas,
            ANCHO
        )


        # --------------------------------------------------
        # CALCULAR TIEMPO
        # --------------------------------------------------

        tiempo_actual = pygame.time.get_ticks()

        tiempo_transcurrido = (
            tiempo_actual - tiempo_inicio
        ) / 1000

        ambiente.actualizar(tiempo_transcurrido)

        jugador.actualizar_tiempo(tiempo_transcurrido)


        # --------------------------------------------------
        # AUMENTAR VELOCIDAD
        # --------------------------------------------------

        # Empieza según el modo y aumenta progresivamente.
        # Cada nivel suma 0.25 más.

        velocidad_objetos = (
            config["velocidad_inicial"]
            + tiempo_transcurrido * config["aumento_velocidad"]
            + (nivel - 1) * 0.25
        )


        # --------------------------------------------------
        # JEFE (modo Avanzado)
        # --------------------------------------------------

        if (
            config["tiene_jefe"]
            and jefe is None
            and puntos >= proximo_jefe
        ):

            jefe = Jefe(ANCHO, ALTO, tiempo_transcurrido, sonidos)

        # Mientras está el jefe no caen meteoritos nuevos
        jefe_activo = jefe is not None and jefe.esta_activo()

        if jefe is not None:

            jefe.actualizar(tiempo_transcurrido, jugador.rect)

            golpe = jefe.golpea(jugador.rect)

            if golpe is not None:

                if jugador.tiene_escudo():
                    escudo_absorbe(*golpe)

                elif not jugador.es_invulnerable():
                    golpear_jugador(*golpe)

            # Premio por sobrevivir
            if estado == "jugando" and jefe.premio_pendiente():

                puntos += PREMIO_JEFE

                agregar_texto_flotante(
                    "¡SOBREVIVISTE!",
                    ANCHO // 2,
                    jefe.y,
                    NARANJA
                )

                agregar_texto_flotante(
                    f"+{PREMIO_JEFE}",
                    ANCHO // 2,
                    jefe.y + 40,
                    AMARILLO
                )

                if vidas < config["vidas_maximas"]:

                    vidas += 1

                    agregar_texto_flotante(
                        "+1 VIDA",
                        jugador.rect.centerx,
                        jugador.rect.top - 20,
                        ROJO
                    )

            if jefe.terminado():

                jefe = None

                proximo_jefe = (puntos // PUNTOS_POR_JEFE + 1) * PUNTOS_POR_JEFE


        # --------------------------------------------------
        # MÁS METEORITOS CON EL TIEMPO
        # --------------------------------------------------

        cantidad_obstaculos = min(
            config["obstaculos_maximos"],
            config["obstaculos_iniciales"]
            + int(tiempo_transcurrido // SEGUNDOS_POR_OBSTACULO)
        )

        while len(obstaculos) < cantidad_obstaculos and not jefe_activo:

            nuevo = Obstaculo(0, 0)

            reubicar_obstaculo(nuevo, monedas)

            obstaculos.append(nuevo)


        # --------------------------------------------------
        # ACTUALIZAR MONEDAS
        # --------------------------------------------------

        for moneda in monedas:

            moneda.actualizar(
                velocidad_objetos
            )


            # El imán atrae las monedas cercanas
            if jugador.tiene_iman() and moneda.rect.bottom > 0:

                distancia = math.hypot(
                    moneda.rect.centerx - jugador.rect.centerx,
                    moneda.rect.centery - jugador.rect.centery
                )

                if distancia < 300:

                    moneda.atraer(
                        jugador.rect.centerx,
                        jugador.rect.centery,
                        8
                    )


            # Si la moneda salió por abajo
            if moneda.esta_fuera(ALTO):

                reubicar_moneda(
                    moneda,
                    obstaculos
                )


            # Detectar colisión con jugador
            if jugador.rect.colliderect(
                moneda.rect
            ):

                combo += 1

                multiplicador = calcular_multiplicador(combo)

                puntos += multiplicador
                sonido_moneda.play()

                ambiente.efecto_moneda(
                    moneda.rect.centerx,
                    moneda.rect.centery
                )

                agregar_texto_flotante(
                    f"+{multiplicador}",
                    moneda.rect.centerx,
                    moneda.rect.top,
                    AMARILLO
                )

                # Aviso cuando sube el combo
                if (
                    combo % MONEDAS_POR_COMBO == 0
                    and combo // MONEDAS_POR_COMBO < MULTIPLICADOR_MAXIMO
                ):

                    agregar_texto_flotante(
                        f"COMBO x{multiplicador}",
                        jugador.rect.centerx,
                        jugador.rect.top - 20,
                        NARANJA
                    )

                # Mandar moneda nuevamente arriba
                reubicar_moneda(
                    moneda,
                    obstaculos
                )


        # --------------------------------------------------
        # ACTUALIZAR OBSTÁCULOS
        # --------------------------------------------------

        for obstaculo in obstaculos:

            if estado != "jugando":
                break

            # Durante el jefe, los que están arriba esperan
            if jefe_activo and obstaculo.rect.bottom < 0:
                continue

            obstaculo.actualizar(
                velocidad_objetos
            )


            # Si salió por abajo
            if obstaculo.esta_fuera(ALTO):

                reubicar_obstaculo(
                    obstaculo,
                    monedas
                )


            # Detectar colisión
            if jugador.rect.colliderect(
                obstaculo.rect
            ):

                # Con escudo: el meteorito se destruye
                if jugador.tiene_escudo():

                    escudo_absorbe(
                        obstaculo.rect.centerx,
                        obstaculo.rect.centery
                    )

                    reubicar_obstaculo(
                        obstaculo,
                        monedas
                    )

                # Recién golpeado: no pasa nada
                elif jugador.es_invulnerable():

                    pass

                else:

                    golpear_jugador(
                        jugador.rect.centerx,
                        jugador.rect.centery
                    )

                    # Reiniciar obstáculo
                    reubicar_obstaculo(
                        obstaculo,
                        monedas
                    )


        # --------------------------------------------------
        # DISPAROS DE LA NAVE
        # --------------------------------------------------

        if (
            estado == "jugando"
            and jugador.tiene_arma()
            and tiempo_transcurrido >= siguiente_bala
        ):

            siguiente_bala = tiempo_transcurrido + CADENCIA_DISPARO

            # Una bala desde cada ala
            for x, y in jugador.puntos_de_disparo():

                balas.append({
                    "x": x,
                    "y": y - 8
                })

            sonidos["disparo_nave"].play()

        for bala in balas[:]:

            bala["y"] -= VELOCIDAD_BALA

            rect_bala = pygame.Rect(0, 0, 6, 18)
            rect_bala.center = (bala["x"], bala["y"])

            # Salió por arriba
            if rect_bala.bottom < 0:

                balas.remove(bala)

                continue

            acerto = False

            # Contra los meteoritos
            for obstaculo in obstaculos:

                if obstaculo.rect.bottom > 0 and rect_bala.colliderect(obstaculo.rect):

                    acerto = True

                    puntos += 1

                    sonidos["meteorito_roto"].play()

                    ambiente.efecto_golpe(
                        obstaculo.rect.centerx,
                        obstaculo.rect.centery
                    )

                    agregar_texto_flotante(
                        "+1",
                        obstaculo.rect.centerx,
                        obstaculo.rect.centery,
                        (255, 170, 60)
                    )

                    reubicar_obstaculo(
                        obstaculo,
                        monedas
                    )

                    break

            # Contra el jefe (brilla, pero hay que sobrevivir igual)
            if not acerto and jefe is not None:

                cuerpo = jefe.rect_cuerpo()

                if cuerpo is not None and rect_bala.colliderect(cuerpo):

                    acerto = True

                    jefe.recibir_impacto(bala["x"], cuerpo.bottom - 10)

                    sonidos["impacto_jefe"].play()

            if acerto:

                balas.remove(bala)


        # --------------------------------------------------
        # OBJETOS ESPECIALES
        # --------------------------------------------------

        if estado != "jugando":

            # Se acabó la partida en este mismo cuadro
            pass

        elif tiempo_transcurrido >= siguiente_potenciador and not potenciadores:

            potenciadores.append(Potenciador(ANCHO))

            siguiente_potenciador = (
                tiempo_transcurrido + random.uniform(8, 14)
            )

        for potenciador in potenciadores[:]:

            potenciador.actualizar(velocidad_objetos)

            if potenciador.esta_fuera(ALTO):

                potenciadores.remove(potenciador)

                continue

            if estado == "jugando" and jugador.rect.colliderect(potenciador.rect):

                potenciadores.remove(potenciador)

                sonidos["potenciador"].play()

                ambiente.efecto_moneda(
                    potenciador.rect.centerx,
                    potenciador.rect.centery
                )

                x = potenciador.rect.centerx
                y = potenciador.rect.top

                if potenciador.tipo == "moneda_grande":

                    combo += 1

                    ganados = 5 * calcular_multiplicador(combo)

                    puntos += ganados

                    agregar_texto_flotante(f"+{ganados}", x, y, AMARILLO)

                elif potenciador.tipo == "corazon":

                    if vidas < config["vidas_maximas"]:

                        vidas += 1

                        agregar_texto_flotante("+1 VIDA", x, y, ROJO)

                    else:

                        # Con las vidas llenas da puntos extra
                        puntos += 3

                        agregar_texto_flotante("+3", x, y, ROJO)

                elif potenciador.tipo == "escudo":

                    jugador.activar_escudo(config["duracion_escudo"])

                    agregar_texto_flotante("ESCUDO", x, y, (80, 200, 255))

                elif potenciador.tipo == "iman":

                    jugador.activar_iman(config["duracion_iman"])

                    agregar_texto_flotante("IMÁN", x, y, (200, 90, 255))

                elif potenciador.tipo == "arma":

                    jugador.activar_arma(DURACION_ARMA)

                    agregar_texto_flotante("¡DISPARO!", x, y, (255, 150, 40))


        # --------------------------------------------------
        # SUBIR DE NIVEL
        # --------------------------------------------------

        nivel_actual = 1 + puntos // PUNTOS_POR_NIVEL

        if nivel_actual > nivel and estado == "jugando":

            nivel = nivel_actual

            mensaje_nivel = f"NIVEL {nivel}"
            mensaje_nivel_hasta = tiempo_transcurrido + 2

            sonidos["nivel"].play()


        # --------------------------------------------------
        # TROFEOS
        # --------------------------------------------------

        if estado == "jugando":

            for datos_trofeo in TROFEOS:

                clave = datos_trofeo[0]
                puntos_necesarios = datos_trofeo[2]

                if puntos >= puntos_necesarios and clave not in trofeos_partida:

                    trofeos_partida.append(clave)

                    es_nuevo = clave not in datos_modo()["trofeos"]

                    modo_abierto = None
                    colores_nuevos = []

                    # Guardar el trofeo en el archivo
                    if es_nuevo:

                        datos_modo()["trofeos"].append(clave)
                        guardar_progreso(progreso)

                        modo_abierto = modo_que_desbloquea(clave)
                        colores_nuevos = colores_que_desbloquea(clave)

                    trofeo_mostrado = (
                        datos_trofeo,
                        es_nuevo,
                        modo_abierto,
                        colores_nuevos
                    )

                    if modo_abierto is not None:
                        sonidos["desbloqueo"].play()
                    else:
                        sonidos["trofeo"].play()

                    pausar("trofeo")

                    # Solo un trofeo a la vez
                    break


        # --------------------------------------------------
        # TEXTOS FLOTANTES
        # --------------------------------------------------

        for texto in textos_flotantes[:]:

            texto["y"] -= 1.2
            texto["vida"] -= 1

            if texto["vida"] <= 0:

                textos_flotantes.remove(texto)


        # --------------------------------------------------
        # SACUDIDA
        # --------------------------------------------------

        if temblor > 0:

            temblor -= 1


    # ======================================================
    # DIBUJAR FONDO
    # ======================================================

    # Todo el juego se dibuja en el lienzo y luego se pega
    # en la pantalla (movido si hay sacudida)

    ambiente.dibujar(
        lienzo,
        jugador
    )


    # ======================================================
    # DIBUJAR MONEDAS
    # ======================================================

    for moneda in monedas:

        moneda.dibujar(
            lienzo
        )


    # ======================================================
    # DIBUJAR OBJETOS ESPECIALES
    # ======================================================

    for potenciador in potenciadores:

        potenciador.dibujar(
            lienzo
        )


    # ======================================================
    # DIBUJAR OBSTÁCULOS
    # ======================================================

    for obstaculo in obstaculos:

        obstaculo.dibujar(
            lienzo
        )


    # ======================================================
    # DIBUJAR JEFE
    # ======================================================

    if jefe is not None:

        jefe.dibujar(
            lienzo
        )


    # ======================================================
    # DIBUJAR BALAS
    # ======================================================

    for bala in balas:

        x = int(bala["x"])
        y = int(bala["y"])

        brillo = pygame.Surface((18, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(brillo, (255, 190, 80, 120), (0, 0, 18, 30))
        lienzo.blit(brillo, (x - 9, y - 15))

        pygame.draw.ellipse(lienzo, (255, 210, 70), (x - 4, y - 10, 8, 20))
        pygame.draw.ellipse(lienzo, (255, 255, 230), (x - 2, y - 7, 4, 12))


    # ======================================================
    # DIBUJAR JUGADOR
    # ======================================================

    if estado != "game_over":

        jugador.dibujar(
            lienzo
        )


    # ======================================================
    # TEXTOS FLOTANTES
    # ======================================================

    for texto in textos_flotantes:

        superficie = fuente.render(texto["texto"], True, texto["color"])

        superficie.set_alpha(min(255, texto["vida"] * 8))

        lienzo.blit(
            superficie,
            superficie.get_rect(center=(int(texto["x"]), int(texto["y"])))
        )


    # ======================================================
    # PEGAR EL LIENZO (CON SACUDIDA)
    # ======================================================

    desplazamiento = (0, 0)

    if temblor > 0 and estado == "jugando":

        fuerza = max(1, temblor // 2)

        desplazamiento = (
            random.randint(-fuerza, fuerza),
            random.randint(-fuerza, fuerza)
        )

    pantalla.fill(NEGRO)

    pantalla.blit(
        lienzo,
        desplazamiento
    )


    # ======================================================
    # INFORMACIÓN EN PANTALLA
    # ======================================================

    if estado != "game_over":

        dibujar_hud()

    # ======================================================
    # PANTALLAS ENCIMA DEL JUEGO
    # ======================================================

    if estado == "pausa":

        dibujar_pausa()

    elif estado == "trofeo":

        dibujar_trofeo_ganado()

    elif estado == "game_over":

        dibujar_game_over()


    # ======================================================
    # ACTUALIZAR PANTALLA
    # ======================================================

    presentar(pantalla)


    # Mantener 60 FPS
    reloj.tick(FPS)


# ==========================================================
# CERRAR PYGAME
# ==========================================================

pygame.mixer.music.stop()
pygame.quit()

sys.exit()
