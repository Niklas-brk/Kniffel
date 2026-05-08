import pygame


class GameUI:
    def __init__(self, game_logic):
        pygame.init()
        self.game_logic = game_logic

        self.size_x = 1500
        self.size_y = 1000
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption("Kniffel")

        self.background_color = (50, 50, 50)
        self.dice_color = (245, 245, 245)
        self.text_color = (25, 25, 25)
        self.info_color = (220, 220, 220)
        self.held_color = (255, 215, 0)
        self.board_color = (68, 68, 68)
        self.board_border_color = (165, 165, 165)
        self.table_line_color = (135, 135, 135)
        self.category_used_color = (190, 190, 190)
        self.preview_color = (210, 210, 210)
        self.section_fill_color = (76, 76, 76)

        self.board_left = 45
        self.board_top = 142
        self.board_width = 645
        self.board_height = 660

        self.right_panel_left = 740
        self.right_panel_top = 140
        self.right_panel_width = 400
        self.right_panel_height = 420

        self.dice_size = 100
        self.dice_gap = 20
        self.dice_top = 220
        self.dice_left = self.right_panel_left + (
            self.right_panel_width - ((3 * self.dice_size) + (2 * self.dice_gap))
        ) // 2

        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 42)
        self.value_font = pygame.font.SysFont(None, 72)
        self.info_font = pygame.font.SysFont(None, 36)
        self.row_font = pygame.font.SysFont(None, 28)

    def get_dice_rects(self):
        rects = []
        row_layout = [3, 2]
        dice_index = 0

        for row, dice_count in enumerate(row_layout):
            row_width = (dice_count * self.dice_size) + ((dice_count - 1) * self.dice_gap)
            row_left = self.dice_left + ((3 * self.dice_size + 2 * self.dice_gap) - row_width) // 2
            y_pos = self.dice_top + row * (self.dice_size + self.dice_gap)

            for column in range(dice_count):
                if dice_index >= len(self.game_logic.dice_list):
                    return rects
                x_pos = row_left + column * (self.dice_size + self.dice_gap)
                rects.append(pygame.Rect(x_pos, y_pos, self.dice_size, self.dice_size))
                dice_index += 1

        return rects

    def get_category_rects(self):
        rects = []
        row_height = 31
        sections = self.game_logic.get_category_sections()

        upper_start_y = self.board_top + 136
        lower_start_y = self.board_top + 418

        current_y = upper_start_y
        for entry in sections["upper"]:
            category = entry["category"]
            label = entry["label"]
            rect = pygame.Rect(self.board_left + 20, current_y, self.board_width - 40, row_height)
            rects.append((category, label, rect))
            current_y += row_height

        current_y = lower_start_y
        for entry in sections["lower"]:
            category = entry["category"]
            label = entry["label"]
            rect = pygame.Rect(self.board_left + 20, current_y, self.board_width - 40, row_height)
            rects.append((category, label, rect))
            current_y += row_height

        return rects

    def handle_mouse_click(self, position):
        for index, rect in enumerate(self.get_dice_rects()):
            if rect.collidepoint(position):
                self.game_logic.toggle_hold(index)
                return

        for category, _label, rect in self.get_category_rects():
            if rect.collidepoint(position):
                self.game_logic.take_category(category)
                return

    def draw_board(self):
        board_rect = pygame.Rect(self.board_left, self.board_top, self.board_width, self.board_height)
        pygame.draw.rect(self.screen, self.board_color, board_rect)
        pygame.draw.rect(self.screen, self.board_border_color, board_rect, width=2)

        board_text = self.title_font.render("Spielfeld", True, self.info_color)
        board_text_rect = board_text.get_rect(center=(self.board_left + self.board_width // 2, self.board_top + 35))
        self.screen.blit(board_text, board_text_rect)

        sections = self.game_logic.get_category_sections()
        category_entries = {
            entry["category"]: entry for entry in self.game_logic.get_category_entries()
        }

        upper_header_rect = pygame.Rect(self.board_left + 20, self.board_top + 72, self.board_width - 40, 31)
        self.draw_section_header(upper_header_rect, "Oberer Block")

        lower_header_y = self.board_top + 354
        lower_header_rect = pygame.Rect(self.board_left + 20, lower_header_y, self.board_width - 40, 31)
        self.draw_section_header(lower_header_rect, "Unterer Block")

        self.draw_column_header(pygame.Rect(self.board_left + 20, self.board_top + 103, self.board_width - 40, 31))

        lower_columns_rect = pygame.Rect(self.board_left + 20, lower_header_y + 31, self.board_width - 40, 31)
        self.draw_column_header(lower_columns_rect)

        for category, label, rect in self.get_category_rects():
            stored_score = category_entries[category]["stored_score"]
            if stored_score is not None:
                used_rect = pygame.Rect(rect.right - 90, rect.y + 3, 78, rect.height - 6)
                pygame.draw.rect(self.screen, self.section_fill_color, used_rect)

            label_surface = self.row_font.render(label, True, self.info_color)
            self.screen.blit(label_surface, (rect.x + 12, rect.y + 4))

            score_value = category_entries[category]["display_score"]
            score_color = self.preview_color if stored_score is None else self.category_used_color

            score_surface = self.row_font.render(str(score_value), True, score_color)
            score_rect = score_surface.get_rect(midright=(rect.right - 12, rect.y + rect.height // 2))
            self.screen.blit(score_surface, score_rect)

            pygame.draw.line(
                self.screen,
                self.table_line_color,
                (rect.left, rect.bottom),
                (rect.right, rect.bottom),
                1,
            )

        total_y = self.board_top + self.board_height - 42
        pygame.draw.line(
            self.screen,
            self.table_line_color,
            (self.board_left + 20, total_y - 8),
            (self.board_left + self.board_width - 20, total_y - 8),
            1,
        )
        total_text = self.info_font.render(
            f"Gesamt: {self.game_logic.get_total_score()}",
            True,
            self.info_color,
        )
        self.screen.blit(total_text, (self.board_left + 20, total_y))

    def draw_section_header(self, rect, title):
        pygame.draw.rect(self.screen, self.section_fill_color, rect)
        pygame.draw.line(
            self.screen,
            self.table_line_color,
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
            1,
        )
        title_surface = self.row_font.render(title, True, self.info_color)
        self.screen.blit(title_surface, (rect.x + 12, rect.y + 4))

    def draw_column_header(self, rect):
        pygame.draw.rect(self.screen, self.board_color, rect)
        name_header = self.row_font.render("Kategorie", True, self.info_color)
        score_header = self.row_font.render("Punkte", True, self.info_color)
        self.screen.blit(name_header, (rect.x + 12, rect.y + 4))
        score_header_rect = score_header.get_rect(midright=(rect.right - 12, rect.y + rect.height // 2))
        self.screen.blit(score_header, score_header_rect)
        pygame.draw.line(
            self.screen,
            self.table_line_color,
            (rect.left, rect.bottom),
            (rect.right, rect.bottom),
            1,
        )

    def draw_dice_area(self):
        panel_rect = pygame.Rect(
            self.right_panel_left,
            self.right_panel_top,
            self.right_panel_width,
            self.right_panel_height,
        )
        pygame.draw.rect(self.screen, self.board_color, panel_rect)
        pygame.draw.rect(self.screen, self.board_border_color, panel_rect, width=2)

        panel_text = self.title_font.render("Wuerfel", True, self.info_color)
        panel_text_rect = panel_text.get_rect(
            center=(self.right_panel_left + self.right_panel_width // 2, self.right_panel_top + 35)
        )
        self.screen.blit(panel_text, panel_text_rect)

    def draw_dice(self):
        for dice, rect in zip(self.game_logic.dice_list, self.get_dice_rects()):
            border_color = self.held_color if dice.held else self.text_color
            pygame.draw.rect(self.screen, self.dice_color, rect)
            pygame.draw.rect(self.screen, border_color, rect, width=3)

            value_surface = self.value_font.render(str(dice.value), True, self.text_color)
            value_rect = value_surface.get_rect(center=rect.center)
            self.screen.blit(value_surface, value_rect)

    def draw_info(self):
        info_surface = self.info_font.render(self.game_logic.info_text, True, self.info_color)
        info_rect = info_surface.get_rect(center=(self.size_x // 2, 90))
        self.screen.blit(info_surface, info_rect)

        roll_surface = self.info_font.render(
            f"Wuerfe uebrig: {self.game_logic.rolls_left}",
            True,
            self.info_color,
        )
        self.screen.blit(roll_surface, (self.right_panel_left, self.right_panel_top + self.right_panel_height + 20))

    def draw(self):
        self.screen.fill(self.background_color)
        self.draw_info()
        self.draw_board()
        self.draw_dice_area()
        self.draw_dice()
        pygame.display.update()

    def run(self):
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
                        self.game_logic.start_roll(current_time)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)

            self.game_logic.update(current_time)
            self.draw()
            self.clock.tick(60)

        pygame.quit()
