from random import shuffle


# create deck of cards
def newDeck():
    colors = ['cuori', 'picche', 'quadri', 'fiori']
    deck = [Card(value, color) for value in range(1, 10) for color in colors]
    shuffle(deck)
    return deck

def giveCards(deck, players):
    for player in players:
        player.handCard(deck.pop(0))

# start the game
def gameStart():
    # create new deck and shuffle it
    deck = newDeck()
    # give the cards to the players
    for i in range(3):
        giveCards(deck, players)
    # take the briscola card and place it under the deck
    briscola = deck.pop(0)
    seme_briscola = briscola.whichColor()
    deck.append(briscola)

    return deck, seme_briscola
