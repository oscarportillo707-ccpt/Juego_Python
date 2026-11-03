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


# ==========================================================
# INICIALIZAR PYGAME
# ==========================================================

## sonidos de la nave y de los meteoritos

pygame.init()

carpeta_sonidos = os.path.join(
    os.path.dirname(__file__),
    "sonidos"
)
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

pantalla = pygame.display.set_mode(
    (ANCHO, ALTO)
)

pygame.display.set_caption(
    "Juego de Monedas"
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
 
    # Devuelve True si el jugador elige SÍ (empezar el juego)
    # y False si elige NO, presiona ESC o cierra la ventana.
 
    # Fuentes
    fuente_titulo = pygame.font.Font(None, 170)
    fuente = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 28)
 
    # Opción seleccionada: 0 = SÍ, 1 = NO
    opcion = 0
 
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
                    return opcion == 0
 
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

        marco = pygame.Rect(30, 30, ANCHO - 60, ALTO - 60)
        pygame.draw.rect(pantalla, AZUL_APAGADO, marco, 4, border_radius=30)

        

 
        # ==================================================
        # PARTE SUPERIOR
        # ==================================================
 
        texto_nombre = fuente_pequena.render(
            "JUEGO DE MONEDAS",
            True,
            CREMA
        )
 
        pantalla.blit(texto_nombre, (60, 60))

        texto_record = fuente_pequena.render(
            f"RÉCORD: {progreso['record']}",
            True,
            NARANJA
        )

        pantalla.blit(texto_record, (60, 88))

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
 
        opciones = ["SÍ", "NO"]
 
        posiciones = [ancho // 2 - 100, ancho // 2 + 100]
 
        for i in range(2):
 
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
 
        # ==================================================
        # TROFEOS GANADOS
        # ==================================================

        dibujar_coleccion(
            pantalla,
            ancho // 2,
            135,
            0.42,
            progreso["trofeos"],
            None,
            separacion=45
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
 
        # ==================================================
        # ACTUALIZAR PANTALLA
        # ==================================================
 
        pygame.display.flip()
 
        reloj.tick(fps)

# ==========================================================
# MOSTRAR LA PANTALLA DE INICIO
# ==========================================================

if not pantalla_inicio(pantalla, ANCHO, ALTO, reloj, FPS):
    pygame.quit()
    sys.exit()

pygame.mixer.music.play(loops=-1)


# ==========================================================
# REGLAS DE LA PARTIDA
# ==========================================================

VIDAS_INICIALES = 3
VIDAS_MAXIMAS = 5

# Cada cuántos puntos se sube de nivel
PUNTOS_POR_NIVEL = 25

# Cuántas monedas seguidas hacen subir el multiplicador
MONEDAS_POR_COMBO = 5
MULTIPLICADOR_MAXIMO = 5

# Cantidad de meteoritos
OBSTACULOS_INICIALES = 3
OBSTACULOS_MAXIMOS = 8

# Cada cuántos segundos aparece un meteorito más
SEGUNDOS_POR_OBSTACULO = 20

# Duración de los efectos (segundos)
DURACION_INVULNERABLE = 1.5
DURACION_ESCUDO = 5
DURACION_IMAN = 6

# Jefes y disparos: para ganar cada trofeo hay que vencer antes a su jefe
# (el jefe y su imagen jefe.png están definidos más arriba en este archivo)
COOLDOWN_DISPARO = 12   # cuadros entre un disparo y el siguiente

# Lienzo donde se dibuja el juego (para poder sacudir la pantalla)
lienzo = pygame.Surface((ANCHO, ALTO))

fuente_titulo = pygame.font.Font(None, 110)
fuente_trofeo = pygame.font.Font(None, 58)


# ==========================================================
# JEFE SIMPLE (usa la imagen jefe.png)
# ==========================================================

# Un jefe por trofeo: bronce, plata, oro, diamante
JEFE_NOMBRES = ["JEFE BRONCE", "JEFE PLATA", "JEFE ORO", "JEFE FINAL"]
JEFE_VIDA = [15, 22, 30, 40]            # golpes que aguanta
JEFE_RECOMPENSA = [10, 15, 20, 30]      # puntos al derrotarlo
JEFE_ESPERA = [80, 70, 60, 50]          # cuadros entre disparos
JEFE_BALAS = [1, 2, 3, 3]               # balas por disparo
JEFE_VEL_BALA = [4, 4.5, 5, 5.5]        # velocidad de sus balas

CARPETA_JUEGO = os.path.dirname(os.path.abspath(__file__))


class Bala:

    # Disparo del jugador (sube)

    def __init__(self, x, y):

        self.rect = pygame.Rect(0, 0, 6, 18)
        self.rect.center = (x, y)

    def actualizar(self):

        self.rect.y -= 11

    def esta_fuera(self):

        return self.rect.bottom < 0

    def dibujar(self, pantalla):

        pygame.draw.rect(pantalla, (255, 240, 120), self.rect, border_radius=3)


class BalaJefe:

    # Disparo del jefe (avanza en línea recta)

    def __init__(self, x, y, vx, vy):

        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = (int(x), int(y))

    def actualizar(self):

        self.x += self.vx
        self.y += self.vy

        self.rect.center = (int(self.x), int(self.y))

    def esta_fuera(self, ancho, alto):

        return (
            self.rect.top > alto
            or self.rect.bottom < 0
            or self.rect.right < 0
            or self.rect.left > ancho
        )

    def dibujar(self, pantalla):

        pygame.draw.circle(pantalla, (255, 90, 60), self.rect.center, 8)
        pygame.draw.circle(pantalla, (255, 255, 255), self.rect.center, 3)


class Jefe:

    def __init__(self, ancho_pantalla, tipo=0):

        tipo = max(0, min(tipo, len(JEFE_VIDA) - 1))

        self.tipo = tipo
        self.nombre = JEFE_NOMBRES[tipo]
        self.vida_max = JEFE_VIDA[tipo]
        self.vida = self.vida_max
        self.recompensa = JEFE_RECOMPENSA[tipo]

        self.ancho_pantalla = ancho_pantalla

        # Imagen del jefe (igual que el jugador y el meteorito)
        try:
            self.imagen = pygame.image.load(
                os.path.join(CARPETA_JUEGO, "jefe.png")
            ).convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Si falta la imagen, se usa un cuadro rojo para no cerrar el juego
            self.imagen = pygame.Surface((160, 110))
            self.imagen.fill((200, 40, 60))

        # Imagen en blanco que se muestra un instante al recibir un golpe
        self.imagen_golpe = self.imagen.copy()
        self.imagen_golpe.fill((120, 120, 120), special_flags=pygame.BLEND_RGB_ADD)

        # Empieza arriba, fuera de la pantalla, y baja
        self.rect = self.imagen.get_rect()
        self.rect.centerx = ancho_pantalla // 2
        self.rect.bottom = 0

        self.y_objetivo = 90
        self.entrando = True

        self.t = 0
        self.espera_disparo = 60
        self.destello = 0

        self.fuente = pygame.font.Font(None, 24)

    def puede_recibir_dano(self):

        return not self.entrando

    def recibir_golpe(self):

        self.vida -= 1
        self.destello = 5

    def derrotado(self):

        return self.vida <= 0

    def actualizar(self, rect_jugador):

        # Devuelve la lista de balas nuevas (vacía si no disparó)

        self.t += 1

        if self.destello > 0:
            self.destello -= 1

        # Baja hasta su lugar
        if self.entrando:

            self.rect.y += 2

            if self.rect.y >= self.y_objetivo:
                self.rect.y = self.y_objetivo
                self.entrando = False

            return []

        # Se mueve de lado a lado
        recorrido = self.ancho_pantalla // 2 - self.rect.width // 2 - 20

        self.rect.centerx = (
            self.ancho_pantalla // 2
            + int(math.sin(self.t * 0.025) * recorrido)
        )

        # Dispara hacia el jugador
        self.espera_disparo -= 1

        if self.espera_disparo > 0:
            return []

        self.espera_disparo = JEFE_ESPERA[self.tipo]

        origen_x = self.rect.centerx
        origen_y = self.rect.bottom - 10

        angulo = math.atan2(
            rect_jugador.centery - origen_y,
            rect_jugador.centerx - origen_x
        )

        cantidad = JEFE_BALAS[self.tipo]
        velocidad = JEFE_VEL_BALA[self.tipo]

        nuevas = []

        for i in range(cantidad):

            desvio = (i - (cantidad - 1) / 2) * 0.3

            nuevas.append(
                BalaJefe(
                    origen_x,
                    origen_y,
                    math.cos(angulo + desvio) * velocidad,
                    math.sin(angulo + desvio) * velocidad
                )
            )

        return nuevas

    def dibujar(self, pantalla):

        if self.destello > 0:
            pantalla.blit(self.imagen_golpe, self.rect)
        else:
            pantalla.blit(self.imagen, self.rect)

        # Barra de vida
        ancho = self.rect.width
        proporcion = max(0, self.vida) / self.vida_max

        pygame.draw.rect(
            pantalla, (60, 60, 70),
            (self.rect.x, self.rect.bottom + 6, ancho, 8),
            border_radius=4
        )

        if proporcion > 0.5:
            color = (60, 220, 100)
        elif proporcion > 0.25:
            color = (255, 200, 0)
        else:
            color = (220, 60, 60)

        pygame.draw.rect(
            pantalla, color,
            (self.rect.x, self.rect.bottom + 6, int(ancho * proporcion), 8),
            border_radius=4
        )

        # Nombre
        texto = self.fuente.render(self.nombre, True, (255, 235, 190))

        pantalla.blit(
            texto,
            texto.get_rect(center=(self.rect.centerx, self.rect.bottom + 28))
        )


print("[JEFES] Versión con jefes simples cargada")


# ==========================================================
# FUNCIONES DE AYUDA
# ==========================================================

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
    # Jugador
    # --------------------------

    jugador = Jugador(
        ANCHO // 2 - 30,
        SUELO - 70
    )


    # --------------------------
    # Obstáculos
    # --------------------------

    obstaculos = []

    for i in range(OBSTACULOS_INICIALES):

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

    vidas = VIDAS_INICIALES


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


# Estado del juego:
# "jugando", "pausa", "trofeo" o "game_over"
estado = "jugando"

# Momento en que empezó la pausa (o el trofeo)
inicio_pausa = 0

# Trofeo que se está mostrando: (datos del trofeo, es_nuevo)
trofeo_mostrado = None

# Textos que suben y desaparecen ("+1", "+5", "ESCUDO"...)
textos_flotantes = []

# Mensaje grande de nivel
mensaje_nivel = ""
mensaje_nivel_hasta = 0

# Sacudida de la pantalla
temblor = 0

# Datos del Game Over
nuevo_record = False
opcion_game_over = 0

tiempo_transcurrido = 0
velocidad_objetos = 3

# Jefes y disparos
puede_disparar = False
balas = []
balas_jefe = []
jefe = None
jefe_trofeo = None      # número del trofeo cuyo jefe está peleando ahora
cooldown_disparo = 0
fin_partida = 0         # momento en que terminó la última partida


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

    global estado, nuevo_record, fin_partida

    estado = "game_over"
    fin_partida = pygame.time.get_ticks()

    pygame.mixer.music.fadeout(800)
    sonidos["game_over"].play()

    # Guardar el récord
    nuevo_record = puntos > progreso["record"]

    if nuevo_record:

        progreso["record"] = puntos
        guardar_progreso(progreso)


def golpe_de_bala_jefe():

    # Una bala del jefe toca al jugador (funciona igual que
    # chocar con un meteorito: el escudo la bloquea)
    global vidas, combo, temblor

    if jugador.tiene_escudo():

        sonidos["escudo"].play()

        ambiente.efecto_golpe(
            jugador.rect.centerx,
            jugador.rect.centery
        )

    elif not jugador.es_invulnerable():

        sonido_meteorito.play()

        vidas -= 1

        combo = 0

        jugador.recibir_golpe(DURACION_INVULNERABLE)

        ambiente.efecto_golpe(
            jugador.rect.centerx,
            jugador.rect.centery
        )

        temblor = 18


def reiniciar_partida():

    global jugador, monedas, obstaculos, potenciadores
    global puntos, vidas, combo, nivel, trofeos_partida
    global siguiente_potenciador, tiempo_inicio
    global estado, textos_flotantes, mensaje_nivel, temblor
    global opcion_game_over
    global puede_disparar, balas, balas_jefe, jefe, jefe_trofeo, cooldown_disparo

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

    puede_disparar = False
    balas = []
    balas_jefe = []
    jefe = None
    jefe_trofeo = None
    cooldown_disparo = 0

    pygame.mixer.music.play(loops=-1)


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
    for i in range(VIDAS_MAXIMAS):

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


    # Mostrar récord
    texto_record = fuente_pequeña.render(
        f"Récord: {max(puntos, progreso['record'])}",
        True,
        CREMA
    )

    pantalla.blit(
        texto_record,
        (ANCHO - 160, 115)
    )


    # Recordatorio de cómo disparar
    if puede_disparar:

        texto_disparo = fuente_pequeña.render(
            "ESPACIO: disparar",
            True,
            VERDE
        )

        pantalla.blit(
            texto_disparo,
            (ANCHO - 190, ALTO - 30)
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


    # Barras de tiempo del escudo y del imán
    y_barra = ALTO - 30

    efectos = [
        ("ESCUDO", jugador.escudo_hasta, DURACION_ESCUDO, (80, 200, 255)),
        ("IMÁN", jugador.iman_hasta, DURACION_IMAN, (200, 90, 255)),
    ]

    for nombre, hasta, duracion, color in efectos:

        restante = hasta - tiempo_transcurrido

        if restante > 0:

            texto = fuente_pequeña.render(nombre, True, color)
            pantalla.blit(texto, (20, y_barra - 4))

            pygame.draw.rect(pantalla, GRIS, (110, y_barra, 150, 12), border_radius=6)

            pygame.draw.rect(
                pantalla,
                color,
                (110, y_barra, int(150 * restante / duracion), 12),
                border_radius=6
            )

            y_barra -= 28


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


def dibujar_pausa():

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((5, 10, 30, 190))
    pantalla.blit(capa, (0, 0))

    sombra = fuente_titulo.render("PAUSA", True, NARANJA_SOMBRA)
    titulo = fuente_titulo.render("PAUSA", True, NARANJA)

    rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 60))

    pantalla.blit(sombra, rect.move(5, 5))
    pantalla.blit(titulo, rect)

    lineas = [
        "P o ESC para continuar",
        "Q para salir del juego"
    ]

    for i, linea in enumerate(lineas):

        texto = fuente_pequeña.render(linea, True, CREMA)

        pantalla.blit(
            texto,
            texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 20 + i * 35))
        )


