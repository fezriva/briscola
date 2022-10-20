from datetime import datetime
import random

class RandomAI:
    def __init__(self, name, params = None):
        random.seed(datetime.now())
        self.name = name
        self.type = 'random'
        
        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False
    
    def act(self, observation):
        if observation['event_name'] == 'GameStart':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'NewRound':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowPlayerHand':
            if self.print_info:
                print(observation)

        elif observation['event_name'] == 'PlayTurn':
            if self.print_info:
                print(observation)

            hand = observation['data']['hand']
            choose_card = random.choice(range(len(observation['data']['hand'])))
            if self.print_info:
                print(self.name, ' choose card: ', choose_card)

            return {
                    "event_name" : "PlayTurn_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }

        elif observation['event_name'] == 'ShowTurnAction':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowTurnEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'RoundEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'GameOver':
            if self.print_info:
                print(observation)  