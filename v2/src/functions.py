import classes

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

# let the current player make is move
# return the chosen card
def move(player, table):
    if player.ai == 0:
        if len(table) != 0:
            print('Table:')
            for card in table:
                print(str(card))
            print()
        print('Hand:')
        for i, card in enumerate(player.hand):
            print('{}. {}'.format(i+1, str(card)))
        print()
        num = 4
        while num > 3:
            num = int(input('Select a card from your hand? (1/2/3) '))
        choice = player.hand.pop(num-1)
    elif player.ai == 1:
        # here will be the code for the MCTS powered AI
        # for now random choice
        choice = choice(player.hand)
    return choice
