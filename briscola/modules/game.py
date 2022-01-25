import functions

# central function, controls the game logic and development
def main(teams, players):
    # create new deck and shuffle it
    deck = functions.newDeck()

    # take out one 2 if there are three players
    if len(players) == 3:
        for i, card in enumerate(deck):
            if card.getValue() == 2:
                deck.pop(i)
                break

    # setup the game
    # give the cards to the players
    for i in range(3):
        functions.giveCards(deck, players)
    
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
            choice = functions.move(player, table)
            table.append(choice)
        
        # calculate winner and assign points
        i_winner, points = functions.roundWinner(table, seme_briscola)
        players[i_winner].getTeam().incrementPoints(points)
        print('{} wins this round and gets {} points'.format(players[i_winner].getName(), points))

        # reorder players list and give them a card each
        for i in range(i_winner):
            players.append(players.pop(0))
        if len(deck) > 0:
            functions.giveCards(deck, players)
        
        # decrease rounds value
        rounds -= 1

    # final ranking and winner declaration
    ranking = functions.finalRanking(teams)

    for i, team in enumerate(ranking):
        print('{}. {}'.format(i+1, str(team)))

    if ranking[0].getPoints() == ranking[1].getPoints():
        print('The game resulted in a tie')
    else:
        ranking[0].teamWins()
        print('{} won, congratulations!'.format(team.getName()))