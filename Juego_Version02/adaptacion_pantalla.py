import pygame


_superficie_escalada = None
_tamaño_ventana = None


def presentar(superficie_logica):
    """Escala el lienzo lógico al tamaño completo de la pantalla."""
    global _superficie_escalada, _tamaño_ventana

    ventana = pygame.display.get_surface()
    if ventana is None:
        return

    tamaño_ventana = ventana.get_size()
    if tamaño_ventana != superficie_logica.get_size():
        if _tamaño_ventana != tamaño_ventana:
            _superficie_escalada = pygame.Surface(tamaño_ventana)
            _tamaño_ventana = tamaño_ventana

        pygame.transform.scale(
            superficie_logica,
            tamaño_ventana,
            _superficie_escalada,
        )
        ventana.blit(_superficie_escalada, (0, 0))
    else:
        ventana.blit(superficie_logica, (0, 0))

    pygame.display.flip()
