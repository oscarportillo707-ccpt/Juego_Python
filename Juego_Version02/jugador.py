import os
import math
import colorsys
import pygame

from rutas import ruta_recurso


def teñir_imagen(imagen, tinte):

    # Cambia el color de las partes azules de la nave.
    #
    # tinte = (tono, saturación, brillo extra)
    # Los colores que no son azules (llamas, cabina...) no cambian.

    tono, saturacion, brillo_extra = tinte

    nueva = imagen.copy()

    for x in range(nueva.get_width()):

        for y in range(nueva.get_height()):

            r, g, b, a = nueva.get_at((x, y))

            if a == 0:
                continue

            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

            # Solo los tonos azules con color
            if s < 0.2 or not (0.45 <= h <= 0.75):
                continue

            h = tono

            if saturacion is not None:
                s = s * saturacion

            v = min(1, v + brillo_extra)

            r, g, b = colorsys.hsv_to_rgb(h, s, v)

            nueva.set_at((x, y), (int(r * 255), int(g * 255), int(b * 255), a))

    return nueva


class Jugador:

    def __init__(self, x, y, tinte=None):
        # Tamaño del jugador
        self.ancho = 60
        self.alto = 70

        # Rectángulo que representa al jugador
        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )

        # Velocidad horizontal
        self.velocidad = 7

        # Imagen de la nave 
        self.imagen = pygame.image.load(ruta_recurso("jugador.png")).convert_alpha()
        pygame.draw.rect(
            self.imagen,
            (0, 0, 0, 0),
            (22, 57, 16, 13)
        )

        # Color de la nave
        if tinte is not None:
            self.imagen = teñir_imagen(self.imagen, tinte)

        # Tiempo de la partida (en segundos)
        self.tiempo_juego = 0

        # Hasta qué segundo dura cada efecto
        self.invulnerable_hasta = 0
        self.escudo_hasta = 0
        self.iman_hasta = 0
        self.arma_hasta = 0

    # ======================================================
    # EFECTOS ESPECIALES
    # ======================================================

    def actualizar_tiempo(self, tiempo_juego):

        self.tiempo_juego = tiempo_juego

    def recibir_golpe(self, duracion=1.5):

        # Después de un golpe la nave queda invulnerable
        self.invulnerable_hasta = self.tiempo_juego + duracion

    def es_invulnerable(self):

        return self.tiempo_juego < self.invulnerable_hasta

    def activar_escudo(self, duracion=5):

        self.escudo_hasta = self.tiempo_juego + duracion

    def tiene_escudo(self):

        return self.tiempo_juego < self.escudo_hasta

    def activar_iman(self, duracion=6):

        self.iman_hasta = self.tiempo_juego + duracion

    def tiene_iman(self):

        return self.tiempo_juego < self.iman_hasta

    def activar_arma(self, duracion=10):

        self.arma_hasta = self.tiempo_juego + duracion

    def tiene_arma(self):

        return self.tiempo_juego < self.arma_hasta

    def puntos_de_disparo(self):

        # Las dos puntas de las alas, de donde salen las balas
        return [
            (self.rect.left + 9, self.rect.top + 30),
            (self.rect.right - 9, self.rect.top + 30)
        ]

    def mover(self, teclas, ancho_pantalla):

        # Mover a la izquierda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad

        # Mover a la derecha
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad

        # Evitar salir por la izquierda
        if self.rect.left < 0:
            self.rect.left = 0

        # Evitar salir por la derecha
        if self.rect.right > ancho_pantalla:
            self.rect.right = ancho_pantalla

        # Dibujar la nave en la pantalla
    def dibujar(self, pantalla):

        tiempo = pygame.time.get_ticks()

        # Campo del imán
        if self.tiene_iman():

            radio = 50 + int((tiempo // 4) % 40)

            capa = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)

            pygame.draw.circle(
                capa,
                (200, 90, 255, 90),
                (radio, radio),
                radio,
                2
            )

            pantalla.blit(
                capa,
                (self.rect.centerx - radio, self.rect.centery - radio)
            )

        # Parpadeo mientras es invulnerable
        if self.es_invulnerable() and (tiempo // 80) % 2 == 0:
            return

        pantalla.blit(self.imagen, self.rect)

        # Cañones en las alas mientras dura el arma
        if self.tiene_arma():

            restante = self.arma_hasta - self.tiempo_juego

            # Parpadean cuando el arma está por terminarse
            if restante > 1.5 or (tiempo // 100) % 2 == 0:

                for x, y in self.puntos_de_disparo():

                    pygame.draw.rect(pantalla, (90, 95, 110), (x - 4, y - 2, 8, 16), border_radius=2)
                    pygame.draw.rect(pantalla, (255, 150, 40), (x - 4, y - 6, 8, 6), border_radius=2)

        # Burbuja del escudo
        if self.tiene_escudo():

            restante = self.escudo_hasta - self.tiempo_juego

            # Parpadea cuando está por terminarse
            if restante > 1.2 or (tiempo // 100) % 2 == 0:

                radio = 48

                capa = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)

                pygame.draw.circle(capa, (80, 200, 255, 50), (radio, radio), radio)
                pygame.draw.circle(capa, (170, 235, 255, 180), (radio, radio), radio, 3)

                pantalla.blit(
                    capa,
                    (self.rect.centerx - radio, self.rect.centery - radio)
                )

        largo_llama = 8 + int((math.sin(tiempo * 0.025) + 1) * 3)
        centro_x = self.rect.centerx
        inicio_y = self.rect.y + 57

        pygame.draw.polygon(
            pantalla,
            (255, 145, 20),
            [
                (centro_x - 6, inicio_y),
                (centro_x, inicio_y + largo_llama),
                (centro_x + 6, inicio_y)
            ]
        )
        pygame.draw.polygon(
            pantalla,
            (255, 235, 60),
            [
                (centro_x - 3, inicio_y),
                (centro_x, inicio_y + largo_llama // 2),
                (centro_x + 3, inicio_y)
            ]
        )