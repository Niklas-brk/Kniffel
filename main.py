import sys

import pygame

import Cup


pygame.init()

SIZE_X = 1200
SIZE_Y = 700
SCREEN = pygame.display.set_mode((SIZE_X, SIZE_Y))
pygame.display.set_caption("Kniffel")

BACKGROUND_COLOR = (50, 50, 50)
DICE_COLOR = (245, 245, 245)
TEXT_COLOR = (25, 25, 25)
INFO_COLOR = (220, 220, 220)
HELD_COLOR = (255, 215, 0)
BOARD_COLOR = (80, 80, 80)
BOARD_BORDER_COLOR = (170, 170, 170)

DICE_SIZE = 100
DICE_GAP = 20
BOARD_LEFT = 40
BOARD_TOP = 140
BOARD_WIDTH = 640
BOARD_HEIGHT = 420
RIGHT_PANEL_LEFT = 740
RIGHT_PANEL_TOP = 140
RIGHT_PANEL_WIDTH = 400
RIGHT_PANEL_HEIGHT = 420
DICE_TOP = 220
DICE_LEFT = RIGHT_PANEL_LEFT + (RIGHT_PANEL_WIDTH - ((3 * DICE_SIZE) + (2 * DICE_GAP))) // 2

clock = pygame.time.Clock()
value_font = pygame.font.SysFont(None, 72)
info_font = pygame.font.SysFont(None, 36)

cup = Cup.Cup()
cup.roll_dice()


def draw_board_placeholder():
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)
    pygame.draw.rect(SCREEN, BOARD_COLOR, board_rect, border_radius=16)
    pygame.draw.rect(SCREEN, BOARD_BORDER_COLOR, board_rect, width=3, border_radius=16)

    board_text = info_font.render("Spielfeld", True, INFO_COLOR)
    board_text_rect = board_text.get_rect(center=(BOARD_LEFT + BOARD_WIDTH // 2, BOARD_TOP + 35))
    SCREEN.blit(board_text, board_text_rect)


def draw_dice_area():
    panel_rect = pygame.Rect(RIGHT_PANEL_LEFT, RIGHT_PANEL_TOP, RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT)
    pygame.draw.rect(SCREEN, BOARD_COLOR, panel_rect, border_radius=16)
    pygame.draw.rect(SCREEN, BOARD_BORDER_COLOR, panel_rect, width=3, border_radius=16)

    panel_text = info_font.render("Wuerfel", True, INFO_COLOR)
    panel_text_rect = panel_text.get_rect(center=(RIGHT_PANEL_LEFT + RIGHT_PANEL_WIDTH // 2, RIGHT_PANEL_TOP + 35))
    SCREEN.blit(panel_text, panel_text_rect)


def draw_ui():
    if cup.is_rolling:
        info_text = "Wuerfeln laeuft..."
    else:
        info_text = "Leertaste druecken, um 5 Sekunden zu wuerfeln"

    info_surface = info_font.render(info_text, True, INFO_COLOR)
    info_rect = info_surface.get_rect(center=(SIZE_X // 2, 100))
    SCREEN.blit(info_surface, info_rect)


def main():
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    cup.start_roll(current_time)

        cup.update(current_time)

        SCREEN.fill(BACKGROUND_COLOR)
        draw_ui()
        draw_board_placeholder()
        draw_dice_area()
        cup.draw(
            SCREEN,
            DICE_LEFT,
            DICE_TOP,
            DICE_SIZE,
            DICE_GAP,
            value_font,
            DICE_COLOR,
            TEXT_COLOR,
            HELD_COLOR,
        )
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
