# wrapper for the card class
# init and string functions
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        # assign points to each value
        if self.value == 1:
            self.points = 11
        elif self.value == 3:
            self.points = 10
        elif self.value == 8:
            self.points = 2
        elif self.value == 9:
            self.points = 3
        elif self.value == 10:
            self.points = 4
        else:
            self.points = 0

    def getColor(self):
        return self.color

    def getPoints(self):
        return self.points

    def __str__(self):
        return str(self.value) + ' di ' + self.color

# class player
class Player:
    starter = 0
    points = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        # to know if the player uses the AI
        if self.name.upper() == 'PC':
            self.ai = 1
        else:
            self.ai = 0

    def handCard(card):
        self.hand.append(card)

    def incrementPoints(self, points):
        self.points += points

    def changeStarter(self, i):
        self.starter = i

    def getName(self):
        return self.name
