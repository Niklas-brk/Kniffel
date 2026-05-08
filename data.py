from dataclasses import dataclass, field


CATEGORY_INFO = [
    ("1", "Einser"),
    ("2", "Zweier"),
    ("3", "Dreier"),
    ("4", "Vierer"),
    ("5", "Fuenfer"),
    ("6", "Sechser"),
    ("3P", "Dreierpasch"),
    ("4P", "Viererpasch"),
    ("FH", "Full House"),
    ("KS", "Kleine Strasse"),
    ("GS", "Grosse Strasse"),
    ("K", "Kniffel"),
    ("C", "Chance"),
]


@dataclass
class Dice:
    value: int = 1
    held: bool = False


@dataclass
class ScoreCard:
    scores: dict[str, int | None] = field(
        default_factory=lambda: {category: None for category, _label in CATEGORY_INFO}
    )

    def total_score(self):
        return sum(score for score in self.scores.values() if score is not None)


@dataclass
class Player:
    name: str = "Spieler 1"
    score_card: ScoreCard = field(default_factory=ScoreCard)
