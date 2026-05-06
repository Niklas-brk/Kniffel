import pygame


class Dice:
    def __init__(self, value):
        self.value = value
        self.held = False

    def draw(self, screen, rect, font, dice_color, text_color, held_color):
        border_color = held_color if self.held else text_color
        pygame.draw.rect(screen, dice_color, rect, border_radius=16)
        pygame.draw.rect(screen, border_color, rect, width=4, border_radius=16)

        value_surface = font.render(str(self.value), True, text_color)
        value_rect = value_surface.get_rect(center=rect.center)
        screen.blit(value_surface, value_rect)
