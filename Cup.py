import random

import pygame

import Dice


class Cup:
    def __init__(self):
        self.dice_list = self.create_dice_list()
        self.is_rolling = False
        self.roll_duration_ms = 5000
        self.roll_update_ms = 100
        self.roll_start_time = 0
        self.last_roll_update = 0

    def create_dice_list(self):
        dice_list = []
        for _ in range(5):
            dice_list.append(Dice.Dice(0))
        return dice_list

    def roll_dice(self):
        for dice in self.dice_list:
            if not dice.held:
                dice.value = random.randint(1, 6)

    def start_roll(self, current_time):
        if self.is_rolling:
            return

        self.is_rolling = True
        self.roll_start_time = current_time
        self.last_roll_update = 0

    def update(self, current_time):
        if not self.is_rolling:
            return

        if current_time - self.roll_start_time >= self.roll_duration_ms:
            self.roll_dice()
            self.is_rolling = False
            return

        if current_time - self.last_roll_update >= self.roll_update_ms:
            self.roll_dice()
            self.last_roll_update = current_time

    def draw(self, screen, left, top, dice_size, dice_gap, font, dice_color, text_color, held_color):
        row_layout = [3, 2]
        dice_index = 0

        for row, dice_count in enumerate(row_layout):
            row_width = (dice_count * dice_size) + ((dice_count - 1) * dice_gap)
            row_left = left + ((3 * dice_size + 2 * dice_gap) - row_width) // 2
            y_pos = top + row * (dice_size + dice_gap)

            for column in range(dice_count):
                if dice_index >= len(self.dice_list):
                    return

                dice = self.dice_list[dice_index]
                x_pos = row_left + column * (dice_size + dice_gap)
                dice_rect = pygame.Rect(x_pos, y_pos, dice_size, dice_size)
                dice.draw(screen, dice_rect, font, dice_color, text_color, held_color)
                dice_index += 1
