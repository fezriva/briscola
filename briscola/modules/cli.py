def welcome_message():
    print('\nHello!')
    print('\nWelcome to a simple briscola interface\n')

    # Ask if the player is ready to play
    p_ready = ''
    while p_ready not in ['y', 'n']:
        p_ready = input('Ready to play? (y/n) ').lower()
    
    return p_ready

def players_number():
    print('\nThe game can be played by 2, 3 or 4 players')

    p_number = 0
    while p_number not in range(2, 5):
        p_number = int(input('How many will play? '))

    return p_number

'''
def teams():
    teams = ''
    while teams not in ['y', 'n']:
        teams = input('Do you want to play teams? (y/n) ').lower()
    
    return teams
'''

def new_game():
    print("\n")
    p_ready = ''
    while p_ready not in ['y', 'n']:
        p_ready = input('Play again? (y/n) ').lower()
    
    return p_ready

# print a list of cards
def printCards(location, cards):
    print(location)
    for i, card in enumerate(cards):
        print('{}. {}'.format(i+1, str(card)))

# select a card from player hand
def selectCard(hand):
    selection = len(hand)
    while selection not in range(len(hand)):
        selection = int(input('Select a card from your hand? (1/2/3) ')) - 1
    return selection