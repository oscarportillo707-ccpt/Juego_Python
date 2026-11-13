import pygame


def presentar(superficie_logica):
    """Escala el lienzo lógico al tamaño completo de la pantalla."""
    ventana = pygame.display.get_surface()
    if ventana is None:
        return

    if ventana.get_size() != superficie_logica.get_size():
        superficie_final = pygame.transform.smoothscale(
            superficie_logica,
            ventana.get_size(),
        )
        ventana.blit(superficie_final, (0, 0))
    else:
        ventana.blit(superficie_logica, (0, 0))

    pygame.display.flip()
