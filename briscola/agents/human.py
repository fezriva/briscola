class Human:
    def __init__(self, name, params):
        self.name = name
    
    def Do_Action(self, observation):
        if observation['event_name'] == 'GameStart':
            print(observation)
        elif observation['event_name'] == 'NewRound':
            print(observation)    
        elif observation['event_name'] == 'ShowPlayerHand':
            print(observation)

        elif observation['event_name'] == 'PlayTurn':
            print(observation)
            hand = observation['data']['hand']
            choose_card = int(input('choose card: ')) - 1

            return {
                    "event_name" : "PlayTurn_Action",
                    "data" : {
                        'playerName': self.name,
                        'action': {'card': choose_card}
                    }
                }

        elif observation['event_name'] == 'ShowTurnAction':
            print(observation)
        elif observation['event_name'] == 'ShowTurnEnd':
            print(observation)
        elif observation['event_name'] == 'RoundEnd':
            print(observation)
        elif observation['event_name'] == 'GameOver':
            print(observation)