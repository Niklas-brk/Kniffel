class Dice:
    def __init__(self,value):
        self.value = value
        self.held = False

    def dice(self):
        color = str(self.red)
        value = int(self.value)
        size = int(self.size)
        position = int(self.position)
        held = bool(self.held)
        return color, value, size, position, held
    