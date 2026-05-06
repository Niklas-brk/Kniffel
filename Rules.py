from collections import Counter


class Rules:
    def __init__(self):
        self.rules = {
            "1": "Einser: Alle Einser zaehlen",
            "2": "Zweier: Alle Zweier zaehlen",
            "3": "Dreier: Alle Dreier zaehlen",
            "4": "Vierer: Alle Vierer zaehlen",
            "5": "Fuenfer: Alle Fuenfer zaehlen",
            "6": "Sechser: Alle Sechser zaehlen",
            "3P": "Dreierpasch: Summe aller Augen bei mindestens 3 gleichen Augen",
            "4P": "Viererpasch: Summe aller Augen bei mindestens 4 gleichen Augen",
            "FH": "Full House: 25 Punkte bei 3 gleichen und 2 gleichen Augen",
            "KS": "Kleine Strasse: 30 Punkte bei 4 aufeinanderfolgenden Zahlen",
            "GS": "Grosse Strasse: 40 Punkte bei 5 aufeinanderfolgenden Zahlen",
            "K": "Kniffel: 50 Punkte bei 5 gleichen Augen",
            "C": "Chance: Summe aller Augen",
        }

    @property
    def check_Rules(self):
        return self.rules

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
