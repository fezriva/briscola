from .classes import Player
from .classes import Card

from gym import Env

import random

# Reinforcement Learning Environment
class BriscolaEnv(Env):

    def __init__(self, playerNames):
        
        self.players = [Player(player_name) for player_name in playerNames]
        self.turn_players = self.players
        self.turn_winner = -1

        self.deck = []
        self.table = []
        self.briscola = None
        self.seme_briscola = None

        self.rounds_to_win = 3

        self.event = None
        self.round = 0

        self.turns = 0
        self.turn = 0

        self.renderInfo = {'printFlag': False, 'Msg': ""}


    def _getPlayerList(self):
        data = []
        for player in self.players:
            data.append({'playerName': player.name})
        return data


    def _getPlayerData(self):
        data = []
        for player in self.players:
            data.append(
                {
                    'playerName': player.name,
                    'playerPoints': player.points,
                    'playerWins': player.wins
                })
        return data


    def _getCardList(self, position):
        data = []
        for card in position:
            data.append(card._toArray())
        return data

    def _getStateList(self, player_cards=[]):
        data = []

        data.append(self.briscola._toNumerical() + [0])
        for card in self.table:
            data.append(card._toNumerical() + [1])
        for card in player_cards:
            data.append(card._toNumerical() + [2])
            
        return data

    # create deck of cards
    def _createNewDeck(self):
        deck = [Card(value, suit) for suit in range(4) for value in range(1, 11)]

        if len(self.players) == 3:
            deck.pop(1)
    
        random.shuffle(deck)
        return deck

    
    # gives a card to a player
    def _giveCards(self):
        for player in self.turn_players:
            player.handCard(self.deck.pop(0))


    def _evaluateTurn(self):
        turn_points = 0
        tmp_winner = -1
    
        # iterate through cards
        for i, card in enumerate(self.table):
            if i == 0:
                high_card = card
                tmp_winner = i
            else:
                if card.suit == self.seme_briscola:
                    if high_card.suit == self.seme_briscola:
                        if card.points > high_card.points:
                            high_card = card
                            tmp_winner = i
                        else:
                            if card.points == high_card.points:
                                if card.value > high_card.value:
                                    high_card = card
                                    tmp_winner = i
                    else:
                        high_card = card
                        tmp_winner = i
                else:
                    if card.suit == high_card.suit:
                        if card.points > high_card.points:
                            high_card = card
                            tmp_winner = i
                        else:
                            if card.points == high_card.points:
                                if card.value > high_card.value:
                                    high_card = card
                                    tmp_winner = i
            turn_points += card.points

        self.turn_winner = tmp_winner
        self.turn_players[self.turn_winner].incrementPoints(turn_points)
        return turn_points

    
    # show cards played in current trick
    def _printCurrentTurn(self):
        turnStr = '\nCurrent table:\n'
        for i, card in enumerate(self.table):
            turnStr += "{0}: {1}\n".format(self.turn_players[i].name, str(card))
        
        return turnStr


    def _event_GameStart(self):

        self.event_data_for_server = {}
        self.event_data_for_client \
        =   {
                'event_name': self.event,
                'broadcast': True,
                'data': {
                    'players' : self._getPlayerList()
                }
            }
        
        for player in self.players:
            player.wins = 0

        self.round = 0

        self.renderInfo = {'printFlag': False, 'Msg': ''}
        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Briscola Start ***\n'

    
    def _event_NewRound(self):

        self.round += 1
        self.turn_winner = -1

        for player in self.players:
            player.points = 0
            
        self.turn_players = self.players
        self.turn_players.append(self.turn_players.pop(0))

        self.deck = self._createNewDeck()

        self.turns = int(len(self.deck) / len(self.players))
        self.turn = 0

        self.table = []

        # give 3 cards to each player
        for i in range(3):
            self._giveCards()
        
        # take the briscola card and place it under the deck
        self.briscola = self.deck.pop(0)
        self.seme_briscola = self.briscola.suit
        self.deck.append(self.briscola)


        self.event_data_for_server = {'shift': 0}

        self.event_data_for_client \
        =   {   
                'event_name': self.event,
                'broadcast': True,
                'data': {
                    'players' : self._getPlayerData()
                }
            }

        self.event = 'PlayTurn'

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Start Round {0} ***\n'.format(self.round)
        for p in self.players:
            self.renderInfo['Msg'] += '{0}: {1}\n'.format(p.name, p.wins)
        

    def _event_PlayTurn(self):
        current_player = self.turn_players[self.event_data_for_server['shift']]

        self.event_data_for_client \
        =   {   'event_name' : self.event,
                'broadcast' : False,
                'data' : {
                    'playerName': current_player.name,
                    'hand': self._getCardList(current_player.hand),
                    'turn': self.turn + 1,
                    'briscola': self.briscola._toArray(),
                    'table': self._getCardList(self.table),
                    'state': self._getStateList(current_player.hand)
                }
            }


    def _event_PlayTurn_Action(self, action_data):
        current_player = self.turn_players[self.event_data_for_server['shift']]

        # player gives card selection
        playedCard = current_player.playCard(action_data['data']['action']['card'])
        self.table.append(playedCard)

        self.event_data_for_server['shift'] += 1
        self.event = 'ShowTurnAction'
        self._event_ShowTurnAction()


    def _event_ShowTurnAction(self):
        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = "\n" + self._printCurrentTurn()
        
        self.event_data_for_client \
        =   { 
                'event_name' : self.event,
                'broadcast' : True,
                'data' : {
                    'turn': self.turn + 1,
                    'briscola': self.briscola._toArray(),
                    'table': self._getCardList(self.table)
                }
            }
        
        if len(self.table) < 4:
            self.event = 'PlayTurn'
        else:
            self.event = 'ShowTurnEnd'


    def _event_ShowTurnEnd(self):
        
        points = self._evaluateTurn()
        winner = self.turn_players[self.turn_winner].name
                 
        self.event_data_for_client \
        =   { 
                'event_name' : self.event,
                'broadcast' : True,
                'data' : {
                    'turn': self.turn + 1,
                    'briscola': self.briscola._toArray(),
                    'table': self._getCardList(self.table),
                    'winner': winner,
                    'points': points,
                    'state': self._getStateList()
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Turn {0} ***\n'.format(self.turn+1)
        self.renderInfo['Msg'] += 'Winner: {0}\n'.format(winner)
        self.renderInfo['Msg'] += 'Points: {0}\n'.format(points)
        self.renderInfo['Msg'] += 'Table: {0}\n'.format(str([str(card) for card in self.table])[1:-1])
        
        self.table = []
        for i in range(self.turn_winner):
            self.turn_players.append(self.turn_players.pop(0))

        if len(self.deck) > 0:
            self._giveCards()

        self.turn += 1
        if self.turn < self.turns:
            self.event = 'PlayTurn'
            self.event_data_for_server = {'shift': 0}
        else:
            self.event = 'RoundEnd'
            self.event_data_for_server = {}

        reward = {}
        for player in self.players:
            if player.name == winner:
                reward[player.name] = points
            else:
                reward[player.name] = 0
        return reward


    def _event_RoundEnd(self):

        round_winner = max(self.players, key=lambda x:x.points)
        round_winner.wins += 1

        self.event_data_for_client \
        =   { 
                'event_name' : self.event,
                'broadcast' : True,
                'data' : {
                    'players' : self._getPlayerData(),
                    'round': self.round,
                    'round_winner': round_winner.name
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Round {0} End ***\n'.format(self.round)
        self.renderInfo['Msg'] += 'Winner: {0}\n'.format(round_winner)
        for p in self.players:
            self.renderInfo['Msg'] += '{0}: {1}\n'.format(p.name, p.points)
        
        
        # new round if no one has lost
        if round_winner.wins < self.rounds_to_win:
            self.event = 'NewRound'
            self.event_data_for_server = {}
        else:
            self.event = 'GameOver'
            self.event_data_for_server = {}


    def _event_GameOver(self):
        
        winner = max(self.players, key=lambda x:x.wins)
        
        self.event_data_for_client \
        =   { 
                'event_name' : self.event,
                'broadcast' : True,
                'data' : {
                    "players" : self._getPlayerData(),
                    'game_winner': winner.name
                }
            }

        self.renderInfo['printFlag'] = True
        self.renderInfo['Msg'] = '\n*** Game Over ***\n'
        for p in self.players:
            self.renderInfo['Msg'] += '{0}: {1}\n'.format(p.name, p.wins)
        
        self.renderInfo['Msg'] += '\nRound: {0}\n'.format(self.round)
        self.renderInfo['Msg'] += 'Winner: {0}\n'.format(winner.name)
        
        self.event = None


    def reset(self):
        
        # Generate a full deck of cards and shuffle it
        self.event = 'GameStart'
        self._event_GameStart()
        observation = self.event_data_for_client
        self.event = 'NewRound'
        self.event_data_for_server = {}
        
        return observation
                
    def render(self, mode = "human"):
        if self.renderInfo['printFlag']:
            print(self.renderInfo['Msg'])
            self.renderInfo['printFlag'] = False
            self.renderInfo['Msg'] = ""
    

        
    def step(self, action_data):
        observation, reward, done, info = None, None, None, None
            
        if self.event == 'NewRound':
            self._event_NewRound()

        elif self.event == 'PlayTurn' or self.event == 'ShowTurnAction' or self.event == 'ShowTurnEnd':
            if action_data != None and action_data['event_name'] == "PlayTurn_Action":
                self._event_PlayTurn_Action(action_data)
            else:
                if self.event == 'PlayTurn':
                    self._event_PlayTurn()
                elif self.event == 'ShowTurnEnd':
                    reward = self._event_ShowTurnEnd()
        
        elif self.event == 'RoundEnd':
            self._event_RoundEnd()
            
        elif self.event == 'GameOver':
            self._event_GameOver()

        elif self.event == None:
            self.event_data_for_client = None
            done = True


        observation = self.event_data_for_client
        return observation, reward, done, info