# wrapper for the card class
# init and string functions
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def whichColor(self):
        return self.color

    def __str__(self):
        return str(self.value) + ' di ' + self.color

# class player
class Player:
    starter = 0
    points = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        if self.name.upper() == 'PC':
            self.ai = 1
        else:
            self.ai = 0

    def handCard(card):
        self.hand.append(card)

    def incrementPoints(self, cards):
        for card in cards:
            self.points = self.points + card.value

    def changeStarter(self, i):
        self.starter = i
