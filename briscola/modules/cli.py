def welcome_message():
    print('\n\nHello!')
    print('\nWelcome to a simple briscola interface\n')

    # Ask if the player is ready to play
    p_ready = ''
    while p_ready not in ['y', 'n']:
        p_ready = input('Ready to play? (y/n) ').lower()
    
    return p_ready

def players_number():
    print('The game can be played by 2, 3 or 4 players')

    p_number = 0
    while p_number not in range(2, 5):
        p_number = int(input('How many will play? '))

    return p_number

def teams():
    teams = ''
    while teams not in ['y', 'n']:
        teams = input('Do you want to play teams? (y/n) ').lower()
    
    return teams

def new_game():
    print("\n")
    p_ready = ''
    while p_ready not in ['y', 'n']:
        p_ready = input('Play again? (y/n) ').lower()
    
    return p_ready