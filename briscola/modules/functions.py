from random import shuffle, choices
from briscola.modules import config
import classes

# create deck of cards
def newDeck():
    colors = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    deck = [classes.Card(value, color) for value in range(1, 10) for color in colors]
    shuffle(deck)
    return deck

# give a card to a player
def giveCards(deck, players):
    for player in players:
        player.handCard(deck.pop(0))

# print a list of cards
def printCards(location, cards):
    print(location)
    for i, card in enumerate(cards):
        print('{}. {}'.format(i+1, str(card)))
    print('\n')

# let the current player make is move
# return the chosen card
def play(player, table):

    if player.ai:
        # here will be the code for the MCTS powered AI
        # for now random choice
        choice = choices(player.hand)
    else:
        if config.CLI:
            printCards('Table:', table)    
            printCards('Hand:', player.hand)
        
            num = 3
            while num not in range(3):
                num = int(input('Select a card from your hand? (1/2/3) ')) - 1
        
        choice = player.hand.pop(num)

    return choice

# calculate which players wins the round and how many points he/she gets
def roundWinner(table, seme_briscola):
    round_points = 0
    
    # iterate through cards
    for i, card in enumerate(table):
        if i == 0:
            high_card = card
            card_number = i
        else:
            if card.getColor() == seme_briscola:
                if high_card.getColor() == seme_briscola:
                    if card.getPoints() > high_card.getPoints():
                        high_card = card
                        card_number = i
                else:
                    high_card = card
                    card_number = i
            else:
                if card.getColor() == high_card.getColor():
                    if card.getPoints() > high_card.getPoints():
                        high_card = card
                        card_number = i
        round_points += card.getPoints()
    return card_number, round_points

### CHECK HOW TO PROPERLY CREATE RANKING IN PYTHON
def finalRanking(teams):
    ranking = []
    for team in teams:
        i = 0
        while i < len(ranking):
            if team.getPoints() > ranking[i].getPoints():
                break
            i += 1
        ranking.insert(i, team)
    return ranking
