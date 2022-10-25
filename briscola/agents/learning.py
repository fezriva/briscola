from tensorflow.python.keras import models, layers, optimizers
from datetime import datetime
import numpy as np
import collections
import random


class DQNAgent:
    def __init__(self,  name, params = None):
        random.seed(datetime.now())
        self.name = name
        self.type = 'learning'
        
        if params != None:
            self.print_info = params['print_info']
        else:
            self.print_info = False

        self.state_size = (None, 3)
        self.action_size = 3
        self.memory = collections.deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = self._build_model()
 
    def _build_model(self):
        model = models.Sequential()
        model.add(layers.Dense(16, activation='relu', input_shape=self.state_size))
        model.add(layers.LSTM(16))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss="mse", optimizer = optimizers.adam_v2.Adam(learning_rate=self.learning_rate))
        return model
 
    def remember(self, state, action, reward, next_state, done): 
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            
            target_f = self.model.predict([state])

            # maybe make this a little better
            if reward > 0:
                target_f[0][action] = 1
            else:
                target_f[0][action] = 0

            self.model.fit(np.array([state]), np.array(target_f), epochs=1, verbose=0) 

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

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

            state = observation['data']['state']

            if np.random.rand() <= self.epsilon:
                choose_card = random.randrange(len(observation['data']['hand']))
            else:
                pred = self.model.predict([state])
                choose_card = np.argmax(pred)


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

    def save(self, name): 
        self.model.save_weights(name)