def dibujar_trofeo_ganado():

    datos, es_nuevo = trofeo_mostrado
    clave, nombre, req, color, sombra_trofeo = datos

    # Fuente para "NIVEL MASTER"
    fuente_master = pygame.font.Font(None, 48)

    segundos = (pygame.time.get_ticks() - inicio_pausa) / 1000

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((5, 10, 30, 210))
    pantalla.blit(capa, (0, 0))

    cx = ANCHO // 2
    cy = ALTO // 2 - 40

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

        # "NIVEL MASTER" cambia de color como un brillo
        onda = (math.sin(segundos * 4) + 1) / 2

        color_master = (
            int(120 + onda * 135),
            int(225 + onda * 30),
            255
        )

        sombra_master = fuente_master.render("NIVEL MASTER", True, sombra_trofeo)
        texto_master = fuente_master.render("NIVEL MASTER", True, color_master)

        rect_master = texto_master.get_rect(center=(cx, cy - 150))

        pantalla.blit(sombra_master, rect_master.move(3, 3))
        pantalla.blit(texto_master, rect_master)

    else:

        titulo = fuente_trofeo.render(f"¡TROFEO DE {nombre}!", True, color)

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(cx, cy - 160))
        )

    texto_puntos = fuente.render(f"Llegaste a {req} puntos", True, CREMA)

    pantalla.blit(
        texto_puntos,
        texto_puntos.get_rect(center=(cx, cy + 150))
    )

    if es_nuevo:
        subtitulo = "¡NUEVO TROFEO GUARDADO!"
    else:
        subtitulo = "Ya tenías este trofeo"

    texto_sub = fuente_pequeña.render(subtitulo, True, AMARILLO)

    pantalla.blit(
        texto_sub,
        texto_sub.get_rect(center=(cx, cy + 190))
    )

    if segundos > 1:

        texto_seguir = fuente_pequeña.render(
            "Presiona cualquier tecla para continuar",
            True,
            AZUL_APAGADO
        )

        pantalla.blit(
            texto_seguir,
            texto_seguir.get_rect(center=(cx, ALTO - 50))
        )


