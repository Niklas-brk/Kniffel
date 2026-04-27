class Rules:
    def __init__(self):
        self.rules = { "1": "Einzer: Alle Einser zählen",
                       "2": "Zweier: Alle Zweier zählen",
                       "3": "Dreier: Alle Dreier zählen",
                       "4": "Vierer: Alle Vierer zählen",
                       "5": "Fünfer: Alle Fünfer zählen",
                       "6": "Sechser: Alle Sechser zählen",
                       "3P": "Dreierpasch: Alle Augen zählen wenn mindestens  3 gleiche Augen vorhanden sind",
                       "4P": "Viererpasch: Alle Augen zählen wenn mindestens  4 gleiche Augen vorhanden sind",
                       "FH": "Full House: 25 Punkte wenn 3 gleiche und 2 gleiche Augen vorhanden sind",
                       "K": "Kniffel: 50 Punkte wenn 5 gleiche Augen vorhanden sind",  }

    @property
    def check_Rules(self):
        return self.rules
    

