import pygame
import random

from rutas import ruta_recurso


class Obstaculo:

    # Probabilidad de que un meteorito caiga en zigzag
    # (la cambia el modo de juego)
    PROBABILIDAD_ZIGZAG = 0

    # Ancho de la pantalla, para rebotar en los bordes
    ANCHO_PANTALLA = 600

    def __init__(self, x, y):
        # Tamaño base del obstáculo
        self.tamaño_base = 45

        self.ancho = 45
        self.alto = 45

        self.rect = pygame.Rect(
            x,
            y,
            self.ancho,
            self.alto
        )

        # Posición como decimal
        self.x = float(x)
        self.y = float(y)

        # Imagen del obstáculo
        self.imagen_original = pygame.image.load(ruta_recurso("meteorito.png")).convert_alpha()
        self.imagen = self.imagen_original

        # Cada meteorito es distinto
        self.variar()

    def variar(self):

        # Tamaño: los grandes son más lentos y los pequeños más rápidos
        escala = random.choice([0.7, 0.85, 1.0, 1.0, 1.25, 1.5])

        self.ancho = int(self.tamaño_base * escala)
        self.alto = self.ancho

        self.factor_velocidad = random.uniform(0.9, 1.15) / escala ** 0.5

        # Rotación
        self.angulo = random.uniform(0, 360)
        self.giro = random.uniform(-3, 3)

        self.imagen = pygame.transform.smoothscale(
            self.imagen_original,
            (self.ancho, self.alto)
        )

        centro_x = self.rect.centerx

        self.rect.size = (self.ancho, self.alto)
        self.rect.centerx = centro_x

        self.x = float(self.rect.x)

        # Movimiento de lado a lado (zigzag)
        if random.random() < self.PROBABILIDAD_ZIGZAG:
            self.deriva = random.choice([-1, 1]) * random.uniform(1, 2.2)
        else:
            self.deriva = 0

    def actualizar(self, velocidad):

        # Actualizar posición vertical
        self.y += velocidad * self.factor_velocidad

        self.rect.y = int(self.y)

        # Zigzag: rebota en los bordes de la pantalla
        if self.deriva != 0:

            self.x += self.deriva

            if self.x < 0:
                self.x = 0
                self.deriva = -self.deriva

            if self.x > self.ANCHO_PANTALLA - self.ancho:
                self.x = self.ANCHO_PANTALLA - self.ancho
                self.deriva = -self.deriva

            self.rect.x = int(self.x)

        # Girar
        self.angulo = (self.angulo + self.giro) % 360

    def reiniciar(self, ancho_pantalla):

        # Nuevo tamaño, velocidad y giro
        self.variar()

        # Nueva posición horizontal
        nueva_x = random.randint(
            0,
            ancho_pantalla - self.ancho
        )

        # Aparecer nuevamente arriba
        nueva_y = random.randint(-500, -80)

        self.rect.x = nueva_x
        self.rect.y = nueva_y

        self.x = float(nueva_x)
        self.y = float(nueva_y)

    def esta_fuera(self, alto_pantalla):

        return self.rect.top > alto_pantalla

    # Dibuja el obstáculo en la pantalla
    def dibujar(self, pantalla):

        imagen = pygame.transform.rotate(self.imagen, self.angulo)

        pantalla.blit(
            imagen,
            imagen.get_rect(center=self.rect.center)
        )
