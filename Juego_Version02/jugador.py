import os
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