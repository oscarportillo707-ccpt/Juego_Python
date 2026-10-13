import os
import math
import pygame


class Jugador:

    def __init__(self, x, y):
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
        self.imagen = pygame.image.load("jugador.png").convert_alpha()
        pygame.draw.rect(
            self.imagen,
            (0, 0, 0, 0),
            (22, 57, 16, 13)
        )

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
        pantalla.blit(self.imagen, self.rect)

        tiempo = pygame.time.get_ticks()
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