import Dice
import random

class Cup:
    def __init__(self):
        self.dice_list = self.diceList()

    def diceList(self):
        diceList = []
        for i in range(5):
            diceList.append(Dice.Dice(0))
        return diceList

    def roll_Dice(self):
        for dice in self.dice_list:
            if not dice.held:
                dice.value = random.randint(1, 6)
    