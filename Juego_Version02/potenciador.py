import math
import random
import pygame


class Potenciador:

    # Tipos de objetos especiales:
    #
    # "moneda_grande" = vale 5 puntos
    # "corazon"       = devuelve una vida
    # "escudo"        = protege de los meteoritos por unos segundos
    # "iman"          = atrae las monedas por unos segundos

    TIPOS = ["moneda_grande", "corazon", "escudo", "iman"]

    # Probabilidad de aparición de cada tipo
    PESOS = [40, 20, 20, 20]

    def __init__(self, ancho_pantalla, tipo=None):

        self.tamaño = 36

        if tipo is None:
            tipo = random.choices(self.TIPOS, weights=self.PESOS)[0]

        self.tipo = tipo

        x = random.randint(0, ancho_pantalla - self.tamaño)
        y = -self.tamaño

        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)

        # Posición vertical como decimal
        self.y = float(y)

        # Para la animación
        self.fase = random.uniform(0, math.pi * 2)

    def actualizar(self, velocidad):

        # Cae un poco más lento que el resto
        self.y += velocidad * 0.8

        self.rect.y = int(self.y)

        self.fase += 0.12

    def esta_fuera(self, alto_pantalla):

        return self.rect.top > alto_pantalla

    def dibujar(self, pantalla):

        cx, cy = self.rect.center

        # Aura que palpita
        radio_aura = int(self.tamaño // 2 + 6 + math.sin(self.fase) * 4)

        colores_aura = {
            "moneda_grande": (255, 210, 40, 70),
            "corazon": (255, 80, 110, 70),
            "escudo": (80, 200, 255, 70),
            "iman": (200, 90, 255, 70),
        }

        aura = pygame.Surface(
            (radio_aura * 2, radio_aura * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            aura,
            colores_aura[self.tipo],
            (radio_aura, radio_aura),
            radio_aura
        )

        pantalla.blit(aura, (cx - radio_aura, cy - radio_aura))

        if self.tipo == "moneda_grande":
            self.dibujar_moneda_grande(pantalla, cx, cy)

        elif self.tipo == "corazon":
            self.dibujar_corazon(pantalla, cx, cy)

        elif self.tipo == "escudo":
            self.dibujar_escudo(pantalla, cx, cy)

        elif self.tipo == "iman":
            self.dibujar_iman(pantalla, cx, cy)

    def dibujar_moneda_grande(self, pantalla, cx, cy):

        # Moneda que gira
        ancho = max(4, int(abs(math.cos(self.fase * 0.5)) * self.tamaño))

        rect = pygame.Rect(0, 0, ancho, self.tamaño)
        rect.center = (cx, cy)

        pygame.draw.ellipse(pantalla, (200, 140, 0), rect)
        pygame.draw.ellipse(pantalla, (255, 215, 0), rect.inflate(-6, -6))

        if ancho > 14:

            fuente = pygame.font.Font(None, 26)
            texto = fuente.render("5", True, (160, 100, 0))
            pantalla.blit(texto, texto.get_rect(center=(cx, cy + 1)))

    def dibujar_corazon(self, pantalla, cx, cy):

        tam = int(30 + math.sin(self.fase) * 3)
        r = tam // 4
        x = cx - tam // 2
        y = cy - tam // 2

        pygame.draw.circle(pantalla, (255, 70, 100), (x + r, y + r), r)
        pygame.draw.circle(pantalla, (255, 70, 100), (x + 3 * r, y + r), r)

        pygame.draw.polygon(pantalla, (255, 70, 100), [
            (x, y + int(r * 1.3)),
            (x + 4 * r, y + int(r * 1.3)),
            (x + 2 * r, y + 4 * r)
        ])

        pygame.draw.circle(pantalla, (255, 200, 210), (x + r, y + r - 2), 3)

    def dibujar_escudo(self, pantalla, cx, cy):

        puntos = [
            (cx, cy - 17), (cx + 14, cy - 11), (cx + 12, cy + 6),
            (cx, cy + 17), (cx - 12, cy + 6), (cx - 14, cy - 11)
        ]

        pygame.draw.polygon(pantalla, (60, 170, 255), puntos)
        pygame.draw.polygon(pantalla, (200, 240, 255), puntos, 3)

        pygame.draw.line(pantalla, (200, 240, 255), (cx, cy - 10), (cx, cy + 10), 3)
        pygame.draw.line(pantalla, (200, 240, 255), (cx - 7, cy - 2), (cx + 7, cy - 2), 3)

    def dibujar_iman(self, pantalla, cx, cy):

        # Imán en forma de U
        rect = pygame.Rect(cx - 14, cy - 16, 28, 28)

        pygame.draw.arc(pantalla, (210, 60, 70), rect, math.pi, 2 * math.pi, 9)

        pygame.draw.rect(pantalla, (210, 60, 70), (cx - 14, cy - 10, 9, 8))
        pygame.draw.rect(pantalla, (210, 60, 70), (cx + 5, cy - 10, 9, 8))

        # Puntas plateadas
        pygame.draw.rect(pantalla, (220, 220, 230), (cx - 14, cy - 17, 9, 7))
        pygame.draw.rect(pantalla, (220, 220, 230), (cx + 5, cy - 17, 9, 7))
