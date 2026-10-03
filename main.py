import pygame
import sys
import random

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
                        velocidad_objetos,
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

        velocidad_objetos = 2 + tiempo_transcurrido * 0.08


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
    # DIBUJAR ZONA DEL SUELO
    # ======================================================

    pygame.draw.rect(
        pantalla,
        GRIS,
        (
            0,
            SUELO,
            ANCHO,
            ALTO - SUELO
        )
    )


    # Línea superior del suelo
    pygame.draw.line(
        pantalla,
        (100, 100, 110),
        (0, SUELO),
        (ANCHO, SUELO),
        3
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