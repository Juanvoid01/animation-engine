#rounded_rect.py

import pygame

# Función para dibujar un rectángulo con bordes redondeados
def draw_rounded_rect(screen, rect, color, corner_radius):
    """
    Dibuja un rectángulo con bordes redondeados.
    
    Args:
        screen: Superficie donde se dibujará (pantalla o superficie personalizada).
        rect: Rectángulo (x, y, ancho, alto).
        color: Color del rectángulo en formato RGB.
        corner_radius: Radio de los bordes redondeados.
    """
    x, y, width, height = rect
    # Dibujar el cuerpo del rectángulo
    inner_rect = pygame.Rect(x + corner_radius, y + corner_radius, width - 2 * corner_radius, height - 2 * corner_radius)
    pygame.draw.rect(screen, color, inner_rect)

    # Dibujar los círculos en las esquinas
    pygame.draw.circle(screen, color, (x + corner_radius, y + corner_radius), corner_radius)  # Esquina superior izquierda
    pygame.draw.circle(screen, color, (x + width - corner_radius, y + corner_radius), corner_radius)  # Esquina superior derecha
    pygame.draw.circle(screen, color, (x + corner_radius, y + height - corner_radius), corner_radius)  # Esquina inferior izquierda
    pygame.draw.circle(screen, color, (x + width - corner_radius, y + height - corner_radius), corner_radius)  # Esquina inferior derecha

    # Dibujar los lados del rectángulo
    pygame.draw.rect(screen, color, (x + corner_radius, y, width - 2 * corner_radius, corner_radius))  # Lado superior
    pygame.draw.rect(screen, color, (x, y + corner_radius, corner_radius, height - 2 * corner_radius))  # Lado izquierdo
    pygame.draw.rect(screen, color, (x + width - corner_radius, y + corner_radius, corner_radius, height - 2 * corner_radius))  # Lado derecho
    pygame.draw.rect(screen, color, (x + corner_radius, y + height - corner_radius, width - 2 * corner_radius, corner_radius))  # Lado inferior
