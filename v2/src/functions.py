from random import shuffle, choice
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

# central function, controls the game flow
def game(players):
    # create new deck and shuffle it
    deck = newDeck()

    # take out one 2 if there are three players
    if len(players) == 3:
        for i, card in enumerate(deck):
            if card.getValue() == 2:
                deck.pop(i)
                break

    # setup the game
    # give the cards to the players
    for i in range(3):
        giveCards(deck, players)
    # take the briscola card and place it under the deck
    briscola = deck.pop(0)
    seme_briscola = briscola.getColor()
    deck.append(briscola)

    rounds = len(deck) / len(players)
    # start game turns
    # for now while True, maybe change it later
    while rounds > 0:
        # create empty table
        table = []
        # make each player make his choice
        for player in players:
            choice = move(player, table)
            table.append(choice)
        # calculate winner and assign points
        i_winner, points = roundWinner(table, seme_briscola)
        players[i_winner].incrementPoints(points)
        print('{} wins this round and gets {} points'.format(players[i_winner].getName(), points))
        # reorder players list and give them a card each
        for i in range(i_winner):
            players.append(players.pop(0))
        if len(deck) > 0:
            giveCards(deck, players)
        # decrease rounds value
        rounds -= 1
    # check game winner -- ADD TEAMS OPTION
    for i, player in enumerate(players):
        if i == 0:
            higher = player
            winner = i
        else:
            if player.getPoints() > higher.getPoints():
                higher = player
                winner = i
    print('The winner is {} with {} staggering points'.format(players[winner].getName, players[winner].getPoints))
