import pygame
import random
import math


class Ambiente:
    """
    Se encarga de toda la ambientación visual del juego:

    - Fondo degradado
    - Partículas
    - Estrellas
    - Iluminación
    - Efectos de monedas
    - Efectos de golpes
    - Cambios visuales con el tiempo
    """

    def __init__(self, ancho, alto):

        self.ancho = ancho
        self.alto = alto

        # ==================================================
        # PARTÍCULAS
        # ==================================================

        self.particulas = []

        for i in range(70):

            particula = {
                "x": random.randint(0, ancho),
                "y": random.randint(0, alto),
                "velocidad": random.uniform(0.2, 1.2),
                "tamaño": random.randint(1, 3),
                "brillo": random.randint(80, 200)
            }

            self.particulas.append(particula)

        # ==================================================
        # ESTRELLAS
        # ==================================================

        self.estrellas = []

        for i in range(35):

            estrella = {
                "x": random.randint(0, ancho),
                "y": random.randint(0, alto),
                "tamaño": random.randint(1, 2),
                "fase": random.uniform(0, math.pi * 2)
            }

            self.estrellas.append(estrella)

        # ==================================================
        # EFECTOS DE MONEDAS
        # ==================================================

        self.efectos_monedas = []

        # ==================================================
        # EFECTOS DE GOLPES
        # ==================================================

        self.efectos_golpes = []

        # ==================================================
        # EFECTOS GENERALES
        # ==================================================

        self.tiempo = 0

        # ==================================================
        # TEMA (cambia según el modo de juego)
        # ==================================================

        self.tema = "basico"

    # ======================================================
    # CAMBIAR EL TEMA
    # ======================================================

    # Colores del fondo de cada tema: lista de (arriba, abajo)
    COLORES_TEMAS = {
        "basico": [
            ((8, 12, 40), (25, 50, 90)),      # Azul oscuro
            ((25, 8, 45), (70, 25, 80)),      # Morado oscuro
            ((5, 8, 30), (15, 35, 70)),       # Azul profundo
        ],
        "medio": [
            ((22, 6, 40), (80, 30, 110)),     # Nebulosa morada
            ((10, 6, 35), (55, 20, 95)),      # Violeta profundo
            ((30, 8, 45), (110, 35, 100)),    # Magenta oscuro
        ],
        "avanzado": [
            ((20, 2, 6), (85, 15, 20)),       # Rojo oscuro
            ((8, 0, 4), (55, 8, 25)),         # Casi negro
            ((25, 4, 2), (110, 30, 10)),      # Rojo fuego
        ],
    }

    # Color de la luz alrededor de la nave
    LUZ_TEMAS = {
        "basico": (80, 150, 255),
        "medio": (170, 100, 255),
        "avanzado": (255, 90, 60),
    }

    def cambiar_tema(self, tema):

        self.tema = tema

    # ======================================================
    # ACTUALIZAR AMBIENTE
    # ======================================================

    def actualizar(self, tiempo_transcurrido):

        self.tiempo = tiempo_transcurrido

        # --------------------------------------------------
        # Actualizar partículas
        # --------------------------------------------------

        for particula in self.particulas:

            particula["y"] += particula["velocidad"]

            # Si sale por abajo, vuelve arriba
            if particula["y"] > self.alto:

                particula["y"] = -5

                particula["x"] = random.randint(
                    0,
                    self.ancho
                )

        # --------------------------------------------------
        # Actualizar estrellas
        # --------------------------------------------------

        for estrella in self.estrellas:

            estrella["fase"] += 0.03

        # --------------------------------------------------
        # Actualizar efectos de monedas
        # --------------------------------------------------

        for efecto in self.efectos_monedas[:]:

            efecto["radio"] += 2
            efecto["vida"] -= 1

            if efecto["vida"] <= 0:

                self.efectos_monedas.remove(
                    efecto
                )

        # --------------------------------------------------
        # Actualizar efectos de golpes
        # --------------------------------------------------

        for efecto in self.efectos_golpes[:]:

            efecto["radio"] += 4
            efecto["vida"] -= 1

            if efecto["vida"] <= 0:

                self.efectos_golpes.remove(
                    efecto
                )

    # ======================================================
    # COLOR DEL FONDO SEGÚN EL TIEMPO
    # ======================================================

    def obtener_colores_fondo(self):

        """
        El fondo cambia lentamente conforme avanza
        la partida.
        """

        tiempo = self.tiempo

        # Ciclo visual
        fase = int((tiempo / 30) % 3)

        colores = self.COLORES_TEMAS.get(
            self.tema,
            self.COLORES_TEMAS["basico"]
        )

        color_arriba, color_abajo = colores[fase]

        return color_arriba, color_abajo

    # ======================================================
    # DIBUJAR FONDO DEGRADADO
    # ======================================================

    def dibujar_fondo(self, pantalla):

        color_arriba, color_abajo = (
            self.obtener_colores_fondo()
        )

        # Zona superior del juego
        altura_fondo = self.alto

        for y in range(altura_fondo):

            porcentaje = y / altura_fondo

            rojo = int(
                color_arriba[0]
                + (
                    color_abajo[0]
                    - color_arriba[0]
                ) * porcentaje
            )

            verde = int(
                color_arriba[1]
                + (
                    color_abajo[1]
                    - color_arriba[1]
                ) * porcentaje
            )

            azul = int(
                color_arriba[2]
                + (
                    color_abajo[2]
                    - color_arriba[2]
                ) * porcentaje
            )

            pygame.draw.line(
                pantalla,
                (rojo, verde, azul),
                (0, y),
                (self.ancho, y)
            )

    # ======================================================
    # DIBUJAR ESTRELLAS
    # ======================================================

    def dibujar_estrellas(self, pantalla):

        for estrella in self.estrellas:

            brillo = (
                math.sin(
                    estrella["fase"]
                ) + 1
            ) / 2

            brillo = int(
                80 + brillo * 175
            )

            color = (
                brillo,
                brillo,
                brillo
            )

            pygame.draw.circle(
                pantalla,
                color,
                (
                    int(estrella["x"]),
                    int(estrella["y"])
                ),
                estrella["tamaño"]
            )

    # ======================================================
    # DIBUJAR PARTÍCULAS
    # ======================================================

    def dibujar_particulas(self, pantalla):

        for particula in self.particulas:

            brillo = particula["brillo"]

            color = (
                brillo,
                brillo,
                min(255, brillo + 30)
            )

            pygame.draw.circle(
                pantalla,
                color,
                (
                    int(particula["x"]),
                    int(particula["y"])
                ),
                particula["tamaño"]
            )

    # ======================================================
    # ILUMINACIÓN AMBIENTAL
    # ======================================================

    def dibujar_iluminacion(
        self,
        pantalla,
        jugador
    ):

        """
        Crea una iluminación suave alrededor
        del jugador.
        """

        capa = pygame.Surface(
            (self.ancho, self.alto),
            pygame.SRCALPHA
        )

        # Oscurecimiento general muy suave
        capa.fill(
            (0, 0, 20, 35)
        )

        # Centro de iluminación
        centro_x = jugador.rect.centerx
        centro_y = jugador.rect.centery

        luz = self.LUZ_TEMAS.get(
            self.tema,
            self.LUZ_TEMAS["basico"]
        )

        # Crear varios círculos transparentes
        for radio in range(180, 20, -20):

            transparencia = int(
                2 + (180 - radio) * 0.10
            )

            pygame.draw.circle(
                capa,
                (
                    *luz,
                    transparencia
                ),
                (
                    centro_x,
                    centro_y
                ),
                radio
            )

        pantalla.blit(
            capa,
            (0, 0)
        )

    # ======================================================
    # EFECTO AL RECOGER MONEDA
    # ======================================================

    def efecto_moneda(self, x, y):

        efecto = {
            "x": x,
            "y": y,
            "radio": 5,
            "vida": 20
        }

        self.efectos_monedas.append(
            efecto
        )

    # ======================================================
    # DIBUJAR EFECTOS DE MONEDAS
    # ======================================================

    def dibujar_efectos_monedas(
        self,
        pantalla
    ):

        for efecto in self.efectos_monedas:

            alpha = int(
                efecto["vida"] * 12
            )

            alpha = max(
                0,
                min(255, alpha)
            )

            capa = pygame.Surface(
                (self.ancho, self.alto),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                capa,
                (
                    255,
                    220,
                    50,
                    alpha
                ),
                (
                    int(efecto["x"]),
                    int(efecto["y"])
                ),
                int(efecto["radio"]),
                3
            )

            pantalla.blit(
                capa,
                (0, 0)
            )

    # ======================================================
    # EFECTO DE GOLPE
    # ======================================================

    def efecto_golpe(self, x, y):

        efecto = {
            "x": x,
            "y": y,
            "radio": 10,
            "vida": 25
        }

        self.efectos_golpes.append(
            efecto
        )

    # ======================================================
    # DIBUJAR EFECTOS DE GOLPES
    # ======================================================

    def dibujar_efectos_golpes(
        self,
        pantalla
    ):

        for efecto in self.efectos_golpes:

            alpha = int(
                efecto["vida"] * 10
            )

            alpha = max(
                0,
                min(255, alpha)
            )

            capa = pygame.Surface(
                (self.ancho, self.alto),
                pygame.SRCALPHA
            )

            # Círculo exterior
            pygame.draw.circle(
                capa,
                (
                    255,
                    60,
                    60,
                    alpha
                ),
                (
                    int(efecto["x"]),
                    int(efecto["y"])
                ),
                int(efecto["radio"]),
                4
            )

            # Líneas de impacto
            centro_x = int(
                efecto["x"]
            )

            centro_y = int(
                efecto["y"]
            )

            radio = int(
                efecto["radio"]
            )

            for i in range(8):

                angulo = (
                    i * math.pi / 4
                )

                x1 = centro_x + int(
                    math.cos(angulo)
                    * radio
                )

                y1 = centro_y + int(
                    math.sin(angulo)
                    * radio
                )

                x2 = centro_x + int(
                    math.cos(angulo)
                    * (radio + 10)
                )

                y2 = centro_y + int(
                    math.sin(angulo)
                    * (radio + 10)
                )

                pygame.draw.line(
                    capa,
                    (
                        255,
                        100,
                        80,
                        alpha
                    ),
                    (x1, y1),
                    (x2, y2),
                    2
                )

            pantalla.blit(
                capa,
                (0, 0)
            )

    # ======================================================
    # AMBIENTE COMPLETO
    # ======================================================

    def dibujar(
        self,
        pantalla,
        jugador
    ):

        # Fondo
        self.dibujar_fondo(
            pantalla
        )

        # Estrellas
        self.dibujar_estrellas(
            pantalla
        )

        # Partículas
        self.dibujar_particulas(
            pantalla
        )

        # Iluminación
        self.dibujar_iluminacion(
            pantalla,
            jugador
        )

        # Efectos de monedas
        self.dibujar_efectos_monedas(
            pantalla
        )

        # Efectos de golpes
        self.dibujar_efectos_golpes(
            pantalla
        )