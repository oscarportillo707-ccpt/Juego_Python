import math
import pygame

from jugador import Jugador

from modos import (
    MODOS,
    ORDEN_MODOS,
    COLORES_NAVE,
    datos_color,
    tinte_nave,
    modo_desbloqueado,
    color_desbloqueado,
    texto_requisito,
    dibujar_estrellas,
    dibujar_candado,
    dibujar_icono_modo
)

from progreso import (
    TROFEOS,
    guardar_progreso,
    dibujar_coleccion
)
from controles_tactiles import ControlesTactiles


# ==========================================================
# COLORES (los mismos de la pantalla de inicio)
# ==========================================================

AZUL = (15, 30, 65)
AZUL_LINEAS = (28, 48, 95)
AZUL_APAGADO = (120, 145, 190)
NARANJA = (255, 150, 30)
NARANJA_SOMBRA = (150, 70, 0)
CREMA = (255, 235, 190)
GRIS_BLOQUEADO = (75, 82, 105)
FONDO_BLOQUEADO = (28, 32, 48)


# ==========================================================
# AYUDAS
# ==========================================================

def dibujar_fondo(pantalla, color_fondo, color_lineas):

    ancho, alto = pantalla.get_size()

    pantalla.fill(color_fondo)

    # Cuadrícula
    for x in range(0, ancho, 50):
        pygame.draw.line(pantalla, color_lineas, (x, 0), (x, alto))

    for y in range(0, alto, 50):
        pygame.draw.line(pantalla, color_lineas, (0, y), (ancho, y))

    marco = pygame.Rect(30, 30, ancho - 60, alto - 60)
    pygame.draw.rect(pantalla, AZUL_APAGADO, marco, 4, border_radius=30)


