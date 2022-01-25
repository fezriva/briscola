import modules.game as game
import modules.classes as classes

print('\n\nHello!')

gioco = input('Ready for a game of briscola? (y/n) ')

if gioco.lower() == 'y':
    print('Great!')
    print('\nTo play against the PC you just need to call \'PC\' the player')
    print('\nGood luck!\n\n')

    players_number = int(input('How many players? '))
    team = 0
    if players_number == 4:
        want_teams = input('Do you want to play teams? (y/n) ')
    teams = []
    players = []

    for i in range(players_number):
        if want_teams == 'y':
            team = team % 2 # assign team
            print('Next player will be in team {}'.format(team + 1))

        if team != team.getTeam():
            teams[team] = classes.Team(team)

        name = input('Player {} name is: '.format(i + 1))
        players[i] = classes.Player(name,team)
        team.addPlayer(players[i])
        team += 1

    while gioco.lower() == 'y':
        # call the game function
        game.main(teams, players)

        print("\n")
        gioco = input('Want to play again? (y/n) ')
        if gioco.lower() == 'y':
            players.append(players.pop(0))

print('Sad to see you go, but hope to see you soon!')
