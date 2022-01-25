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

    def getValue(self):
        return self.value

    def __str__(self):
        return str(self.value) + ' di ' + self.color

# class team to store points
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


# class player
class Player:

    def __init__(self, name, team):
        self.name = name
        self.hand = []
        self.team = team

        # to know if the player uses the AI
        if self.name.upper() == 'PC':
            self.ai = 1
        else:
            self.ai = 0

    def handCard(self, card):
        self.hand.append(card)

    def getName(self):
        return self.name

    def getTeam(self):
        return self.team
