from random import shuffle, choices
import classes

# create deck of cards
def newDeck():
    colors = ['cuori', 'picche', 'quadri', 'fiori']
    deck = [classes.Card(value, color) for value in range(1, 10) for color in colors]
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
        choice = choices(player.hand)
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
                break;
            i += 1
        ranking.insert(i, team)
    return ranking