def dibujar_titulo(pantalla, texto, cy, fuente):

    ancho = pantalla.get_width()

    sombra = fuente.render(texto, True, NARANJA_SOMBRA)
    titulo = fuente.render(texto, True, NARANJA)

    rect = titulo.get_rect(center=(ancho // 2, cy))

    pantalla.blit(sombra, rect.move(4, 4))
    pantalla.blit(titulo, rect)


def aclarar(color, cantidad):

    return tuple(min(255, c + cantidad) for c in color)


# Las naves de muestra se guardan para no teñirlas cada cuadro
_naves_muestra = {}


def nave_muestra(tinte):

    if tinte not in _naves_muestra:
        _naves_muestra[tinte] = Jugador(0, 0, tinte)

    return _naves_muestra[tinte]


def total_trofeos(progreso):

    ganados = sum(len(progreso["modos"][modo]["trofeos"]) for modo in ORDEN_MODOS)

    return ganados, len(TROFEOS) * len(ORDEN_MODOS)


# ==========================================================
# PANTALLA PARA ELEGIR EL MODO
# ==========================================================

def pantalla_modos(pantalla, reloj, fps, progreso, sonidos, modo_inicial="basico"):

    # Devuelve el modo elegido o None si el jugador vuelve atrás

    ancho, alto = pantalla.get_size()

    fuente_titulo = pygame.font.Font(None, 64)
    fuente = pygame.font.Font(None, 34)
    fuente_pequena = pygame.font.Font(None, 24)
    fuente_mini = pygame.font.Font(None, 20)

    seleccion = ORDEN_MODOS.index(modo_inicial)

    # Colores que se pueden elegir (solo los desbloqueados)
    colores_disponibles = [
        datos[0] for datos in COLORES_NAVE
        if color_desbloqueado(progreso, datos[0])
    ]

    if progreso["color_nave"] in colores_disponibles:
        indice_color = colores_disponibles.index(progreso["color_nave"])
    else:
        indice_color = 0

    # Sacudida de la tarjeta bloqueada
    sacudida_hasta = 0
    controles_menu = ControlesTactiles(ancho, alto)

    while True:

        ticks = pygame.time.get_ticks()
        tiempo = ticks / 1000

        modo = ORDEN_MODOS[seleccion]

        # ==================================================
        # EVENTOS
        # ==================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return None

            toque = controles_menu.evento(evento)
            if toque is not None and toque[0] == "back":
                return None

            if toque is not None and toque[0] == "swipe":
                if toque[1] == "izquierda":
                    seleccion = (seleccion - 1) % len(ORDEN_MODOS)
                elif toque[1] == "derecha":
                    seleccion = (seleccion + 1) % len(ORDEN_MODOS)
                elif toque[1] == "arriba":
                    indice_color = (indice_color - 1) % len(colores_disponibles)
                else:
                    indice_color = (indice_color + 1) % len(colores_disponibles)
                sonidos["mover"].play()
                continue

            if toque is not None and toque[0] == "down":
                _, posicion = toque
                if 115 <= posicion[1] <= 425:
                    x_inicio_touch = (ancho - (160 * 3 + 15 * 2)) // 2
                    indice = max(0, min(len(ORDEN_MODOS) - 1, (posicion[0] - x_inicio_touch) // 175))
                    if x_inicio_touch <= posicion[0] <= x_inicio_touch + 3 * 160 + 2 * 15:
                        seleccion = int(indice)
                        sonidos["mover"].play()
                elif 515 <= posicion[1] <= 625:
                    if posicion[1] < 570:
                        indice_color = (indice_color - 1) % len(colores_disponibles)
                    else:
                        indice_color = (indice_color + 1) % len(colores_disponibles)
                    sonidos["mover"].play()
                elif posicion[1] > alto - 115:
                    modo = ORDEN_MODOS[seleccion]
                    if modo_desbloqueado(progreso, modo):
                        progreso["color_nave"] = colores_disponibles[indice_color]
                        guardar_progreso(progreso)
                        sonidos["elegir"].play()
                        return modo

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_LEFT, pygame.K_a):

                    seleccion = (seleccion - 1) % len(ORDEN_MODOS)
                    sonidos["mover"].play()

                if evento.key in (pygame.K_RIGHT, pygame.K_d):

                    seleccion = (seleccion + 1) % len(ORDEN_MODOS)
                    sonidos["mover"].play()

                if evento.key in (pygame.K_UP, pygame.K_w):

                    indice_color = (indice_color - 1) % len(colores_disponibles)
                    sonidos["mover"].play()

                if evento.key in (pygame.K_DOWN, pygame.K_s):

                    indice_color = (indice_color + 1) % len(colores_disponibles)
                    sonidos["mover"].play()

                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                    modo = ORDEN_MODOS[seleccion]

                    if modo_desbloqueado(progreso, modo):

                        # Guardar el color elegido
                        progreso["color_nave"] = colores_disponibles[indice_color]
                        guardar_progreso(progreso)

                        sonidos["elegir"].play()

                        return modo

                    else:

                        sonidos["bloqueado"].play()
                        sacudida_hasta = ticks + 350

                if evento.key == pygame.K_ESCAPE:
                    return None

        modo = ORDEN_MODOS[seleccion]

        # ==================================================
        # FONDO (del color del modo seleccionado)
        # ==================================================

        if modo_desbloqueado(progreso, modo):
            dibujar_fondo(pantalla, MODOS[modo]["fondo"], MODOS[modo]["lineas"])
        else:
            dibujar_fondo(pantalla, AZUL, AZUL_LINEAS)

        dibujar_titulo(pantalla, "ELIGE TU MISIÓN", 80, fuente_titulo)

        # ==================================================
        # TARJETAS
        # ==================================================

        ancho_tarjeta = 160
        alto_tarjeta = 280
        separacion = 15

        x_inicio = (ancho - (ancho_tarjeta * 3 + separacion * 2)) // 2

        for i, clave in enumerate(ORDEN_MODOS):

            datos = MODOS[clave]
            abierto = modo_desbloqueado(progreso, clave)
            elegida = i == seleccion

            x = x_inicio + i * (ancho_tarjeta + separacion)
            y = 125

            # La tarjeta elegida sube un poco
            if elegida:
                y -= 10

            # Sacudida si está bloqueada
            if elegida and ticks < sacudida_hasta:
                x += int(math.sin(ticks * 0.08) * 8)

            tarjeta = pygame.Rect(x, y, ancho_tarjeta, alto_tarjeta)
            cx = tarjeta.centerx

            # Fondo y borde
            if abierto:
                color_tarjeta = aclarar(datos["fondo"], 12)
            else:
                color_tarjeta = FONDO_BLOQUEADO

            pygame.draw.rect(pantalla, color_tarjeta, tarjeta, border_radius=18)

            if elegida:

                # Borde que brilla
                brillo = int((math.sin(tiempo * 5) + 1) * 30)

                pygame.draw.rect(pantalla, aclarar(NARANJA, brillo), tarjeta, 4, border_radius=18)

            else:
                pygame.draw.rect(pantalla, AZUL_APAGADO, tarjeta, 2, border_radius=18)

            if abierto:

                color_nombre = datos["color"]

                dibujar_icono_modo(pantalla, clave, cx, y + 58, tiempo)

            else:

                color_nombre = GRIS_BLOQUEADO

                dibujar_candado(pantalla, cx, y + 52, 1.1, GRIS_BLOQUEADO)

            # Nombre del modo
            texto = fuente.render(datos["nombre"], True, color_nombre)
            pantalla.blit(texto, texto.get_rect(center=(cx, y + 115)))

            # Estrellas de dificultad
            if abierto:
                color_estrella = NARANJA
            else:
                color_estrella = GRIS_BLOQUEADO

            dibujar_estrellas(pantalla, cx, y + 145, datos["estrellas"], color_estrella, GRIS_BLOQUEADO, 9)

            if abierto:

                texto = fuente_mini.render(datos["subtitulo"], True, CREMA)
                pantalla.blit(texto, texto.get_rect(center=(cx, y + 175)))

                record = progreso["modos"][clave]["record"]

                texto = fuente_pequena.render(f"Récord: {record}", True, CREMA)
                pantalla.blit(texto, texto.get_rect(center=(cx, y + 203)))

                dibujar_coleccion(
                    pantalla,
                    cx,
                    y + 245,
                    0.32,
                    progreso["modos"][clave]["trofeos"],
                    None,
                    separacion=35
                )

                # Etiqueta de NUEVO si todavía no se ha jugado
                if clave != "basico" and record == 0:

                    etiqueta = fuente_mini.render("¡NUEVO!", True, (40, 20, 0))

                    rect = etiqueta.get_rect()
                    rect.inflate_ip(14, 8)
                    rect.topright = (tarjeta.right - 6, tarjeta.top - 8 + int(math.sin(tiempo * 6) * 2))

                    pygame.draw.rect(pantalla, NARANJA, rect, border_radius=8)
                    pantalla.blit(etiqueta, etiqueta.get_rect(center=rect.center))

            else:

                texto = fuente_mini.render("Para desbloquear:", True, AZUL_APAGADO)
                pantalla.blit(texto, texto.get_rect(center=(cx, y + 185)))

                requisito = datos["requisito"]

                texto = fuente_pequena.render(f"Trofeo {requisito[1].upper()}", True, (255, 205, 40))
                pantalla.blit(texto, texto.get_rect(center=(cx, y + 212)))

                texto = fuente_pequena.render(f"en {MODOS[requisito[0]]['nombre']}", True, (255, 205, 40))
                pantalla.blit(texto, texto.get_rect(center=(cx, y + 236)))

        # ==================================================
        # NAVE Y COLOR
        # ==================================================

        clave_color = colores_disponibles[indice_color]

        nave = nave_muestra(tinte_nave(clave_color, modo))

        nave.rect.topleft = (ancho // 2 - 30, 440 + int(math.sin(tiempo * 2.5) * 4))
        nave.dibujar(pantalla)

        nombre_color = datos_color(clave_color)[1]

        if clave_color == "modo":

            nombre_color += f" ({datos_color(MODOS[modo]['color_nave'])[1]})"

        texto = fuente_pequena.render(f"NAVE: {nombre_color}", True, CREMA)
        rect = texto.get_rect(center=(ancho // 2, 545))
        pantalla.blit(texto, rect)

        # Flechas arriba y abajo para cambiar el color
        flecha_x = rect.right + 18

        pygame.draw.polygon(pantalla, NARANJA, [
            (flecha_x, rect.centery - 13), (flecha_x - 6, rect.centery - 4), (flecha_x + 6, rect.centery - 4)
        ])

        pygame.draw.polygon(pantalla, NARANJA, [
            (flecha_x, rect.centery + 13), (flecha_x - 6, rect.centery + 4), (flecha_x + 6, rect.centery + 4)
        ])

        bloqueados = len(COLORES_NAVE) - len(colores_disponibles)

        if bloqueados > 0:

            if bloqueados == 1:
                aviso = "1 color por desbloquear (mira LOGROS)"
            else:
                aviso = f"{bloqueados} colores por desbloquear (mira LOGROS)"

            texto = fuente_mini.render(
                aviso,
                True,
                AZUL_APAGADO
            )

            pantalla.blit(texto, texto.get_rect(center=(ancho // 2, 572)))

        # ==================================================
        # AYUDA
        # ==================================================

        lineas = [
            "Izquierda / Derecha: modo     Arriba / Abajo: color",
            "ENTER jugar      ESC volver"
        ]

        for i, linea in enumerate(lineas):

            texto = fuente_pequena.render(linea, True, AZUL_APAGADO)
            pantalla.blit(texto, texto.get_rect(center=(ancho // 2, alto - 92 + i * 26)))

        texto_tactil = fuente_mini.render("Toca una tarjeta, el color o JUGAR", True, AZUL_APAGADO)
        pantalla.blit(texto_tactil, texto_tactil.get_rect(center=(ancho // 2, alto - 35)))

        pygame.display.flip()

        reloj.tick(fps)


# ==========================================================
# PANTALLA DE LOGROS
# ==========================================================

def pantalla_logros(pantalla, reloj, fps, progreso, sonidos):

    ancho, alto = pantalla.get_size()

    fuente_titulo = pygame.font.Font(None, 72)
    fuente = pygame.font.Font(None, 32)
    fuente_pequena = pygame.font.Font(None, 24)
    fuente_mini = pygame.font.Font(None, 18)
    controles_menu = ControlesTactiles(ancho, alto)

    while True:

        tiempo = pygame.time.get_ticks() / 1000

        # ==================================================
        # EVENTOS
        # ==================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return

            toque = controles_menu.evento(evento)
            if toque is not None and toque[0] in ("back", "swipe", "down"):
                sonidos["elegir"].play()
                return

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):

                    sonidos["elegir"].play()
                    return

        # ==================================================
        # FONDO Y TÍTULO
        # ==================================================

        dibujar_fondo(pantalla, AZUL, AZUL_LINEAS)

        dibujar_titulo(pantalla, "LOGROS", 75, fuente_titulo)

        ganados, total = total_trofeos(progreso)

        texto = fuente_pequena.render(f"Trofeos: {ganados} / {total}", True, CREMA)
        pantalla.blit(texto, texto.get_rect(center=(ancho // 2, 112)))

        # ==================================================
        # UNA FILA POR MODO
        # ==================================================

        for i, clave in enumerate(ORDEN_MODOS):

            datos = MODOS[clave]
            abierto = modo_desbloqueado(progreso, clave)

            y = 130 + i * 122

            panel = pygame.Rect(50, y, ancho - 100, 112)

            if abierto:

                pygame.draw.rect(pantalla, aclarar(datos["fondo"], 10), panel, border_radius=16)
                pygame.draw.rect(pantalla, datos["color"], panel, 2, border_radius=16)

                dibujar_icono_modo(pantalla, clave, 108, y + 42, tiempo)

                color_nombre = datos["color"]

            else:

                pygame.draw.rect(pantalla, FONDO_BLOQUEADO, panel, border_radius=16)
                pygame.draw.rect(pantalla, GRIS_BLOQUEADO, panel, 2, border_radius=16)

                dibujar_candado(pantalla, 108, y + 40, 0.8, GRIS_BLOQUEADO)

                color_nombre = GRIS_BLOQUEADO

            dibujar_estrellas(
                pantalla, 108, y + 90, datos["estrellas"],
                NARANJA if abierto else GRIS_BLOQUEADO,
                GRIS_BLOQUEADO,
                7
            )

            # Nombre y récord
            texto = fuente.render(datos["nombre"], True, color_nombre)
            pantalla.blit(texto, (165, y + 18))

            if abierto:

                record = progreso["modos"][clave]["record"]

                texto = fuente_pequena.render(f"Récord: {record}", True, CREMA)
                pantalla.blit(texto, (165, y + 50))

                # El diamante de cada modo tiene su propio título
                if "diamante" in progreso["modos"][clave]["trofeos"]:

                    texto = fuente_mini.render(datos["texto_diamante"], True, (120, 225, 255))
                    pantalla.blit(texto, (165, y + 76))

            else:

                texto = fuente_mini.render("Consigue el trofeo", True, AZUL_APAGADO)
                pantalla.blit(texto, (165, y + 52))

                texto = fuente_mini.render(texto_requisito(datos["requisito"]), True, (255, 205, 40))
                pantalla.blit(texto, (165, y + 70))

            # Trofeos del modo
            dibujar_coleccion(
                pantalla,
                415,
                y + 48,
                0.45,
                progreso["modos"][clave]["trofeos"],
                fuente_mini,
                separacion=56
            )

        # ==================================================
        # COLORES DE NAVE
        # ==================================================

        texto = fuente_pequena.render("COLORES DE NAVE", True, CREMA)
        pantalla.blit(texto, texto.get_rect(center=(ancho // 2, 507)))

        colores = [datos for datos in COLORES_NAVE if datos[0] != "modo"]

        separacion = 70
        x_inicio = ancho // 2 - separacion * (len(colores) - 1) / 2

        for i, (clave, nombre, tinte, requisito) in enumerate(colores):

            cx = int(x_inicio + i * separacion)

            if color_desbloqueado(progreso, clave):

                nave = nave_muestra(tinte)

                imagen = pygame.transform.smoothscale(nave.imagen, (30, 35))
                pantalla.blit(imagen, imagen.get_rect(center=(cx, 545)))

                texto = fuente_mini.render(nombre, True, CREMA)
                pantalla.blit(texto, texto.get_rect(center=(cx, 576)))

            else:

                dibujar_candado(pantalla, cx, 542, 0.45, GRIS_BLOQUEADO)

                texto = fuente_mini.render(nombre, True, GRIS_BLOQUEADO)
                pantalla.blit(texto, texto.get_rect(center=(cx, 576)))

                modo_req, trofeo_req = requisito

                texto = fuente_mini.render(trofeo_req.upper(), True, AZUL_APAGADO)
                pantalla.blit(texto, texto.get_rect(center=(cx, 592)))

                texto = fuente_mini.render(MODOS[modo_req]["nombre"], True, AZUL_APAGADO)
                pantalla.blit(texto, texto.get_rect(center=(cx, 606)))

        texto = fuente_pequena.render("ESC o ENTER para volver", True, AZUL_APAGADO)
        pantalla.blit(texto, texto.get_rect(center=(ancho // 2, alto - 60)))

        texto_tactil = fuente_mini.render("Toca la pantalla para volver", True, AZUL_APAGADO)
        pantalla.blit(texto_tactil, texto_tactil.get_rect(center=(ancho // 2, alto - 32)))

        pygame.display.flip()

        reloj.tick(fps)
