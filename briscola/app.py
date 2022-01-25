import modules.classes as classes
import modules.config as config
import modules.game as game
import modules.cli as cli

player_ready = 'n'

if config.CLI:
    player_ready = cli.welcome_message()

while player_ready == 'y':

    players = []
    players_number = 0 # default
    if config.CLI:
        players_number = cli.players_number()

    team = 0
    teams = []
    want_teams = 'n' # default
    if players_number == 4:
        if config.CLI:
            want_teams = cli.teams()

    # set players
    for i in range(players_number):

        # assign a team to the new player
        if want_teams == 'y':
            team = team % 2
            if config.CLI:
                print('Team {}'.format(team+1))

        # create the Team class
        if team != team.getTeam():
            teams[team] = classes.Team(team)

        # create player
        name = ''
        if config.CLI:
            name = input('Team {} - Player {}\'s name: '.format(team, i + 1))
        
        players[i] = classes.Player(name,team)
        team.addPlayer(players[i])
        team += 1

    while gioco.lower() == 'y':
        # call the game function
        game.main(teams, players)

        if config.CLI:
            gioco = cli.new_game()

        if gioco.lower() == 'y':
            players.append(players.pop(0))

if config.CLI:
    print('\n\nSad to see you go, but hope to see you soon!')
