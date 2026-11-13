"""Entrada tactil para Pygame en Android y escritorio.

Durante la partida no dibuja botones: el jugador arrastra el dedo de lado a
lado en cualquier zona de la pantalla. Los menus usan toque y deslizamiento.
"""

import time

import pygame


class ControlesTactiles:
    """Convierte eventos SDL en coordenadas logicas y gestos."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.puntos = {}
        self.inicios = {}
        self.ultimo_atras = 0.0
        self.umbral_deslizamiento = max(32, int(min(ancho, alto) * 0.08))

    def _posicion_logica(self, x, y, normalizada=False):
        if normalizada:
            return int(x * self.ancho), int(y * self.alto)

        ventana = pygame.display.get_surface()
        if ventana is not None:
            ventana_ancho, ventana_alto = ventana.get_size()
            if ventana_ancho and ventana_alto:
                x = x * self.ancho / ventana_ancho
                y = y * self.alto / ventana_alto
        return int(x), int(y)

    def _gesto(self, inicio, final):
        dx = final[0] - inicio[0]
        dy = final[1] - inicio[1]
        if max(abs(dx), abs(dy)) < self.umbral_deslizamiento:
            return None
        if abs(dx) >= abs(dy):
            return "derecha" if dx > 0 else "izquierda"
        return "abajo" if dy > 0 else "arriba"

    def evento(self, evento):
        """Devuelve down, motion, up, swipe o back según el evento SDL."""
        finger_down = getattr(pygame, "FINGERDOWN", -1)
        finger_up = getattr(pygame, "FINGERUP", -1)
        finger_motion = getattr(pygame, "FINGERMOTION", -1)

        if evento.type == pygame.KEYDOWN:
            teclas_atras = {pygame.K_ESCAPE}
            tecla_ac_back = getattr(pygame, "K_AC_BACK", None)
            if tecla_ac_back is not None:
                teclas_atras.add(tecla_ac_back)
            if evento.key in teclas_atras:
                return "back", None
            return None

        if evento.type in (finger_down, finger_up, finger_motion):
            identificador = getattr(evento, "finger_id", 0)
            posicion = self._posicion_logica(
                getattr(evento, "x", 0),
                getattr(evento, "y", 0),
                normalizada=True,
            )

            if evento.type == finger_down:
                self.puntos[identificador] = posicion
                self.inicios[identificador] = posicion
                return "down", posicion

            if evento.type == finger_motion:
                anterior = self.puntos.get(identificador, posicion)
                self.puntos[identificador] = posicion
                return "motion", (posicion, posicion[0] - anterior[0], posicion[1] - anterior[1])

            inicio = self.inicios.pop(identificador, posicion)
            self.puntos.pop(identificador, None)
            gesto = self._gesto(inicio, posicion)
            return ("swipe", gesto) if gesto else ("up", posicion)

        if evento.type == pygame.MOUSEBUTTONDOWN and getattr(evento, "button", 0) == 1:
            posicion = self._posicion_logica(*evento.pos)
            self.puntos["mouse"] = posicion
            self.inicios["mouse"] = posicion
            return "down", posicion

        if evento.type == pygame.MOUSEMOTION and "mouse" in self.puntos and getattr(evento, "buttons", (0,))[0]:
            anterior = self.puntos["mouse"]
            posicion = self._posicion_logica(*evento.pos)
            self.puntos["mouse"] = posicion
            return "motion", (posicion, posicion[0] - anterior[0], posicion[1] - anterior[1])

        if evento.type == pygame.MOUSEBUTTONUP and getattr(evento, "button", 0) == 1:
            posicion = self._posicion_logica(*evento.pos)
            inicio = self.inicios.pop("mouse", posicion)
            self.puntos.pop("mouse", None)
            gesto = self._gesto(inicio, posicion)
            return ("swipe", gesto) if gesto else ("up", posicion)

        return None

    def doble_atras(self, ventana=0.85):
        """Devuelve True en la segunda pulsacion de atras."""
        ahora = time.monotonic()
        doble = ahora - self.ultimo_atras <= ventana
        self.ultimo_atras = ahora
        return doble
