import math
import random
import pygame


class Jefe:

    # ======================================================
    # DURACIÓN DE CADA PARTE (segundos)
    # ======================================================

    DURACION_ALERTA = 2
    DURACION_ENTRADA = 1
    DURACION_ATAQUE = 10
    DURACION_SALIDA = 1.2

    # Ataques especiales: (segundo del ataque, tipo)
    ATAQUES = [
        (2.0, "abanico"),
        (3.5, "laser"),
        (5.5, "abanico"),
        (7.0, "laser"),
        (8.5, "abanico"),
    ]

    # Cada cuánto dispara normalmente
    CADENCIA = 0.75

    # Altura donde se queda la nave (debajo de los puntos y vidas)
    ALTURA = 215

    def __init__(self, ancho, alto, tiempo_inicio, sonidos):

        self.ancho = ancho
        self.alto = alto
        self.sonidos = sonidos

        self.inicio = tiempo_inicio
        self.tiempo = tiempo_inicio

        # "alerta", "entrando", "atacando", "saliendo" o "fin"
        self.fase = "alerta"

        # Posición del centro de la nave
        self.x = ancho / 2
        self.y = -120.0

        self.proyectiles = []

        # Rayo: {"x", "inicio"} (carga 1 s y dispara 0.5 s)
        self.laser = None

        self.siguiente_disparo = 0
        self.ataques_pendientes = list(self.ATAQUES)

        # Para que el juego dé el premio una sola vez
        self.premio_entregado = False

        # Partículas de la explosión
        self.particulas = []

        # Hasta qué segundo brilla en blanco por una bala
        self.destello_hasta = 0

        self.fuente = pygame.font.Font(None, 54)
        self.fuente_pequeña = pygame.font.Font(None, 26)

        self.sonidos["alerta"].play()

    # ======================================================
    # ESTADO
    # ======================================================

    def segundos(self):

        return self.tiempo - self.inicio

    def segundos_ataque(self):

        return self.segundos() - self.DURACION_ALERTA - self.DURACION_ENTRADA

    def esta_activo(self):

        # Mientras está el jefe no caen meteoritos nuevos
        return self.fase != "fin"

    def terminado(self):

        return self.fase == "fin" and not self.proyectiles

    def premio_pendiente(self):

        # True una sola vez, cuando el jugador sobrevive
        if self.fase in ("saliendo", "fin") and not self.premio_entregado:

            self.premio_entregado = True
            return True

        return False

    # ======================================================
    # ACTUALIZAR
    # ======================================================

    def actualizar(self, tiempo, jugador_rect):

        self.tiempo = tiempo

        s = self.segundos()

        inicio_entrada = self.DURACION_ALERTA
        inicio_ataque = inicio_entrada + self.DURACION_ENTRADA
        inicio_salida = inicio_ataque + self.DURACION_ATAQUE
        fin = inicio_salida + self.DURACION_SALIDA

        # --------------------------------------------------
        # Cambiar de fase
        # --------------------------------------------------

        if s < inicio_entrada:
            self.fase = "alerta"

        elif s < inicio_ataque:

            self.fase = "entrando"

            # Baja desde arriba
            avance = (s - inicio_entrada) / self.DURACION_ENTRADA
            self.y = -120 + (self.ALTURA + 120) * avance

        elif s < inicio_salida:

            if self.fase != "atacando":
                self.siguiente_disparo = 0.5

            self.fase = "atacando"
            self.y = self.ALTURA

            self.atacar(s - inicio_ataque, jugador_rect)

        elif s < fin:

            if self.fase != "saliendo":

                self.fase = "saliendo"
                self.laser = None
                self.crear_explosion()
                self.sonidos["explosion"].play()

        else:
            self.fase = "fin"

        # --------------------------------------------------
        # Mover proyectiles
        # --------------------------------------------------

        for proyectil in self.proyectiles[:]:

            proyectil["x"] += proyectil["vx"]
            proyectil["y"] += proyectil["vy"]

            if (
                proyectil["y"] > self.alto + 20
                or proyectil["x"] < -20
                or proyectil["x"] > self.ancho + 20
            ):
                self.proyectiles.remove(proyectil)

        # --------------------------------------------------
        # Partículas de la explosión
        # --------------------------------------------------

        for particula in self.particulas[:]:

            particula["x"] += particula["vx"]
            particula["y"] += particula["vy"]
            particula["vida"] -= 1

            if particula["vida"] <= 0:
                self.particulas.remove(particula)

    def atacar(self, s, jugador_rect):

        # Se mueve de lado a lado
        self.x = self.ancho / 2 + math.sin(s * 1.3) * (self.ancho / 2 - 95)

        # --------------------------------------------------
        # Rayo
        # --------------------------------------------------

        if self.laser is not None:

            if self.tiempo - self.laser["inicio"] > 1.5:
                self.laser = None

        # --------------------------------------------------
        # Ataques especiales
        # --------------------------------------------------

        if self.ataques_pendientes and s >= self.ataques_pendientes[0][0]:

            segundo, tipo = self.ataques_pendientes.pop(0)

            if tipo == "abanico":
                self.disparar_abanico()

            elif tipo == "laser":

                # El rayo cae donde está el jugador en ese momento
                self.laser = {
                    "x": jugador_rect.centerx,
                    "inicio": self.tiempo,
                    "sonó": False
                }

        # Sonido cuando el rayo dispara
        if self.laser is not None and self.laser_disparando() and not self.laser["sonó"]:

            self.laser["sonó"] = True
            self.sonidos["laser"].play()

        # --------------------------------------------------
        # Disparo normal (no dispara mientras carga el rayo)
        # --------------------------------------------------

        if s >= self.siguiente_disparo:

            self.siguiente_disparo = s + self.CADENCIA

            if self.laser is None:
                self.disparar(jugador_rect)

    def disparar(self, jugador_rect):

        # Apunta un poco hacia el jugador
        dx = jugador_rect.centerx - self.x

        self.proyectiles.append({
            "x": self.x,
            "y": self.y + 40,
            "vx": max(-2, min(2, dx / 120)),
            "vy": 6,
            "radio": 8
        })

        self.sonidos["disparo"].play()

    def disparar_abanico(self):

        for i in range(5):

            angulo = math.radians(90 + (i - 2) * 18)

            self.proyectiles.append({
                "x": self.x,
                "y": self.y + 40,
                "vx": math.cos(angulo) * 5,
                "vy": math.sin(angulo) * 5,
                "radio": 9
            })

        self.sonidos["disparo"].play()

    def laser_disparando(self):

        if self.laser is None:
            return False

        segundos_laser = self.tiempo - self.laser["inicio"]

        return 1.0 <= segundos_laser <= 1.5

    def crear_explosion(self):

        for i in range(40):

            angulo = random.uniform(0, math.pi * 2)
            velocidad = random.uniform(1, 6)

            self.particulas.append({
                "x": self.x,
                "y": self.y,
                "vx": math.cos(angulo) * velocidad,
                "vy": math.sin(angulo) * velocidad,
                "vida": random.randint(30, 60),
                "color": random.choice([
                    (255, 220, 80), (255, 140, 40), (255, 70, 50), (255, 255, 255)
                ])
            })

    # ======================================================
    # BALAS DEL JUGADOR
    # ======================================================

    def rect_cuerpo(self):

        # Zona donde le pegan las balas (None si no está en pantalla)
        if self.fase not in ("entrando", "atacando"):
            return None

        rect = pygame.Rect(0, 0, 190, 70)
        rect.center = (int(self.x), int(self.y))

        return rect

    def recibir_impacto(self, x, y):

        # Las balas no lo destruyen (hay que sobrevivir),
        # pero brilla y saltan chispas
        self.destello_hasta = self.tiempo + 0.08

        for i in range(4):

            angulo = random.uniform(math.pi * 1.1, math.pi * 1.9)

            self.particulas.append({
                "x": x,
                "y": y,
                "vx": math.cos(angulo) * random.uniform(1, 3),
                "vy": -math.sin(angulo) * random.uniform(1, 3),
                "vida": random.randint(10, 20),
                "color": (255, 220, 120)
            })

    # ======================================================
    # CHOQUES CON EL JUGADOR
    # ======================================================

    def golpea(self, jugador_rect):

        # Devuelve el punto del golpe (x, y) o None

        # Zona de choque un poco más pequeña que la nave
        zona = jugador_rect.inflate(-18, -14)

        for proyectil in self.proyectiles:

            rect = pygame.Rect(0, 0, proyectil["radio"] * 2, proyectil["radio"] * 2)
            rect.center = (proyectil["x"], proyectil["y"])

            if zona.colliderect(rect):

                self.proyectiles.remove(proyectil)

                return rect.center

        if self.laser_disparando():

            rayo = pygame.Rect(0, 0, 36, self.alto)
            rayo.centerx = self.laser["x"]

            if zona.colliderect(rayo):
                return zona.center

        return None

    # ======================================================
    # DIBUJAR
    # ======================================================

    def dibujar(self, pantalla):

        ticks = pygame.time.get_ticks()

        # --------------------------------------------------
        # Rayo
        # --------------------------------------------------

        if self.laser is not None:

            segundos_laser = self.tiempo - self.laser["inicio"]
            x = int(self.laser["x"])

            capa = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)

            if segundos_laser < 1.0:

                # Aviso: columna roja que parpadea cada vez más rápido
                velocidad = 120 - int(segundos_laser * 80)

                if (ticks // max(30, velocidad)) % 2 == 0:

                    pygame.draw.rect(capa, (255, 40, 40, 70), (x - 18, 0, 36, self.alto))

                pygame.draw.line(capa, (255, 80, 80, 200), (x - 18, 0), (x - 18, self.alto), 2)
                pygame.draw.line(capa, (255, 80, 80, 200), (x + 18, 0), (x + 18, self.alto), 2)

            else:

                # Disparo del rayo
                grosor = 36 + int(math.sin(ticks * 0.05) * 4)

                pygame.draw.rect(capa, (255, 60, 60, 120), (x - grosor, 0, grosor * 2, self.alto))
                pygame.draw.rect(capa, (255, 150, 120, 220), (x - grosor // 2, 0, grosor, self.alto))
                pygame.draw.rect(capa, (255, 255, 255, 255), (x - 6, 0, 12, self.alto))

            pantalla.blit(capa, (0, 0))

        # --------------------------------------------------
        # Nave del jefe
        # --------------------------------------------------

        if self.fase in ("entrando", "atacando"):

            self.dibujar_nave(pantalla, int(self.x), int(self.y), ticks)

            # Brillo blanco cuando le pega una bala
            if self.tiempo < self.destello_hasta:

                brillo = pygame.Surface((220, 90), pygame.SRCALPHA)
                pygame.draw.ellipse(brillo, (255, 255, 255, 110), (0, 0, 220, 90))
                pantalla.blit(brillo, (int(self.x) - 110, int(self.y) - 45))

        elif self.fase == "saliendo":

            # Tiembla y se desvanece
            if (ticks // 60) % 2 == 0:

                temblor_x = random.randint(-5, 5)
                temblor_y = random.randint(-5, 5)

                self.dibujar_nave(pantalla, int(self.x) + temblor_x, int(self.y) + temblor_y, ticks)

        # --------------------------------------------------
        # Proyectiles
        # --------------------------------------------------

        for proyectil in self.proyectiles:

            x = int(proyectil["x"])
            y = int(proyectil["y"])
            radio = proyectil["radio"]

            brillo = pygame.Surface((radio * 4, radio * 4), pygame.SRCALPHA)
            pygame.draw.circle(brillo, (255, 60, 80, 80), (radio * 2, radio * 2), radio * 2)
            pantalla.blit(brillo, (x - radio * 2, y - radio * 2))

            pygame.draw.circle(pantalla, (255, 80, 90), (x, y), radio)
            pygame.draw.circle(pantalla, (255, 220, 200), (x, y), radio // 2)

        # --------------------------------------------------
        # Explosión
        # --------------------------------------------------

        for particula in self.particulas:

            tamaño = max(1, particula["vida"] // 10)

            pygame.draw.circle(
                pantalla,
                particula["color"],
                (int(particula["x"]), int(particula["y"])),
                tamaño
            )

    def dibujar_nave(self, pantalla, cx, cy, ticks):

        # Alas
        pygame.draw.polygon(pantalla, (90, 20, 50), [
            (cx - 30, cy - 10), (cx - 95, cy + 5), (cx - 85, cy + 30), (cx - 25, cy + 20)
        ])

        pygame.draw.polygon(pantalla, (90, 20, 50), [
            (cx + 30, cy - 10), (cx + 95, cy + 5), (cx + 85, cy + 30), (cx + 25, cy + 20)
        ])

        # Puntas de las alas
        pygame.draw.polygon(pantalla, (200, 40, 70), [
            (cx - 95, cy + 5), (cx - 105, cy + 35), (cx - 85, cy + 30)
        ])

        pygame.draw.polygon(pantalla, (200, 40, 70), [
            (cx + 95, cy + 5), (cx + 105, cy + 35), (cx + 85, cy + 30)
        ])

        # Cuerpo
        pygame.draw.ellipse(pantalla, (130, 25, 60), (cx - 55, cy - 38, 110, 70))
        pygame.draw.ellipse(pantalla, (170, 40, 80), (cx - 45, cy - 34, 90, 50))

        # Cabina (ojo rojo)
        pulso = (math.sin(ticks * 0.008) + 1) / 2

        pygame.draw.ellipse(pantalla, (40, 0, 10), (cx - 24, cy - 26, 48, 24))

        pygame.draw.ellipse(
            pantalla,
            (255, int(40 + pulso * 80), 40),
            (cx - 16, cy - 22, 32, 16)
        )

        # Cañón: brilla más cuando está por disparar
        if self.fase == "atacando":

            falta = self.siguiente_disparo - self.segundos_ataque()
            carga = max(0, min(1, 1 - falta / self.CADENCIA))

        else:
            carga = 0

        pygame.draw.rect(pantalla, (60, 10, 25), (cx - 10, cy + 20, 20, 22), border_radius=4)

        pygame.draw.circle(
            pantalla,
            (255, int(80 + carga * 175), int(carga * 120)),
            (cx, cy + 40),
            int(5 + carga * 5)
        )

        # Luces que parpadean alrededor
        for i in range(6):

            encendida = ((ticks // 150) + i) % 3 == 0

            color = (255, 230, 120) if encendida else (90, 40, 40)

            angulo = math.pi + (i + 0.5) * math.pi / 6

            x = cx + math.cos(angulo) * -50
            y = cy + 12 + math.sin(angulo) * -14

            pygame.draw.circle(pantalla, color, (int(x), int(y)), 3)

    def dibujar_alerta(self, pantalla):

        # Aviso grande en el centro durante la alerta
        if self.fase != "alerta":
            return

        ticks = pygame.time.get_ticks()

        if (ticks // 250) % 2 == 1:
            return

        cy = self.alto // 2 - 60

        franja = pygame.Surface((self.ancho, 110), pygame.SRCALPHA)
        franja.fill((200, 20, 30, 150))
        pantalla.blit(franja, (0, cy - 55))

        pygame.draw.line(pantalla, (255, 220, 60), (0, cy - 55), (self.ancho, cy - 55), 4)
        pygame.draw.line(pantalla, (255, 220, 60), (0, cy + 55), (self.ancho, cy + 55), 4)

        # Triángulos de peligro
        for lado in (-1, 1):

            tx = self.ancho // 2 + lado * 225

            pygame.draw.polygon(pantalla, (255, 220, 60), [
                (tx, cy - 26), (tx + 26, cy + 20), (tx - 26, cy + 20)
            ])

            pygame.draw.line(pantalla, (60, 0, 0), (tx, cy - 10), (tx, cy + 6), 5)
            pygame.draw.circle(pantalla, (60, 0, 0), (tx, cy + 13), 3)

        texto = self.fuente.render("¡JEFE EN CAMINO!", True, (255, 255, 255))
        pantalla.blit(texto, texto.get_rect(center=(self.ancho // 2, cy - 8)))

        sub = self.fuente_pequeña.render("Sobrevive 10 segundos", True, (255, 220, 60))
        pantalla.blit(sub, sub.get_rect(center=(self.ancho // 2, cy + 30)))

    def dibujar_barra(self, pantalla):

        # Barra de tiempo arriba mientras ataca
        if self.fase != "atacando":
            return

        restante = max(0, self.DURACION_ATAQUE - self.segundos_ataque())

        ancho_barra = 180
        x = self.ancho // 2 - ancho_barra // 2
        y = 14

        texto = self.fuente_pequeña.render(f"JEFE  {restante:.0f}s", True, (255, 120, 120))
        pantalla.blit(texto, texto.get_rect(center=(self.ancho // 2, y + 6)))

        pygame.draw.rect(pantalla, (60, 20, 30), (x, y + 18, ancho_barra, 10), border_radius=5)

        pygame.draw.rect(
            pantalla,
            (255, 70, 80),
            (x, y + 18, int(ancho_barra * restante / self.DURACION_ATAQUE), 10),
            border_radius=5
        )
