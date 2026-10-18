import pygame
import random
import math


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

        # Posición como decimal
        self.x = float(x)
        self.y = float(y)

        # Fase del giro (cada moneda gira desfasada)
        self.fase = random.uniform(0, math.pi * 2)

    def actualizar(self, velocidad):

        # Actualizar velocidad
        self.y += velocidad

        # Actualizar posición del rectángulo
        self.rect.y = int(self.y)

        # Animación de giro
        self.fase += 0.08

    def atraer(self, destino_x, destino_y, fuerza=6):

        # Mueve la moneda hacia el jugador (imán)
        dx = destino_x - self.rect.centerx
        dy = destino_y - self.rect.centery

        distancia = math.hypot(dx, dy)

        if distancia < 1:
            return

        paso = min(fuerza, distancia)

        self.x += dx / distancia * paso
        self.y += dy / distancia * paso

        self.rect.x = int(self.x)
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

        self.x = float(nueva_x)
        self.y = float(nueva_y)

    def esta_fuera(self, alto_pantalla):

        return self.rect.top > alto_pantalla

    def dibujar(self, pantalla):

        # La moneda "gira" cambiando su ancho
        giro = abs(math.cos(self.fase))

        ancho = max(4, int(self.tamaño * giro))

        rect = pygame.Rect(0, 0, ancho, self.tamaño)
        rect.center = self.rect.center

        # Borde
        pygame.draw.ellipse(
            pantalla,
            (210, 160, 0),
            rect
        )

        # Cara de la moneda
        if ancho > 8:

            pygame.draw.ellipse(
                pantalla,
                (255, 215, 0),
                rect.inflate(-5, -5)
            )

        # Brillo de la moneda
        brillo = pygame.Rect(0, 0, max(2, int(10 * giro)), 12)
        brillo.center = (rect.centerx - int(4 * giro), rect.centery - 4)

        pygame.draw.ellipse(
            pantalla,
            (255, 245, 160),
            brillo
        )

        # Destello que aparece de vez en cuando
        if math.sin(self.fase * 0.5) > 0.97:

            cx, cy = rect.centerx + 8, rect.top + 4

            pygame.draw.line(pantalla, (255, 255, 255), (cx - 6, cy), (cx + 6, cy), 2)
            pygame.draw.line(pantalla, (255, 255, 255), (cx, cy - 6), (cx, cy + 6), 2)
