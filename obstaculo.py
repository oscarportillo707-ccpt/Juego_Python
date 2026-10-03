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

    def dibujar(self, pantalla):

        # Por ahora usamos un cuadrado rojo.
        # Después podemos colocar obstaculo.png
        pygame.draw.rect(
            pantalla,
            (220, 50, 50),
            self.rect,
            border_radius=8
        )

        # Detalle del obstáculo
        pygame.draw.line(
            pantalla,
            (255, 120, 120),
            self.rect.topleft,
            self.rect.bottomright,
            3
        )

        pygame.draw.line(
            pantalla,
            (255, 120, 120),
            self.rect.topright,
            self.rect.bottomleft,
            3
        )