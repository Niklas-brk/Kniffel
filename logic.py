import random
from collections import Counter

from data import CATEGORY_INFO, Dice, Player


class Rules:
    def __init__(self):
        self.rules = {
            "1": "Alle Einser zaehlen",
            "2": "Alle Zweier zaehlen",
            "3": "Alle Dreier zaehlen",
            "4": "Alle Vierer zaehlen",
            "5": "Alle Fuenfer zaehlen",
            "6": "Alle Sechser zaehlen",
            "3P": "Summe aller Augen bei mindestens 3 gleichen Augen",
            "4P": "Summe aller Augen bei mindestens 4 gleichen Augen",
            "FH": "25 Punkte bei 3 gleichen und 2 gleichen Augen",
            "KS": "30 Punkte bei 4 aufeinanderfolgenden Zahlen",
            "GS": "40 Punkte bei 5 aufeinanderfolgenden Zahlen",
            "K": "50 Punkte bei 5 gleichen Augen",
            "C": "Summe aller Augen",
        }

    def get_dice_values(self, dice_list):
        return [dice.value for dice in dice_list]

    def count_values(self, dice_list):
        return Counter(self.get_dice_values(dice_list))

    def score_upper(self, dice_list, target_value):
        values = self.get_dice_values(dice_list)
        return sum(value for value in values if value == target_value)

    def score_three_of_a_kind(self, dice_list):
        counts = self.count_values(dice_list)
        if max(counts.values()) >= 3:
            return sum(self.get_dice_values(dice_list))
        return 0

    def score_four_of_a_kind(self, dice_list):
        counts = self.count_values(dice_list)
        if max(counts.values()) >= 4:
            return sum(self.get_dice_values(dice_list))
        return 0

    def score_full_house(self, dice_list):
        counts = sorted(self.count_values(dice_list).values())
        if counts == [2, 3]:
            return 25
        return 0

    def score_small_straight(self, dice_list):
        unique_values = set(self.get_dice_values(dice_list))
        straights = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
        if any(straight.issubset(unique_values) for straight in straights):
            return 30
        return 0

    def score_large_straight(self, dice_list):
        unique_values = set(self.get_dice_values(dice_list))
        if unique_values == {1, 2, 3, 4, 5} or unique_values == {2, 3, 4, 5, 6}:
            return 40
        return 0

    def score_kniffel(self, dice_list):
        counts = self.count_values(dice_list)
        if max(counts.values()) == 5:
            return 50
        return 0

    def score_chance(self, dice_list):
        return sum(self.get_dice_values(dice_list))

    def calculate_score(self, category, dice_list):
        if category in {"1", "2", "3", "4", "5", "6"}:
            return self.score_upper(dice_list, int(category))
        if category == "3P":
            return self.score_three_of_a_kind(dice_list)
        if category == "4P":
            return self.score_four_of_a_kind(dice_list)
        if category == "FH":
            return self.score_full_house(dice_list)
        if category == "KS":
            return self.score_small_straight(dice_list)
        if category == "GS":
            return self.score_large_straight(dice_list)
        if category == "K":
            return self.score_kniffel(dice_list)
        if category == "C":
            return self.score_chance(dice_list)
        raise ValueError(f"Unbekannte Kategorie: {category}")


class GameLogic:
    def __init__(self):
        self.player = Player()
        self.rules = Rules()
        self.dice_list = [Dice() for _ in range(5)]
        self.is_rolling = False
        self.roll_duration_ms = 5000
        self.roll_update_ms = 100
        self.roll_start_time = 0
        self.last_roll_update = 0
        self.rolls_left = 3
        self.info_text = "Leertaste druecken, um 5 Sekunden zu wuerfeln"
        self.roll_dice()

    def roll_dice(self):
        for dice in self.dice_list:
            if not dice.held:
                dice.value = random.randint(1, 6)

    def start_roll(self, current_time):
        if self.is_rolling or self.rolls_left <= 0:
            return

        self.is_rolling = True
        self.roll_start_time = current_time
        self.last_roll_update = 0
        self.info_text = "Wuerfeln laeuft..."

    def update(self, current_time):
        if not self.is_rolling:
            return

        if current_time - self.roll_start_time >= self.roll_duration_ms:
            self.roll_dice()
            self.is_rolling = False
            self.rolls_left -= 1
            if self.rolls_left > 0:
                self.info_text = f"Noch {self.rolls_left} Wuerfe in diesem Zug"
            else:
                self.info_text = "Kein Wurf mehr uebrig. Kategorie waehlen."
            return

        if current_time - self.last_roll_update >= self.roll_update_ms:
            self.roll_dice()
            self.last_roll_update = current_time

    def toggle_hold(self, dice_index):
        if self.is_rolling:
            return
        if 0 <= dice_index < len(self.dice_list):
            self.dice_list[dice_index].held = not self.dice_list[dice_index].held

    def take_category(self, category):
        if self.player.score_card.scores[category] is not None:
            return

        score = self.rules.calculate_score(category, self.dice_list)
        self.player.score_card.scores[category] = score
        self.reset_turn()
        self.info_text = f"{category} eingetragen: {score} Punkte"

    def reset_turn(self):
        self.rolls_left = 3
        for dice in self.dice_list:
            dice.held = False

    def get_preview_score(self, category):
        if self.player.score_card.scores[category] is not None:
            return self.player.score_card.scores[category]
        return self.rules.calculate_score(category, self.dice_list)

    def get_category_entries(self):
        entries = []
        for category, label in CATEGORY_INFO:
            stored_score = self.player.score_card.scores[category]
            preview_score = stored_score if stored_score is not None else self.get_preview_score(category)
            entries.append(
                {
                    "category": category,
                    "label": label,
                    "stored_score": stored_score,
                    "display_score": preview_score,
                }
            )
        return entries

    def get_total_score(self):
        return self.player.score_card.total_score()

    def get_category_sections(self):
        entries = self.get_category_entries()
        return {
            "upper": entries[:6],
            "lower": entries[6:],
        }
