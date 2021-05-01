from functions import *
from classes import *

print('\n\nHello!')

gioco = input('Ready for a game of briscola? (y/n) ')

if gioco.lower() == 'y':
    print('Great!')
    print('\nTo play against the PC you just need to call \'PC\' the player')
    print('\nGood luck!\n\n')

    players_number = int(input('How many players? '))
    players = []

    for i in range(players_number):
        name = input('Player {} name is: '.format(i+1))
        players[i] = Player(name)

    while gioco.lower() == 'y':
        # call the game function
        game(players)

        print("\n")
        gioco = input('Want to play again? (y/n) ')
        if gioco.lower() == 'y':
            players.append(players.pop(0))

print('Sad to see you go, but hope to see you soon!')
