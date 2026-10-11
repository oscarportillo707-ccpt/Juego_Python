import pygame
import sys
import random
import math

from jugador import Jugador
from moneda import Moneda
from obstaculo import Obstaculo

from ambiente import Ambiente


# ==========================================================
# INICIALIZAR PYGAME
# ==========================================================

pygame.init()


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

 
        # ==================================================
        # PARTE SUPERIOR
        # ==================================================
 
        texto_nombre = fuente_pequena.render(
            "JUEGO DE MONEDAS",
            True,
            CREMA
        )
 
        pantalla.blit(texto_nombre, (60, 60))
 
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
            "EXPEDICCIÓN 33",
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
    # Monedas
    # --------------------------

    monedas = []

    for i in range(4):

        x = random.randint(
            0,
            ANCHO - 30
        )

        y = random.randint(
            -700,
            -100
        )

        moneda = Moneda(x, y)

        monedas.append(moneda)


    # --------------------------
    # Obstáculos
    # --------------------------

    obstaculos = []

    for i in range(3):

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
    # Puntuación
    # --------------------------

    puntos = 0


    # --------------------------
    # Vidas
    # --------------------------

    vidas = 3


    # --------------------------
    # Velocidad inicial
    # --------------------------


    # --------------------------
    # Tiempo de inicio
    # --------------------------

    tiempo_inicio = pygame.time.get_ticks()


    return (
        jugador,
        monedas,
        obstaculos,
        puntos,
        vidas,
        tiempo_inicio
    )


# ==========================================================
# INICIAR LA PARTIDA
# ==========================================================

(
    jugador,
    monedas,
    obstaculos,
    puntos,
    vidas,
    tiempo_inicio
) = iniciar_juego()


# Estado del juego
juego_terminado = False


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

            # Si estamos en Game Over
            if juego_terminado:

                # Presionar R para reiniciar
                if evento.key == pygame.K_r:

                    (
                        jugador,
                        monedas,
                        obstaculos,
                        puntos,
                        vidas,
                        tiempo_inicio
                    ) = iniciar_juego()

                    juego_terminado = False


                # ESC para salir
                if evento.key == pygame.K_ESCAPE:

                    ejecutando = False


    # ======================================================
    # TECLAS
    # ======================================================

    teclas = pygame.key.get_pressed()


    # ======================================================
    # ACTUALIZAR JUEGO
    # ======================================================

    if not juego_terminado:

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


        # --------------------------------------------------
        # AUMENTAR VELOCIDAD
        # --------------------------------------------------

        # Empieza lento y aumenta progresivamente.
        #
        # 2.0 = velocidad inicial
        # 0.08 = cuánto aumenta por segundo

        velocidad_objetos = 3 + tiempo_transcurrido * 0.08


        # --------------------------------------------------
        # ACTUALIZAR MONEDAS
        # --------------------------------------------------

        for moneda in monedas:

            moneda.actualizar(
                velocidad_objetos
            )


            # Si la moneda salió por abajo
            if moneda.esta_fuera(ALTO):

                moneda.reiniciar(
                    ANCHO
                )


            # Detectar colisión con jugador
            if jugador.rect.colliderect(
                moneda.rect
            ):
                
                puntos += 1

                ambiente.efecto_moneda(
                    moneda.rect.centerx,
                    moneda.rect.centery
                )

                # Mandar moneda nuevamente arriba
                moneda.reiniciar(
                    ANCHO
                )


        # --------------------------------------------------
        # ACTUALIZAR OBSTÁCULOS
        # --------------------------------------------------

        for obstaculo in obstaculos:

            obstaculo.actualizar(
                velocidad_objetos
            )


            # Si salió por abajo
            if obstaculo.esta_fuera(ALTO):

                obstaculo.reiniciar(
                    ANCHO
                )


            # Detectar colisión
            if jugador.rect.colliderect(
                obstaculo.rect
            ):

                # Quitar una vida
                vidas -= 1

                # Reiniciar obstáculo
                obstaculo.reiniciar(
                    ANCHO
                )


                # Si no quedan vidas
                if vidas <= 0:

                    juego_terminado = True


    # ======================================================
    # DIBUJAR FONDO
    # ======================================================

    ambiente.dibujar(
        pantalla,
        jugador
    )


    # ======================================================
    # DIBUJAR MONEDAS
    # ======================================================

    for moneda in monedas:

        moneda.dibujar(
            pantalla
        )


    # ======================================================
    # DIBUJAR OBSTÁCULOS
    # ======================================================

    for obstaculo in obstaculos:

        obstaculo.dibujar(
            pantalla
        )


    # ======================================================
    # DIBUJAR JUGADOR
    # ======================================================

    jugador.dibujar(
        pantalla
    )


    # ======================================================
    # INFORMACIÓN EN PANTALLA
    # ======================================================

    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_puntos,
        (20, 20)
    )


    texto_vidas = fuente.render(
        f"Vidas: {vidas}",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_vidas,
        (20, 55)
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
    if not juego_terminado:

        texto_tiempo = fuente_pequeña.render(
            f"Tiempo: {tiempo_transcurrido:.0f}s",
            True,
            BLANCO
        )

        pantalla.blit(
            texto_tiempo,
            (ANCHO - 160, 55)
        )


    # ======================================================
    # GAME OVER
    # ======================================================

    if juego_terminado:

        # Fondo semitransparente
        capa = pygame.Surface(
            (ANCHO, ALTO),
            pygame.SRCALPHA
        )

        capa.fill(
            (0, 0, 0, 180)
        )

        pantalla.blit(
            capa,
            (0, 0)
        )


        # Texto GAME OVER
        texto_game_over = fuente_grande.render(
            "GAME OVER",
            True,
            ROJO
        )

        rect_game_over = texto_game_over.get_rect(
            center=(
                ANCHO // 2,
                ALTO // 2 - 60
            )
        )

        pantalla.blit(
            texto_game_over,
            rect_game_over
        )


        # Puntuación final
        texto_final = fuente.render(
            f"Puntuación: {puntos}",
            True,
            BLANCO
        )

        rect_final = texto_final.get_rect(
            center=(
                ANCHO // 2,
                ALTO // 2 + 20
            )
        )

        pantalla.blit(
            texto_final,
            rect_final
        )


        # Instrucción para reiniciar
        texto_reiniciar = fuente_pequeña.render(
            "Presiona R para volver a jugar",
            True,
            BLANCO
        )

        rect_reiniciar = texto_reiniciar.get_rect(
            center=(
                ANCHO // 2,
                ALTO // 2 + 70
            )
        )

        pantalla.blit(
            texto_reiniciar,
            rect_reiniciar
        )


    # ======================================================
    # ACTUALIZAR PANTALLA
    # ======================================================

    pygame.display.flip()


    # Mantener 60 FPS
    reloj.tick(FPS)


# ==========================================================
# CERRAR PYGAME
# ==========================================================

pygame.quit()

sys.exit()