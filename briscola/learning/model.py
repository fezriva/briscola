from tensorflow.python.keras import models, layers, optimizers
import numpy as np

input_shape = (None, 3)
output_shape = 3

state = [[ [0, 8, 0], [0, 6, 1], [1, 10, 1], [3, 6, 1], [3, 2, 2], [1, 3, 2] ]]

def build_model(states, actions):
    model = models.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=states))
    model.add(layers.LSTM(16))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(actions, activation='linear'))
    return model

model = build_model(input_shape, output_shape)
model.summary()
print(state)
pred = model.predict(state)
#pred = np.argmax(pred)
print(pred)