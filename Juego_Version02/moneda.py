import pygame
import random


class Moneda:

    def __init__(self, x, y):
        # Tamaño de la moneda
        self.tamaño = 30

        self.rect = pygame.Rect(
            x,
            y,
            self.tamaño,
            self.tamaño
        )

        # Posición vertical como decimal
        self.y = float(y)

    def actualizar(self, velocidad):

        # Actualizar velocidad
        self.y += velocidad

        # Actualizar posición del rectángulo
        self.rect.y = int(self.y)

    def reiniciar(self, ancho_pantalla):

        # Nueva posición horizontal aleatoria
        nueva_x = random.randint(
            0,
            ancho_pantalla - self.tamaño
        )

        # Aparecer nuevamente arriba
        nueva_y = random.randint(-300, -50)

        self.rect.x = nueva_x
        self.rect.y = nueva_y

        self.y = float(nueva_y)

    def esta_fuera(self, alto_pantalla):

        return self.rect.top > alto_pantalla

    def dibujar(self, pantalla):

        # Por ahora usamos un círculo amarillo.
        # Después podemos colocar moneda.png
        pygame.draw.circle(
            pantalla,
            (255, 215, 0),
            self.rect.center,
            self.tamaño // 2
        )

        # Brillo de la moneda
        pygame.draw.circle(
            pantalla,
            (255, 240, 120),
            self.rect.center,
            8
        )