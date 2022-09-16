# wrapper for the card class
# init and string functions
import random


### TODO change all colors into suits
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        
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

    def __str__(self):
        return str(self.value) + ' of ' + self.suit


# class player
class Player:

    def __init__(self, name):
        self.name = name
        
        self.hand = []
        self.points = 0
        self.wins = 0
        # self.team = team

    def handCard(self, card):
        self.hand.append(card)

    def playCard(self, card):
        return self.hand.pop(card)

    def incrementPoints(self, points):
        self.points += points

    def playerWins(self):
        self.wins += 1
    
    def resetPoints(self):
        self.points = 0

    def __str__(self):
        return self.name + ' gained: ' + str(self.points) + ' points'


# class team
'''
class Team:
    players = []
    points = 0
    wins = 0
    def __init__(self, team):
        self.name = 'Team ' + str(team)
    def addPlayer(self, player):
        self.players.append(player)
    def incrementPoints(self, points):
        self.points += points
    def teamWins(self):
        self.wins += 1
    def getPoints(self):
        return self.points
    def getPlayers(self):
        return self.players
    def getName(self):
        return self.name
    def __str__(self):
        pl_str = ''
        for i, player in enumerate(self.players):
            if i != 0:
                pl_str += ', '
            pl_str += player.getName()
        final_str = self.name + ':\n\tPlayers: ' + pl_str + '\n\tPoints: ' + self.points
        return final_str
'''