import pygame
import random


class Obstaculo:

    def __init__(self, x, y):
        # Tamaño del obstáculo
        self.ancho = 45
        self.alto = 45

        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )

        # Posición vertical como decimal
        self.y = float(y)

        # Imagen del obstáculo
        self.imagen = pygame.image.load("meteorito.png").convert_alpha()

    def actualizar(self, velocidad):

        # Actualizar posición vertical
        self.y += velocidad

        self.rect.y = int(self.y)

    def reiniciar(self, ancho_pantalla):

        # Nueva posición horizontal
        nueva_x = random.randint(
            0,
            ancho_pantalla - self.ancho
        )

        # Aparecer nuevamente arriba
        nueva_y = random.randint(-500, -80)

        self.rect.x = nueva_x
        self.rect.y = nueva_y

        self.y = float(nueva_y)

    def esta_fuera(self, alto_pantalla):

        return self.rect.top > alto_pantalla

    # Dibuja el obstáculo en la pantalla
    def dibujar(self, pantalla):
         pantalla.blit(self.imagen, self.rect)