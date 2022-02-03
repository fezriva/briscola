import functions
import config

# central function, controls the game logic and development
def main(players):
    # create new deck and shuffle it
    deck = functions.newDeck()

    # take out one 2 if there are three players
    if len(players) == 3:
        for i, card in enumerate(deck):
            if card.getValue() == 2:
                deck.pop(i)
                break

    # setup the game
    # give 3 cards to each player
    for i in range(3):
        functions.giveCards(deck, players)
    
    # take the briscola card and place it under the deck
    briscola = deck.pop(0)
    seme_briscola = briscola.getColor()
    deck.append(briscola)

    # calculate number of rounds
    rounds = int(len(deck) / len(players))

    # start game turns
    while rounds > 0:

        # create empty table
        table = []

        # make each player make his choice
        for player in players:
            choice = functions.play(player, table)
            table.append(choice)
        
        # calculate winner and assign points
        round_winner, points = functions.roundWinner(table, seme_briscola)
        players[round_winner].incrementPoints(points)
        if config.CLI:
            print('{} wins this round and gets {} points'.format(players[round_winner].getName(), points))

        # reorder players list and give them a card each
        for i in range(round_winner):
            players.append(players.pop(0))

        if len(deck) > 0:
            functions.giveCards(deck, players)
        
        # decrease rounds value
        rounds -= 1

    # final ranking and winner declaration
    ranking = functions.finalRanking(players)

    for i, player in enumerate(ranking):
        if config.CLI:
            print('{}. {}'.format(i+1, str(player)))
    
    if ranking[0].getPoints() > ranking[1].getPoints():
        ranking[0].playerWins()