def dibujar_game_over():

    # Fondo azul semitransparente (mismo estilo que el menú)
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((15, 30, 65, 225))
    pantalla.blit(capa, (0, 0))

    marco = pygame.Rect(30, 30, ANCHO - 60, ALTO - 60)
    pygame.draw.rect(pantalla, AZUL_APAGADO, marco, 4, border_radius=30)

    # Título
    sombra = fuente_titulo.render("GAME OVER", True, NARANJA_SOMBRA)
    titulo = fuente_titulo.render("GAME OVER", True, NARANJA)

    rect_titulo = titulo.get_rect(center=(ANCHO // 2, 120))

    pantalla.blit(sombra, rect_titulo.move(5, 5))
    pantalla.blit(titulo, rect_titulo)

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
        f"Récord: {progreso['record']}",
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

    # Colección de trofeos
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
        progreso["trofeos"],
        fuente_pequeña
    )

    # Pregunta y opciones
    texto_otra = fuente.render("¿JUGAR OTRA VEZ?", True, CREMA)

    pantalla.blit(
        texto_otra,
        texto_otra.get_rect(center=(ANCHO // 2, 505))
    )

    opciones = ["SÍ", "NO"]

    posiciones = [ANCHO // 2 - 100, ANCHO // 2 + 100]

    for i in range(2):

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


        # Teclas presionadas
        if evento.type == pygame.KEYDOWN:

            # Al terminar la partida se ignoran las teclas un momento,
            # para no saltarse el Game Over sin querer al disparar
            if (
                estado == "game_over"
                and pygame.time.get_ticks() - fin_partida < 600
            ):
                continue

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

                if evento.key == pygame.K_q:

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
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_w,
                    pygame.K_s
                ):
                    opcion_game_over = 1 - opcion_game_over

                # Confirmar
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                    if opcion_game_over == 0:
                        reiniciar_partida()
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

        # Empieza lento y aumenta progresivamente.
        #
        # 3 = velocidad inicial
        # 0.08 = cuánto aumenta por segundo
        # 0.25 = cuánto aumenta por cada nivel

        velocidad_objetos = (
            3
            + tiempo_transcurrido * 0.08
            + (nivel - 1) * 0.25
        )


        # --------------------------------------------------
        # MÁS METEORITOS CON EL TIEMPO
        # --------------------------------------------------

        cantidad_obstaculos = min(
            OBSTACULOS_MAXIMOS,
            OBSTACULOS_INICIALES
            + int(tiempo_transcurrido // SEGUNDOS_POR_OBSTACULO)
        )

        while len(obstaculos) < cantidad_obstaculos:

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

            # Mientras hay un jefe no llegan meteoritos nuevos:
            # los que ya están en pantalla terminan de caer y
            # los demás esperan arriba hasta que el jefe caiga.
            if jefe is not None:

                # Todavía no se ve: se queda esperando arriba
                if obstaculo.rect.bottom <= 0:

                    continue

                # Ya salió por abajo: vuelve a la zona de espera
                if obstaculo.esta_fuera(ALTO):

                    reubicar_obstaculo(
                        obstaculo,
                        monedas
                    )

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

                    sonidos["escudo"].play()

                    ambiente.efecto_golpe(
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

                    sonido_meteorito.play()

                    # Quitar una vida
                    vidas -= 1

                    # Se pierde el combo
                    combo = 0

                    jugador.recibir_golpe(DURACION_INVULNERABLE)

                    ambiente.efecto_golpe(
                        jugador.rect.centerx,
                        jugador.rect.centery
                    )

                    # Sacudir la pantalla
                    temblor = 18

                    # Reiniciar obstáculo
                    reubicar_obstaculo(
                        obstaculo,
                        monedas
                    )


                    # Si no quedan vidas
                    if vidas <= 0:

                        terminar_partida()

                        break


        # --------------------------------------------------
        # OBJETOS ESPECIALES
        # --------------------------------------------------

        # Aparece uno nuevo cada cierto tiempo
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

                    if vidas < VIDAS_MAXIMAS:

                        vidas += 1

                        agregar_texto_flotante("+1 VIDA", x, y, ROJO)

                    else:

                        # Con las vidas llenas da puntos extra
                        puntos += 3

                        agregar_texto_flotante("+3", x, y, ROJO)

                elif potenciador.tipo == "escudo":

                    jugador.activar_escudo(DURACION_ESCUDO)

                    agregar_texto_flotante("ESCUDO", x, y, (80, 200, 255))

                elif potenciador.tipo == "iman":

                    jugador.activar_iman(DURACION_IMAN)

                    agregar_texto_flotante("IMÁN", x, y, (200, 90, 255))


        # --------------------------------------------------
        # JEFES Y DISPAROS
        # --------------------------------------------------

        if estado == "jugando":

            # Disparar manteniendo ESPACIO
            if cooldown_disparo > 0:

                cooldown_disparo -= 1

            if (
                puede_disparar
                and teclas[pygame.K_SPACE]
                and cooldown_disparo == 0
            ):

                balas.append(
                    Bala(jugador.rect.centerx, jugador.rect.top)
                )

                cooldown_disparo = COOLDOWN_DISPARO


            # Balas del jugador
            for bala in balas[:]:

                bala.actualizar()

                if bala.esta_fuera():

                    balas.remove(bala)

                    continue

                impacto = False

                # Contra los meteoritos
                for obstaculo in obstaculos:

                    if (
                        obstaculo.rect.bottom > 0
                        and bala.rect.colliderect(obstaculo.rect)
                    ):

                        ambiente.efecto_golpe(
                            obstaculo.rect.centerx,
                            obstaculo.rect.centery
                        )

                        reubicar_obstaculo(
                            obstaculo,
                            monedas
                        )

                        impacto = True

                        break

                # Contra el jefe
                if (
                    not impacto
                    and jefe is not None
                    and jefe.puede_recibir_dano()
                    and bala.rect.colliderect(jefe.rect)
                ):

                    jefe.recibir_golpe()

                    ambiente.efecto_golpe(
                        bala.rect.centerx,
                        bala.rect.top
                    )

                    impacto = True

                if impacto:

                    balas.remove(bala)


            # El jefe se mueve y dispara
            if jefe is not None:

                balas_jefe.extend(jefe.actualizar(jugador.rect))

                if jefe.derrotado():

                    puntos += jefe.recompensa

                    agregar_texto_flotante(
                        f"+{jefe.recompensa}",
                        jefe.rect.centerx,
                        jefe.rect.centery,
                        AMARILLO
                    )

                    ambiente.efecto_golpe(
                        jefe.rect.centerx,
                        jefe.rect.centery
                    )

                    # Al vencer al jefe se gana su trofeo
                    datos_trofeo = TROFEOS[jefe_trofeo]
                    clave = datos_trofeo[0]

                    if clave not in trofeos_partida:

                        trofeos_partida.append(clave)

                    es_nuevo = clave not in progreso["trofeos"]

                    # Guardar el trofeo en el archivo
                    if es_nuevo:

                        progreso["trofeos"].append(clave)
                        guardar_progreso(progreso)

                    trofeo_mostrado = (datos_trofeo, es_nuevo)

                    sonidos["trofeo"].play()

                    jefe = None
                    jefe_trofeo = None

                    balas_jefe.clear()

                    pausar("trofeo")


            # Balas del jefe
            for bala_jefe in balas_jefe[:]:

                bala_jefe.actualizar()

                if bala_jefe.esta_fuera(ANCHO, ALTO):

                    balas_jefe.remove(bala_jefe)

                    continue

                if jugador.rect.colliderect(bala_jefe.rect):

                    balas_jefe.remove(bala_jefe)

                    golpe_de_bala_jefe()

                    if vidas <= 0:

                        terminar_partida()

                        break


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

        # Al llegar a los puntos de un trofeo NO se gana todavía:
        # primero aparece su jefe. El trofeo se entrega al derrotarlo.
        if estado == "jugando" and jefe is None:

            for indice, datos_trofeo in enumerate(TROFEOS):

                clave = datos_trofeo[0]
                puntos_necesarios = datos_trofeo[2]

                # Solo importa el próximo trofeo que falta por ganar
                if clave in trofeos_partida:

                    continue

                if puntos >= puntos_necesarios:

                    # El primer jefe desbloquea el disparo
                    if not puede_disparar:

                        puede_disparar = True

                        agregar_texto_flotante(
                            "¡DISPARA CON ESPACIO!",
                            ANCHO // 2,
                            ALTO // 2,
                            VERDE
                        )

                    jefe = Jefe(ANCHO, indice)
                    jefe_trofeo = indice

                    mensaje_nivel = "¡JEFE!"
                    mensaje_nivel_hasta = tiempo_transcurrido + 2

                    sonidos["nivel"].play()

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
    # DIBUJAR DISPAROS Y JEFE
    # ======================================================

    for bala in balas:

        bala.dibujar(
            lienzo
        )


    if jefe is not None:

        jefe.dibujar(
            lienzo
        )


    for bala_jefe in balas_jefe:

        bala_jefe.dibujar(
            lienzo
        )


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

    pygame.display.flip()


    # Mantener 60 FPS
    reloj.tick(FPS)


# ==========================================================
# CERRAR PYGAME
# ==========================================================

pygame.mixer.music.stop()
pygame.quit()

sys.exit()