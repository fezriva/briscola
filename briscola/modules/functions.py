from modules import config, classes, cli

import random

# create deck of cards
def newDeck():
    colors = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    deck = [classes.Card(value, color) for value in range(1, 11) for color in colors]
    random.shuffle(deck)
    return deck

# give a card to a player
def giveCards(deck, players):
    for player in players:
        player.handCard(deck.pop(0))

# let the current player make is move
# return the chosen card
def play(player, table):

    if player.ai:
        # here will be the code for the MCTS powered AI
        # for now random choice
        selection = random.choice(range(len(player.hand)))
        
    else:
        if config.CLI:
            cli.printCards('Table:', table)    
            cli.printCards('Hand:', player.hand)

            selection = cli.selectCard(player.hand)
        
    card = player.hand.pop(selection)

    if config.CLI:
        print('{} plays a {}'.format(player.getName(), card))
    return card

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
def finalRanking(players):
    ranking = []
    for player in players:
        i = 0
        while i < len(ranking):
            if player.getPoints() > ranking[i].getPoints():
                break
            i += 1
        ranking.insert(i, player)
    return ranking
